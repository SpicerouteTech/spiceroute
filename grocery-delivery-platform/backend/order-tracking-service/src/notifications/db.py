from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from .models import NotificationPreferenceDB, PushTokenDB, NotificationLogDB
import logging

logger = logging.getLogger(__name__)

class NotificationDatabaseService:
    def __init__(self, mongodb_url: str, database_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db: AsyncIOMotorDatabase = self.client[database_name]
        
    async def init_indexes(self):
        """Initialize database indexes."""
        try:
            # Notification preferences indexes
            await self.db.notification_preferences.create_index("customer_id", unique=True)
            
            # Push tokens indexes
            await self.db.push_tokens.create_index([("customer_id", 1), ("token", 1)], unique=True)
            await self.db.push_tokens.create_index("token")
            
            # Notification logs indexes
            await self.db.notification_logs.create_index([
                ("customer_id", 1),
                ("sent_at", -1)
            ])
            await self.db.notification_logs.create_index("sent_at")
            
            logger.info("Successfully initialized notification database indexes")
        except Exception as e:
            logger.error(f"Error initializing notification database indexes: {e}")
            raise

    async def get_preferences(self, customer_id: str) -> Optional[NotificationPreferenceDB]:
        """Get notification preferences for a customer."""
        try:
            prefs = await self.db.notification_preferences.find_one({"customer_id": customer_id})
            return NotificationPreferenceDB(**prefs) if prefs else None
        except Exception as e:
            logger.error(f"Error getting notification preferences for customer {customer_id}: {e}")
            raise

    async def upsert_preferences(self, preferences: NotificationPreferenceDB) -> NotificationPreferenceDB:
        """Create or update notification preferences."""
        try:
            preferences.updated_at = datetime.utcnow()
            result = await self.db.notification_preferences.find_one_and_update(
                {"customer_id": preferences.customer_id},
                {"$set": preferences.dict(exclude={"id"})},
                upsert=True,
                return_document=True
            )
            return NotificationPreferenceDB(**result)
        except Exception as e:
            logger.error(f"Error upserting notification preferences for customer {preferences.customer_id}: {e}")
            raise

    async def register_push_token(self, token: PushTokenDB) -> PushTokenDB:
        """Register a new push notification token."""
        try:
            result = await self.db.push_tokens.find_one_and_update(
                {"customer_id": token.customer_id, "token": token.token},
                {"$set": token.dict(exclude={"id"})},
                upsert=True,
                return_document=True
            )
            return PushTokenDB(**result)
        except Exception as e:
            logger.error(f"Error registering push token for customer {token.customer_id}: {e}")
            raise

    async def unregister_push_token(self, customer_id: str, token: str) -> bool:
        """Unregister a push notification token."""
        try:
            result = await self.db.push_tokens.update_one(
                {"customer_id": customer_id, "token": token},
                {"$set": {"is_active": False}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error unregistering push token for customer {customer_id}: {e}")
            raise

    async def log_notification(self, log: NotificationLogDB) -> NotificationLogDB:
        """Log a notification attempt."""
        try:
            result = await self.db.notification_logs.insert_one(log.dict(exclude={"id"}))
            log.id = str(result.inserted_id)
            return log
        except Exception as e:
            logger.error(f"Error logging notification for customer {log.customer_id}: {e}")
            raise

    async def update_notification_status(self, log_id: str, status: str, error: Optional[str] = None) -> bool:
        """Update the status of a sent notification."""
        try:
            update = {
                "$set": {
                    "status": status,
                    "delivered_at": datetime.utcnow() if status == "delivered" else None
                }
            }
            if error:
                update["$set"]["error"] = error

            result = await self.db.notification_logs.update_one(
                {"_id": ObjectId(log_id)},
                update
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating notification status for log {log_id}: {e}")
            raise

    async def get_active_push_tokens(self, customer_id: str) -> List[PushTokenDB]:
        """Get all active push tokens for a customer."""
        try:
            cursor = self.db.push_tokens.find({
                "customer_id": customer_id,
                "is_active": True
            })
            return [PushTokenDB(**token) async for token in cursor]
        except Exception as e:
            logger.error(f"Error getting active push tokens for customer {customer_id}: {e}")
            raise 