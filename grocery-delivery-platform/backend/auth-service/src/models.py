from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re

class StoreOwner(BaseModel):
    email: EmailStr = Field(..., description="Store owner's email address")
    name: str = Field(..., min_length=2, max_length=100)
    oauth_id: str = Field(..., min_length=5, max_length=100)
    oauth_provider: str = Field(..., pattern="^(google|facebook)$")
    picture: Optional[str] = Field(None, max_length=500)
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

    class Config:
        schema_extra = {
            "example": {
                "email": "store@example.com",
                "name": "John Doe",
                "oauth_id": "123456789",
                "oauth_provider": "google",
                "picture": "https://example.com/picture.jpg"
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

class ErrorLog(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: str = Field(..., pattern="^(INFO|WARNING|ERROR|CRITICAL)$")
    service: str = Field(default="auth-service")
    message: str
    details: Optional[dict] = None
    trace_id: Optional[str] = None 