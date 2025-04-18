from typing import List, Dict, Any, Optional
import aiohttp
import logging
from abc import ABC, abstractmethod
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class NotificationProvider(ABC):
    @abstractmethod
    async def send(self, **kwargs) -> Dict[str, Any]:
        pass

class EmailProvider(NotificationProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "YOUR_SENDGRID_API_KEY"
        self.base_url = "https://api.sendgrid.com/v3/mail/send"

    async def send(
        self,
        to_email: str,
        subject: str,
        content: str
    ) -> Dict[str, Any]:
        """Send email using SendGrid API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "personalizations": [{
                    "to": [{"email": to_email}]
                }],
                "from": {"email": "notifications@yourdomain.com"},
                "subject": subject,
                "content": [{
                    "type": "text/html",
                    "value": content
                }]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 202:
                        return {"status": "sent", "provider": "sendgrid"}
                    else:
                        error_data = await response.json()
                        raise HTTPException(
                            status_code=response.status,
                            detail=error_data
                        )
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            raise

class SMSProvider(NotificationProvider):
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None):
        self.account_sid = account_sid or "YOUR_TWILIO_ACCOUNT_SID"
        self.auth_token = auth_token or "YOUR_TWILIO_AUTH_TOKEN"
        self.from_number = "YOUR_TWILIO_NUMBER"
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"

    async def send(
        self,
        to_phone: str,
        message: str
    ) -> Dict[str, Any]:
        """Send SMS using Twilio API."""
        try:
            auth = aiohttp.BasicAuth(self.account_sid, self.auth_token)
            data = {
                "To": to_phone,
                "From": self.from_number,
                "Body": message
            }

            async with aiohttp.ClientSession(auth=auth) as session:
                async with session.post(self.base_url, data=data) as response:
                    if response.status == 201:
                        result = await response.json()
                        return {
                            "status": "sent",
                            "provider": "twilio",
                            "message_id": result["sid"]
                        }
                    else:
                        error_data = await response.json()
                        raise HTTPException(
                            status_code=response.status,
                            detail=error_data
                        )
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            raise

class WhatsAppProvider(NotificationProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "YOUR_META_API_KEY"
        self.base_url = "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"

    async def send(
        self,
        to_phone: str,
        message: str
    ) -> Dict[str, Any]:
        """Send WhatsApp message using Meta Cloud API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "text",
                "text": {"body": message}
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "status": "sent",
                            "provider": "meta",
                            "message_id": result["messages"][0]["id"]
                        }
                    else:
                        error_data = await response.json()
                        raise HTTPException(
                            status_code=response.status,
                            detail=error_data
                        )
        except Exception as e:
            logger.error(f"WhatsApp sending failed: {str(e)}")
            raise

class PushNotificationProvider(NotificationProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "YOUR_FIREBASE_API_KEY"
        self.base_url = "https://fcm.googleapis.com/fcm/send"

    async def send(
        self,
        tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send push notification using Firebase Cloud Messaging."""
        try:
            headers = {
                "Authorization": f"key={self.api_key}",
                "Content-Type": "application/json"
            }
            
            message = {
                "notification": {
                    "title": title,
                    "body": body
                },
                "data": data or {},
                "registration_ids": tokens
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=message
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "status": "sent",
                            "provider": "firebase",
                            "success_count": result["success"],
                            "failure_count": result["failure"]
                        }
                    else:
                        error_data = await response.json()
                        raise HTTPException(
                            status_code=response.status,
                            detail=error_data
                        )
        except Exception as e:
            logger.error(f"Push notification sending failed: {str(e)}")
            raise 