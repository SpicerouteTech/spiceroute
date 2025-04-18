from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime

from ..auth import get_current_customer
from .models import NotificationPreferenceDB, PushTokenDB
from .db import NotificationDatabaseService
from ..config import get_settings

router = APIRouter(prefix="/notifications", tags=["notifications"])
settings = get_settings()

def get_notification_db():
    return NotificationDatabaseService(settings.MONGODB_URL, settings.DATABASE_NAME)

@router.get("/preferences", response_model=NotificationPreferenceDB)
async def get_notification_preferences(
    customer_id: str = Depends(get_current_customer),
    db: NotificationDatabaseService = Depends(get_notification_db)
):
    """Get current notification preferences for the authenticated customer."""
    prefs = await db.get_preferences(customer_id)
    if not prefs:
        # Create default preferences if none exist
        prefs = NotificationPreferenceDB(
            customer_id=customer_id,
            channels=["email"],  # Default to email only
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        prefs = await db.upsert_preferences(prefs)
    return prefs

@router.put("/preferences", response_model=NotificationPreferenceDB)
async def update_notification_preferences(
    preferences: NotificationPreferenceDB,
    customer_id: str = Depends(get_current_customer),
    db: NotificationDatabaseService = Depends(get_notification_db)
):
    """Update notification preferences for the authenticated customer."""
    if preferences.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify preferences for another customer"
        )
    
    return await db.upsert_preferences(preferences)

@router.post("/push/register-token", response_model=PushTokenDB)
async def register_push_token(
    token: PushTokenDB,
    customer_id: str = Depends(get_current_customer),
    db: NotificationDatabaseService = Depends(get_notification_db)
):
    """Register a new push notification token."""
    if token.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot register token for another customer"
        )
    
    # Ensure the token is marked as active
    token.is_active = True
    token.last_used = datetime.utcnow()
    return await db.register_push_token(token)

@router.delete("/push/unregister-token")
async def unregister_push_token(
    token: str,
    customer_id: str = Depends(get_current_customer),
    db: NotificationDatabaseService = Depends(get_notification_db)
):
    """Unregister a push notification token."""
    success = await db.unregister_push_token(customer_id, token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found or already unregistered"
        )
    return {"message": "Token unregistered successfully"}

@router.post("/whatsapp/opt-in", response_model=NotificationPreferenceDB)
async def opt_in_whatsapp(
    phone: str,
    customer_id: str = Depends(get_current_customer),
    db: NotificationDatabaseService = Depends(get_notification_db)
):
    """Opt in to WhatsApp notifications."""
    prefs = await db.get_preferences(customer_id)
    if not prefs:
        prefs = NotificationPreferenceDB(
            customer_id=customer_id,
            channels=["email"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    prefs.whatsapp_opted_in = True
    prefs.phone = phone
    if "whatsapp" not in prefs.channels:
        prefs.channels.append("whatsapp")
    
    return await db.upsert_preferences(prefs)

@router.post("/whatsapp/opt-out", response_model=NotificationPreferenceDB)
async def opt_out_whatsapp(
    customer_id: str = Depends(get_current_customer),
    db: NotificationDatabaseService = Depends(get_notification_db)
):
    """Opt out from WhatsApp notifications."""
    prefs = await db.get_preferences(customer_id)
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No notification preferences found"
        )
    
    prefs.whatsapp_opted_in = False
    if "whatsapp" in prefs.channels:
        prefs.channels.remove("whatsapp")
    
    return await db.upsert_preferences(prefs) 