from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from fastapi import HTTPException
from .models import (
    NotificationType,
    NotificationChannel,
    NotificationStatus,
    NotificationPriority,
    NotificationTemplate,
    NotificationPreference,
    Campaign,
    Notification,
    UserSegment
)
from .providers import (
    EmailProvider,
    SMSProvider,
    WhatsAppProvider,
    PushNotificationProvider,
    WebPushProvider,
    InAppProvider
)
from .db import NotificationDatabaseService

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, db_service: NotificationDatabaseService):
        self.db = db_service
        # Initialize providers
        self.providers = {
            NotificationChannel.EMAIL: EmailProvider(),
            NotificationChannel.SMS: SMSProvider(),
            NotificationChannel.WHATSAPP: WhatsAppProvider(),
            NotificationChannel.PUSH: PushNotificationProvider(),
            NotificationChannel.WEB_PUSH: WebPushProvider(),
            NotificationChannel.IN_APP: InAppProvider()
        }

    async def create_template(self, template: NotificationTemplate) -> NotificationTemplate:
        """Create a new notification template."""
        return await self.db.create_template(template)

    async def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create a new notification campaign."""
        # Validate template exists
        template = await self.db.get_template(campaign.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        if campaign.segment_id:
            # Validate segment exists
            segment = await self.db.get_segment(campaign.segment_id)
            if not segment:
                raise HTTPException(status_code=404, detail="Segment not found")
        
        return await self.db.create_campaign(campaign)

    async def send_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Execute a notification campaign."""
        campaign = await self.db.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        template = await self.db.get_template(campaign.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Get target users
        users = []
        if campaign.segment_id:
            segment = await self.db.get_segment(campaign.segment_id)
            users = await self.db.get_users_by_segment(segment.criteria)
        else:
            users = await self.db.get_all_active_users()
        
        results = {
            "total": len(users),
            "sent": 0,
            "failed": 0,
            "skipped": 0
        }
        
        for user in users:
            try:
                prefs = await self.db.get_preferences(user.id)
                if not prefs or not self._should_send_notification(prefs, template.type):
                    results["skipped"] += 1
                    continue
                
                for channel in template.channels:
                    if channel in prefs.channels.get(template.type, []):
                        notification = Notification(
                            user_id=user.id,
                            type=template.type,
                            channel=channel,
                            template_id=template.id,
                            campaign_id=campaign_id,
                            content=self._render_template(template, channel, campaign.variables, user)
                        )
                        await self.send_notification(notification)
                        results["sent"] += 1
            except Exception as e:
                logger.error(f"Error sending campaign notification to user {user.id}: {str(e)}")
                results["failed"] += 1
        
        # Update campaign metrics
        campaign.metrics = results
        campaign.status = "completed"
        await self.db.update_campaign(campaign)
        
        return results

    async def send_notification(self, notification: Notification) -> Notification:
        """Send a single notification through specified channel."""
        try:
            provider = self.providers.get(notification.channel)
            if not provider:
                raise ValueError(f"No provider found for channel {notification.channel}")
            
            # Check rate limits and quiet hours
            if not await self._can_send_notification(notification):
                notification.status = NotificationStatus.FAILED
                notification.error = "Rate limit exceeded or quiet hours"
                return notification
            
            # Send notification
            result = await provider.send(notification)
            
            # Update notification status
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.utcnow()
            
            # Store notification
            stored_notification = await self.db.create_notification(notification)
            
            # Start delivery tracking if supported
            if hasattr(provider, 'track_delivery'):
                await provider.track_delivery(stored_notification.id)
            
            return stored_notification
            
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            notification.status = NotificationStatus.FAILED
            notification.error = str(e)
            return await self.db.create_notification(notification)

    async def update_notification_status(
        self,
        notification_id: str,
        status: NotificationStatus,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Update notification status and metadata."""
        notification = await self.db.get_notification(notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.status = status
        if status == NotificationStatus.DELIVERED:
            notification.delivered_at = datetime.utcnow()
        elif status == NotificationStatus.READ:
            notification.read_at = datetime.utcnow()
        
        if metadata:
            notification.metadata.update(metadata)
        
        return await self.db.update_notification(notification)

    async def create_user_segment(self, segment: UserSegment) -> UserSegment:
        """Create a new user segment for targeted notifications."""
        return await self.db.create_segment(segment)

    async def update_preferences(
        self,
        user_id: str,
        preferences: NotificationPreference
    ) -> NotificationPreference:
        """Update user notification preferences."""
        if preferences.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot modify preferences for another user"
            )
        return await self.db.update_preferences(preferences)

    def _should_send_notification(
        self,
        preferences: NotificationPreference,
        notification_type: NotificationType
    ) -> bool:
        """Check if notification should be sent based on user preferences."""
        # Check if user has opted out of marketing
        if notification_type == NotificationType.MARKETING and not preferences.marketing_opted_in:
            return False
        
        # Check if notification type is enabled
        if notification_type not in preferences.channels:
            return False
        
        return True

    async def _can_send_notification(self, notification: Notification) -> bool:
        """Check rate limits and quiet hours."""
        preferences = await self.db.get_preferences(notification.user_id)
        if not preferences:
            return True
        
        # Check quiet hours
        if preferences.quiet_hours and notification.priority != NotificationPriority.URGENT:
            current_hour = datetime.utcnow().strftime("%H:%M")
            if self._is_quiet_hour(current_hour, preferences.quiet_hours):
                return False
        
        # Check frequency limits
        if preferences.frequency_limits:
            limit = preferences.frequency_limits.get(notification.type)
            if limit:
                count = await self.db.get_recent_notification_count(
                    notification.user_id,
                    notification.type,
                    hours=24
                )
                if count >= limit:
                    return False
        
        return True

    def _is_quiet_hour(self, current_time: str, quiet_hours: Dict[str, str]) -> bool:
        """Check if current time is within quiet hours."""
        start = quiet_hours.get("start")
        end = quiet_hours.get("end")
        if not start or not end:
            return False
        
        # Handle overnight quiet hours
        if start > end:
            return current_time >= start or current_time <= end
        return start <= current_time <= end

    def _render_template(
        self,
        template: NotificationTemplate,
        channel: NotificationChannel,
        variables: Dict[str, Any],
        user: Any
    ) -> Dict[str, str]:
        """Render notification template with variables."""
        channel_template = template.templates.get(channel, {})
        rendered = {}
        
        for key, value in channel_template.items():
            # Replace variables in template
            content = value
            for var in template.variables:
                placeholder = f"{{{var}}}"
                if placeholder in content:
                    # Try to get value from campaign variables or user data
                    var_value = variables.get(var) or getattr(user, var, "")
                    content = content.replace(placeholder, str(var_value))
            rendered[key] = content
        
        return rendered 