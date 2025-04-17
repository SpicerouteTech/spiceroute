from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator
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
    day: str
    open_time: str
    close_time: str
    is_closed: bool = False
    
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
        import re
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
        import re
        if not re.match(r'^\d{10}$|^\d{3}-\d{3}-\d{4}$', v):
            raise ValueError("Phone number must be 10 digits or in format XXX-XXX-XXXX")
        return v
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        } 