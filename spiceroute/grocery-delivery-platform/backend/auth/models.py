from datetime import datetime, time
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class StoreOwnerStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"

class ContractType(str, Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"
    PARTNER = "partner"

class MembershipTier(str, Enum):
    BASIC = "basic"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

class CommunicationPreference(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    NONE = "none"

class DietaryRestriction(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    LACTOSE_FREE = "lactose_free"
    NUT_FREE = "nut_free"
    NONE = "none"

class User(BaseModel):
    # Basic Information
    user_id: str = Field(..., description="Unique identifier for the user")
    email: EmailStr = Field(..., description="User's email address")
    password_hash: str = Field(..., description="Hashed password")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    address: str = Field(..., description="User's complete address")
    phone_number: str = Field(..., description="User's contact phone number")
    
    # Contract Information
    contract_type: ContractType = Field(..., description="Type of contract (individual/business/partner)")
    contract_id: str = Field(..., description="Unique identifier for the contract")
    customer_desc: Optional[str] = Field(None, description="Additional customer information or description")
    
    # Membership & Loyalty
    membership_tier: MembershipTier = Field(default=MembershipTier.BASIC, description="Customer's membership tier")
    loyalty_points: int = Field(default=0, description="Accumulated loyalty points")
    membership_start_date: Optional[datetime] = Field(None, description="Date when membership started")
    referral_code: Optional[str] = Field(None, description="Customer's unique referral code")
    referred_by: Optional[str] = Field(None, description="Referrer's user_id")
    
    # Shopping Preferences
    preferred_delivery_times: List[time] = Field(default_factory=list, description="Preferred delivery time slots")
    dietary_restrictions: List[DietaryRestriction] = Field(default_factory=list, description="Dietary restrictions or allergies")
    preferred_payment_methods: List[str] = Field(default_factory=list, description="Preferred payment methods")
    favorite_categories: List[str] = Field(default_factory=list, description="Favorite product categories")
    regular_shopping_days: List[str] = Field(default_factory=list, description="Regular shopping days (e.g., ['Monday', 'Friday'])")
    
    # Communication Preferences
    preferred_language: str = Field(default="en", description="Preferred language for communication")
    marketing_communication: bool = Field(default=True, description="Opt-in for marketing communications")
    notification_preferences: List[CommunicationPreference] = Field(
        default_factory=lambda: [CommunicationPreference.EMAIL],
        description="Preferred notification methods"
    )
    
    # System Information
    role: str = Field(..., description="User's role in the system")
    store_id: Optional[str] = Field(None, description="Associated store ID if applicable")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    is_active: bool = Field(default=True, description="Account status")
    is_verified: bool = Field(default=False, description="Email verification status")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "usr_123456",
                "email": "user@example.com",
                "password_hash": "hashed_password_here",
                "first_name": "John",
                "last_name": "Doe",
                "address": "123 Main St, City, State, ZIP",
                "phone_number": "+1234567890",
                "contract_type": "individual",
                "contract_id": "cnt_789012",
                "customer_desc": "Regular customer with monthly subscription",
                "membership_tier": "gold",
                "loyalty_points": 1500,
                "membership_start_date": "2023-01-01T00:00:00Z",
                "referral_code": "REF123",
                "referred_by": "usr_789012",
                "preferred_delivery_times": ["09:00", "17:00"],
                "dietary_restrictions": ["vegetarian", "gluten_free"],
                "preferred_payment_methods": ["credit_card", "apple_pay"],
                "favorite_categories": ["organic", "beverages"],
                "regular_shopping_days": ["Monday", "Friday"],
                "preferred_language": "en",
                "marketing_communication": True,
                "notification_preferences": ["email", "push"],
                "role": "customer",
                "store_id": "store_456",
                "created_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-15T12:00:00Z",
                "is_active": True,
                "is_verified": True
            }
        }

class StoreOwnerBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    status: StoreOwnerStatus = StoreOwnerStatus.PENDING
    oauth_provider: OAuthProvider
    oauth_id: str
    is_verified: bool = False
    last_login: Optional[datetime] = None

class StoreOwnerCreate(StoreOwnerBase):
    pass

class StoreOwnerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[StoreOwnerStatus] = None

class StoreOwnerInDB(StoreOwnerBase):
    id: str
    created_at: datetime
    updated_at: datetime

class StoreOwnerInvite(BaseModel):
    email: EmailStr
    invited_by: str
    expires_at: datetime
    token: str
    is_used: bool = False 