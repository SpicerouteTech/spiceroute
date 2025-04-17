from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from bson import ObjectId


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


class Nutrition(BaseModel):
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbohydrates: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    sodium: Optional[float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "calories": 100,
                "protein": 2.0,
                "fat": 0.5,
                "carbohydrates": 20.0,
                "fiber": 3.0,
                "sugar": 5.0,
                "sodium": 10.0
            }
        }


class CatalogItem(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    store_id: PyObjectId
    name: str
    description: str
    price: float
    sale_price: Optional[float] = None
    unit: str  # e.g., "lb", "kg", "each", "dozen"
    category: List[str] = []
    subcategory: Optional[str] = None
    image_urls: List[str] = []
    nutrition: Optional[Nutrition] = None
    stock_quantity: int = 0
    is_organic: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    country_of_origin: Optional[str] = None
    brand: Optional[str] = None
    tags: List[str] = []
    available: bool = True
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('price', 'sale_price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v
    
    @validator('stock_quantity')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "store_id": "6058f12b45783f2b3fc14d23",
                "name": "Organic Honeycrisp Apple",
                "description": "Fresh, locally-grown organic Honeycrisp apples",
                "price": 1.99,
                "sale_price": 1.49,
                "unit": "each",
                "category": ["Fruit", "Organic", "Fresh Produce"],
                "subcategory": "Apples",
                "image_urls": ["https://example.com/images/honeycrisp-apple.jpg"],
                "nutrition": {
                    "calories": 95,
                    "protein": 0.5,
                    "fat": 0.3,
                    "carbohydrates": 25.0,
                    "fiber": 4.4,
                    "sugar": 19.0,
                    "sodium": 1.8
                },
                "stock_quantity": 100,
                "is_organic": True,
                "is_vegan": True,
                "is_gluten_free": True,
                "country_of_origin": "USA",
                "brand": "Local Farms",
                "tags": ["fresh", "sweet", "seasonal"],
                "available": True,
                "featured": True
            }
        }


class CatalogItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    sale_price: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[List[str]] = None
    subcategory: Optional[str] = None
    image_urls: Optional[List[str]] = None
    nutrition: Optional[Nutrition] = None
    stock_quantity: Optional[int] = None
    is_organic: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    country_of_origin: Optional[str] = None
    brand: Optional[str] = None
    tags: Optional[List[str]] = None
    available: Optional[bool] = None
    featured: Optional[bool] = None
    
    @validator('price', 'sale_price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v
    
    @validator('stock_quantity')
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[Dict[str, Any]] 