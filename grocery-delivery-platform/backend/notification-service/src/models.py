from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from bson import ObjectId
from enum import Enum

class NotificationType(str, Enum):
    ORDER_STATUS = "order_status"
    PROMOTION = "promotion"
    PRICE_ALERT = "price_alert"
    STOCK_ALERT = "stock_alert"
    DELIVERY_UPDATE = "delivery_update"
    MARKETING = "marketing"
    SYSTEM = "system"
    SECURITY = "security"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PUSH = "push"
    IN_APP = "in_app"
    WEB_PUSH = "web_push"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class UserSegment(BaseModel):
    """Model for user segmentation criteria."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str
    criteria: Dict[str, Any]  # e.g., {"location": "NYC", "age_range": "18-25"}
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}

class NotificationTemplate(BaseModel):
    """Model for notification templates."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str
    type: NotificationType
    channels: List[NotificationChannel]
    templates: Dict[NotificationChannel, Dict[str, str]]  # Channel-specific templates
    variables: List[str]  # Template variables
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}

class NotificationPreference(BaseModel):
    """Model for user notification preferences."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    user_id: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    channels: Dict[NotificationType, List[NotificationChannel]]
    quiet_hours: Optional[Dict[str, str]] = None  # e.g., {"start": "22:00", "end": "07:00"}
    frequency_limits: Optional[Dict[NotificationType, int]] = None
    push_tokens: List[str] = Field(default_factory=list)
    whatsapp_opted_in: bool = False
    marketing_opted_in: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}

class Campaign(BaseModel):
    """Model for notification campaigns."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str
    template_id: str
    segment_id: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None  # For scheduled campaigns
    variables: Dict[str, Any]  # Template variable values
    status: str = "draft"  # draft, scheduled, in_progress, completed, cancelled
    metrics: Dict[str, int] = Field(default_factory=dict)  # Delivery metrics
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}

class Notification(BaseModel):
    """Model for individual notifications."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    user_id: str
    type: NotificationType
    channel: NotificationChannel
    template_id: Optional[str] = None
    campaign_id: Optional[str] = None
    priority: NotificationPriority = NotificationPriority.MEDIUM
    content: Dict[str, str]  # {"subject": "...", "body": "..."}
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: NotificationStatus = NotificationStatus.PENDING
    error: Optional[str] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()} 