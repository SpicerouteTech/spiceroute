from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, EmailStr, validator, constr, condecimal
from bson import ObjectId
from decimal import Decimal
import re


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str = "USA"
    
    class Config:
        schema_extra = {
            "example": {
                "street": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "postal_code": "94105",
                "country": "USA"
            }
        }


class BusinessHours(BaseModel):
    day: int = Field(..., ge=0, le=6)  # 0 = Sunday, 6 = Saturday
    open_time: str = Field(..., regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    close_time: str = Field(..., regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    is_closed: bool = Field(default=False)
    
    @validator('day')
    def validate_day(cls, v):
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if v not in valid_days:
            raise ValueError(f"Day must be one of {valid_days}")
        return v
    
    @validator('open_time', 'close_time')
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, "%H:%M")
        except ValueError:
            raise ValueError("Time must be in 24-hour format (HH:MM)")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "day": "Monday",
                "open_time": "09:00",
                "close_time": "18:00",
                "is_closed": False
            }
        }


class StoreOwnerProfile(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str  # Reference to the auth service user ID
    store_name: str
    description: Optional[str] = None
    email: EmailStr
    phone: str
    category: List[str] = []
    address: Address
    business_hours: List[BusinessHours] = []
    logo_url: Optional[str] = None
    website: Optional[str] = None
    verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    average_rating: float = 0.0
    total_reviews: int = 0
    active: bool = True
    
    @validator('phone')
    def validate_phone(cls, v):
        # Simple validation for US phone numbers
        if not re.match(r'^\d{10}$|^\d{3}-\d{3}-\d{4}$', v):
            raise ValueError("Phone number must be 10 digits or in format XXX-XXX-XXXX")
        return v
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "user_id": "auth0|12345",
                "store_name": "Green Grocers",
                "description": "Fresh organic produce and groceries",
                "email": "contact@greengrocers.com",
                "phone": "415-555-1234",
                "category": ["Organic", "Local", "Groceries"],
                "address": {
                    "street": "123 Main St",
                    "city": "San Francisco",
                    "state": "CA",
                    "postal_code": "94105",
                    "country": "USA"
                },
                "business_hours": [
                    {
                        "day": "Monday",
                        "open_time": "09:00",
                        "close_time": "18:00",
                        "is_closed": False
                    }
                ],
                "logo_url": "https://example.com/logo.png",
                "website": "https://greengrocers.com",
                "verified": True,
                "active": True
            }
        }


class StoreOwnerProfileUpdate(BaseModel):
    store_name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    category: Optional[List[str]] = None
    address: Optional[Address] = None
    business_hours: Optional[List[BusinessHours]] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    active: Optional[bool] = None
    
    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\d{10}$|^\d{3}-\d{3}-\d{4}$', v):
            raise ValueError("Phone number must be 10 digits or in format XXX-XXX-XXXX")
        return v
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class StoreOwner(BaseModel):
    email: EmailStr = Field(..., description="Store owner's email address")
    name: str = Field(..., min_length=2, max_length=100)
    oauth_id: str = Field(..., min_length=5, max_length=100)
    oauth_provider: str = Field(..., pattern="^(google|facebook)$")
    picture: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=15)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = Field(default=True)
    stores: List[str] = Field(default_factory=list)  # List of store IDs
    
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


class StoreLocation(BaseModel):
    address: str = Field(..., min_length=5, max_length=200)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=50)
    postal_code: str = Field(..., min_length=5, max_length=10)
    country: str = Field(..., min_length=2, max_length=50)
    coordinates: Optional[Dict[str, float]] = Field(None)  # {"lat": float, "lng": float}


class Store(BaseModel):
    store_id: str = Field(..., min_length=5)
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    owner_email: EmailStr
    location: StoreLocation
    business_hours: List[BusinessHours]
    phone: str = Field(..., regex="^\+?1?\d{9,15}$")
    email: EmailStr
    website: Optional[str] = Field(None, max_length=200)
    delivery_radius: float = Field(..., gt=0)  # in kilometers
    minimum_order: Decimal = Field(..., ge=0)
    delivery_fee: Decimal = Field(..., ge=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website URL must start with http:// or https://')
        return v


class Category(BaseModel):
    category_id: str = Field(..., min_length=5)
    store_id: str
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('image_url')
    def validate_image_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Image URL must start with http:// or https://')
        return v


class Product(BaseModel):
    product_id: str = Field(..., min_length=5)
    store_id: str
    category_id: str
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    price: Decimal = Field(..., ge=0)
    sale_price: Optional[Decimal] = Field(None, ge=0)
    unit: str = Field(..., regex="^(piece|gram|kg|lb|oz|ml|l|pack)$")
    stock_quantity: int = Field(..., ge=0)
    image_url: Optional[str] = Field(None, max_length=500)
    is_available: bool = Field(default=True)
    is_featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('sale_price')
    def validate_sale_price(cls, v, values):
        if v and v >= values['price']:
            raise ValueError('Sale price must be less than regular price')
        return v
    
    @validator('image_url')
    def validate_image_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Image URL must start with http:// or https://')
        return v


class TokenData(BaseModel):
    email: EmailStr
    exp: datetime
    oauth_provider: str


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    expires_in: int = Field(..., gt=0) 