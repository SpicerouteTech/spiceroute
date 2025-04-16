from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException
from config import settings

class OAuthService:
    @staticmethod
    async def get_google_user_info(access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid Google token")
            return response.json()

    @staticmethod
    async def get_facebook_user_info(access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.facebook.com/me?fields=id,email,name,picture&access_token={access_token}"
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid Facebook token")
            return response.json()

    @staticmethod
    async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            return await OAuthService.get_google_user_info(token)
        except Exception:
            return None

    @staticmethod
    async def verify_facebook_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            return await OAuthService.get_facebook_user_info(token)
        except Exception:
            return None

    @staticmethod
    def get_google_auth_url() -> str:
        return (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
            "response_type=code&"
            "scope=email profile&"
            "access_type=offline&"
            "prompt=consent"
        )

    @staticmethod
    def get_facebook_auth_url() -> str:
        return (
            "https://www.facebook.com/v12.0/dialog/oauth?"
            f"client_id={settings.FACEBOOK_CLIENT_ID}&"
            f"redirect_uri={settings.FACEBOOK_REDIRECT_URI}&"
            "scope=email,public_profile"
        ) 