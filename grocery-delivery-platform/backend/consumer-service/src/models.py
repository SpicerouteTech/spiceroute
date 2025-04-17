from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field, validator, constr
from decimal import Decimal
import re

class Address(BaseModel):
    street: str = Field(..., min_length=5, max_length=100)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    postal_code: str = Field(..., min_length=5, max_length=10)
    is_default: bool = Field(default=False)
    
    @validator('postal_code')
    def validate_postal_code(cls, v):
        if not re.match("^[0-9]{5}(-[0-9]{4})?$", v):
            raise ValueError('Invalid postal code format')
        return v

class PaymentMethod(BaseModel):
    type: str = Field(..., pattern="^(credit|debit)$")
    last_four: str = Field(..., min_length=4, max_length=4)
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int = Field(..., ge=2024)
    is_default: bool = Field(default=False)
    card_holder_name: str = Field(..., min_length=2, max_length=100)
    
    @validator('last_four')
    def validate_last_four(cls, v):
        if not v.isdigit():
            raise ValueError('Last four must contain only digits')
        return v

class CartItem(BaseModel):
    product_id: str = Field(..., description="Product ID from catalog")
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)
    name: str = Field(..., min_length=1)
    image_url: Optional[str] = None
    
    @validator('unit_price')
    def validate_price(cls, v):
        return Decimal(str(v)).quantize(Decimal('0.01'))

class Cart(BaseModel):
    items: List[CartItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def total(self) -> Decimal:
        return sum(item.unit_price * item.quantity for item in self.items)

class OrderStatus(str):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(BaseModel):
    order_id: str = Field(..., min_length=10)
    consumer_email: EmailStr
    items: List[CartItem]
    total_amount: Decimal
    delivery_address: Address
    payment_method: PaymentMethod
    status: str = Field(..., pattern="^(pending|confirmed|preparing|out_for_delivery|delivered|cancelled)$")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_delivery: Optional[datetime] = None
    delivery_notes: Optional[str] = Field(None, max_length=500)
    
    @validator('total_amount')
    def validate_total(cls, v):
        return Decimal(str(v)).quantize(Decimal('0.01'))

class Consumer(BaseModel):
    email: EmailStr = Field(..., description="Consumer's email address")
    name: str = Field(..., min_length=2, max_length=100)
    oauth_id: str = Field(..., min_length=5, max_length=100)
    oauth_provider: str = Field(..., pattern="^(google|facebook)$")
    picture: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=15)
    addresses: List[Address] = Field(default_factory=list)
    payment_methods: List[PaymentMethod] = Field(default_factory=list)
    cart: Optional[Cart] = None
    orders: List[str] = Field(default_factory=list)  # List of order IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = Field(default=True)
    
    @validator('name')
    def validate_name(cls, v):
        if not re.match("^[a-zA-Z0-9 .-]+$", v):
            raise ValueError('Name contains invalid characters')
        return v.strip()
    
    @validator('picture')
    def validate_picture_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Picture URL must start with http:// or https://')
        return v
        
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match("^\+?1?\d{9,15}$", v):
            raise ValueError('Invalid phone number format')
        return v

    class Config:
        schema_extra = {
            "example": {
                "email": "consumer@example.com",
                "name": "John Doe",
                "oauth_id": "123456789",
                "oauth_provider": "google",
                "picture": "https://example.com/picture.jpg",
                "phone": "+1234567890"
            }
        }

class TokenData(BaseModel):
    email: EmailStr
    exp: datetime
    oauth_provider: str

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    expires_in: int = Field(..., gt=0) 