from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class NotificationPreferenceDB(BaseModel):
    """Database model for notification preferences."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    customer_id: str
    channels: List[str]
    email: Optional[str] = None
    phone: Optional[str] = None
    push_tokens: List[str] = Field(default_factory=list)
    whatsapp_opted_in: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: str
        }

class PushTokenDB(BaseModel):
    """Database model for push notification tokens."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    customer_id: str
    token: str
    device_type: str  # ios, android, web
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: str
        }

class NotificationLogDB(BaseModel):
    """Database model for notification logs."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    customer_id: str
    channel: str
    notification_type: str  # order_status, promotion, etc.
    content: str
    metadata: dict = Field(default_factory=dict)
    status: str  # sent, failed, delivered
    error: Optional[str] = None
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: str
        } 