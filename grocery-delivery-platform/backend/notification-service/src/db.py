from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
import logging
from .models import (
    NotificationTemplate,
    NotificationPreference,
    Campaign,
    Notification,
    UserSegment,
    NotificationType
)

logger = logging.getLogger(__name__)

class NotificationDatabaseService:
    def __init__(self, mongodb_url: str, database_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db: AsyncIOMotorDatabase = self.client[database_name]
        
    async def init_indexes(self):
        """Initialize database indexes."""
        try:
            # Templates collection indexes
            await self.db.templates.create_index("name", unique=True)
            await self.db.templates.create_index("type")
            
            # Preferences collection indexes
            await self.db.preferences.create_index("user_id", unique=True)
            
            # Campaigns collection indexes
            await self.db.campaigns.create_index("name")
            await self.db.campaigns.create_index("status")
            await self.db.campaigns.create_index("template_id")
            
            # Notifications collection indexes
            await self.db.notifications.create_index([("user_id", 1), ("created_at", -1)])
            await self.db.notifications.create_index("campaign_id")
            await self.db.notifications.create_index("status")
            await self.db.notifications.create_index("type")
            await self.db.notifications.create_index("created_at")
            
            # Segments collection indexes
            await self.db.segments.create_index("name", unique=True)
            
            logger.info("Successfully initialized notification database indexes")
        except Exception as e:
            logger.error(f"Error initializing notification database indexes: {e}")
            raise

    # Template operations
    async def create_template(self, template: NotificationTemplate) -> NotificationTemplate:
        """Create a new notification template."""
        try:
            result = await self.db.templates.insert_one(template.dict(exclude={"id"}))
            template.id = str(result.inserted_id)
            return template
        except Exception as e:
            logger.error(f"Error creating template: {e}")
            raise

    async def get_template(self, template_id: str) -> Optional[NotificationTemplate]:
        """Get a template by ID."""
        try:
            result = await self.db.templates.find_one({"_id": ObjectId(template_id)})
            return NotificationTemplate(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting template: {e}")
            raise

    # Campaign operations
    async def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create a new notification campaign."""
        try:
            result = await self.db.campaigns.insert_one(campaign.dict(exclude={"id"}))
            campaign.id = str(result.inserted_id)
            return campaign
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            raise

    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get a campaign by ID."""
        try:
            result = await self.db.campaigns.find_one({"_id": ObjectId(campaign_id)})
            return Campaign(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting campaign: {e}")
            raise

    async def update_campaign(self, campaign: Campaign) -> Campaign:
        """Update a campaign."""
        try:
            await self.db.campaigns.update_one(
                {"_id": ObjectId(campaign.id)},
                {"$set": campaign.dict(exclude={"id"})}
            )
            return campaign
        except Exception as e:
            logger.error(f"Error updating campaign: {e}")
            raise

    # Notification operations
    async def create_notification(self, notification: Notification) -> Notification:
        """Create a new notification."""
        try:
            result = await self.db.notifications.insert_one(notification.dict(exclude={"id"}))
            notification.id = str(result.inserted_id)
            return notification
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise

    async def get_notification(self, notification_id: str) -> Optional[Notification]:
        """Get a notification by ID."""
        try:
            result = await self.db.notifications.find_one({"_id": ObjectId(notification_id)})
            return Notification(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting notification: {e}")
            raise

    async def update_notification(self, notification: Notification) -> Notification:
        """Update a notification."""
        try:
            await self.db.notifications.update_one(
                {"_id": ObjectId(notification.id)},
                {"$set": notification.dict(exclude={"id"})}
            )
            return notification
        except Exception as e:
            logger.error(f"Error updating notification: {e}")
            raise

    async def get_recent_notification_count(
        self,
        user_id: str,
        notification_type: NotificationType,
        hours: int = 24
    ) -> int:
        """Get count of recent notifications for rate limiting."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            count = await self.db.notifications.count_documents({
                "user_id": user_id,
                "type": notification_type,
                "created_at": {"$gte": cutoff_time}
            })
            return count
        except Exception as e:
            logger.error(f"Error getting notification count: {e}")
            raise

    # User segment operations
    async def create_segment(self, segment: UserSegment) -> UserSegment:
        """Create a new user segment."""
        try:
            result = await self.db.segments.insert_one(segment.dict(exclude={"id"}))
            segment.id = str(result.inserted_id)
            return segment
        except Exception as e:
            logger.error(f"Error creating segment: {e}")
            raise

    async def get_segment(self, segment_id: str) -> Optional[UserSegment]:
        """Get a segment by ID."""
        try:
            result = await self.db.segments.find_one({"_id": ObjectId(segment_id)})
            return UserSegment(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting segment: {e}")
            raise

    async def get_users_by_segment(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get users matching segment criteria."""
        try:
            # This would typically query your user service or user collection
            # For now, we'll return an empty list
            return []
        except Exception as e:
            logger.error(f"Error getting users by segment: {e}")
            raise

    # Preference operations
    async def get_preferences(self, user_id: str) -> Optional[NotificationPreference]:
        """Get notification preferences for a user."""
        try:
            result = await self.db.preferences.find_one({"user_id": user_id})
            return NotificationPreference(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting preferences: {e}")
            raise

    async def update_preferences(self, preferences: NotificationPreference) -> NotificationPreference:
        """Update notification preferences."""
        try:
            preferences.updated_at = datetime.utcnow()
            await self.db.preferences.update_one(
                {"user_id": preferences.user_id},
                {"$set": preferences.dict(exclude={"id"})},
                upsert=True
            )
            return preferences
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
            raise

    async def get_all_active_users(self) -> List[Dict[str, Any]]:
        """Get all active users."""
        try:
            # This would typically query your user service or user collection
            # For now, we'll return an empty list
            return []
        except Exception as e:
            logger.error(f"Error getting active users: {e}")
            raise 