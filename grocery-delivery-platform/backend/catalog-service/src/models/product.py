from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from decimal import Decimal
from bson import ObjectId


class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            raise ValueError("Invalid ObjectId")
        return str(v)


class ProductImage(BaseModel):
    url: HttpUrl
    alt_text: str
    is_primary: bool = False
    width: Optional[int] = None
    height: Optional[int] = None


class ProductVariant(BaseModel):
    id: PydanticObjectId = Field(default_factory=lambda: str(ObjectId()))
    sku: str
    name: str
    price: Decimal
    compare_at_price: Optional[Decimal] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    stock_quantity: int = 0
    is_available: bool = True


class Product(BaseModel):
    id: PydanticObjectId = Field(default_factory=lambda: str(ObjectId()))
    store_id: PydanticObjectId
    name: str
    description: str
    category_id: PydanticObjectId
    subcategory_id: Optional[PydanticObjectId] = None
    brand: Optional[str] = None
    images: List[ProductImage] = []
    variants: List[ProductVariant] = []
    tags: List[str] = []
    is_featured: bool = False
    is_active: bool = True
    tax_rate: Optional[Decimal] = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
            Decimal: lambda d: str(d)
        }
        
    def get_primary_image(self) -> Optional[ProductImage]:
        """Get the primary image for the product"""
        return next((img for img in self.images if img.is_primary), None)
    
    def get_default_variant(self) -> Optional[ProductVariant]:
        """Get the default variant for the product"""
        return self.variants[0] if self.variants else None
    
    def get_price_range(self) -> tuple[Decimal, Decimal]:
        """Get the min and max prices across all variants"""
        if not self.variants:
            return Decimal('0'), Decimal('0')
        prices = [v.price for v in self.variants]
        return min(prices), max(prices)
    
    def get_total_stock(self) -> int:
        """Get total stock across all variants"""
        return sum(v.stock_quantity for v in self.variants)
    
    def is_in_stock(self) -> bool:
        """Check if any variant is in stock"""
        return any(v.stock_quantity > 0 for v in self.variants)
    
    def update_timestamps(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow() 