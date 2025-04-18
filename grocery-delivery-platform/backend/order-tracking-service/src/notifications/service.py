from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import aiohttp
import logging
from fastapi import HTTPException
from .providers import (
    EmailProvider,
    SMSProvider,
    WhatsAppProvider,
    PushNotificationProvider
)

logger = logging.getLogger(__name__)

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PUSH = "push"

class NotificationPreference(BaseModel):
    customer_id: str
    channels: List[NotificationChannel]
    email: Optional[str]
    phone: Optional[str]
    push_tokens: Optional[List[str]]
    whatsapp_opted_in: Optional[bool] = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class NotificationService:
    def __init__(self):
        # Initialize notification providers
        self.email_provider = EmailProvider()
        self.sms_provider = SMSProvider()
        self.whatsapp_provider = WhatsAppProvider()
        self.push_provider = PushNotificationProvider()

    async def send_order_status_notification(
        self,
        customer_id: str,
        order_id: str,
        status: str,
        preferences: NotificationPreference,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send notifications through all preferred channels."""
        results = {}
        errors = []

        # Prepare notification content
        content = self._prepare_notification_content(status, additional_data)

        for channel in preferences.channels:
            try:
                if channel == NotificationChannel.EMAIL and preferences.email:
                    result = await self.email_provider.send(
                        to_email=preferences.email,
                        subject=f"Order {order_id} Update",
                        content=content["email"]
                    )
                    results["email"] = result

                elif channel == NotificationChannel.SMS and preferences.phone:
                    result = await self.sms_provider.send(
                        to_phone=preferences.phone,
                        message=content["sms"]
                    )
                    results["sms"] = result

                elif channel == NotificationChannel.WHATSAPP and preferences.whatsapp_opted_in:
                    result = await self.whatsapp_provider.send(
                        to_phone=preferences.phone,
                        message=content["whatsapp"]
                    )
                    results["whatsapp"] = result

                elif channel == NotificationChannel.PUSH and preferences.push_tokens:
                    result = await self.push_provider.send(
                        tokens=preferences.push_tokens,
                        title=content["push"]["title"],
                        body=content["push"]["body"],
                        data={"order_id": order_id, "status": status}
                    )
                    results["push"] = result

            except Exception as e:
                logger.error(f"Error sending {channel} notification: {str(e)}")
                errors.append({"channel": channel, "error": str(e)})

        return {
            "success": len(results) > 0,
            "results": results,
            "errors": errors
        }

    def _prepare_notification_content(
        self,
        status: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Prepare notification content for different channels."""
        data = additional_data or {}
        store_name = data.get("store_name", "the store")
        eta = data.get("eta", "")
        driver_name = data.get("driver_name", "your delivery partner")

        templates = {
            "SUBMITTED": {
                "title": "Order Received",
                "message": f"Your order has been received and sent to {store_name}."
            },
            "STORE_ACKNOWLEDGED": {
                "title": "Order Confirmed",
                "message": f"{store_name} has confirmed your order and will start preparing it soon."
            },
            "PICKING_IN_PROGRESS": {
                "title": "Order Preparation Started",
                "message": f"{store_name} has started preparing your order."
            },
            "SUBSTITUTIONS_NEEDED": {
                "title": "Substitutions Required",
                "message": "Some items in your order need substitution. Please check the app to approve or reject."
            },
            "READY_FOR_PICKUP": {
                "title": "Order Ready",
                "message": "Your order is ready and waiting for pickup."
            },
            "DRIVER_ASSIGNED": {
                "title": "Driver Assigned",
                "message": f"{driver_name} will be delivering your order."
            },
            "DRIVER_PICKUP_COMPLETE": {
                "title": "Order Picked Up",
                "message": f"Your order is on its way! Estimated delivery time: {eta}"
            },
            "DELIVERED": {
                "title": "Order Delivered",
                "message": "Your order has been delivered. Enjoy!"
            }
        }

        template = templates.get(status, {
            "title": "Order Update",
            "message": f"Your order status has been updated to {status}"
        })

        return {
            "email": self._format_email_content(template, data),
            "sms": self._format_sms_content(template, data),
            "whatsapp": self._format_whatsapp_content(template, data),
            "push": {
                "title": template["title"],
                "body": template["message"]
            }
        }

    def _format_email_content(
        self,
        template: Dict[str, str],
        data: Dict[str, Any]
    ) -> str:
        """Format email content with HTML template."""
        return f"""
        <h2>{template['title']}</h2>
        <p>{template['message']}</p>
        {self._format_additional_info(data)}
        """

    def _format_sms_content(
        self,
        template: Dict[str, str],
        data: Dict[str, Any]
    ) -> str:
        """Format SMS content with character limit."""
        return f"{template['title']}: {template['message']}"

    def _format_whatsapp_content(
        self,
        template: Dict[str, str],
        data: Dict[str, Any]
    ) -> str:
        """Format WhatsApp content with markdown support."""
        return f"*{template['title']}*\n\n{template['message']}"

    def _format_additional_info(self, data: Dict[str, Any]) -> str:
        """Format additional information for email notifications."""
        info = []
        if "order_total" in data:
            info.append(f"<p>Order Total: ${data['order_total']:.2f}</p>")
        if "eta" in data:
            info.append(f"<p>Estimated Delivery Time: {data['eta']}</p>")
        if "driver_name" in data and "driver_phone" in data:
            info.append(
                f"<p>Driver: {data['driver_name']} "
                f"(Phone: {data['driver_phone']})</p>"
            )
        return "\n".join(info) 