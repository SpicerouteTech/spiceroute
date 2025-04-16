from fastapi import HTTPException, status
import httpx
from typing import Optional, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class OAuthService:
    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.facebook_app_id = os.getenv("FACEBOOK_APP_ID")
        self.facebook_app_secret = os.getenv("FACEBOOK_APP_SECRET")

    async def verify_google_token(self, token: str) -> Dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
                )
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Google token"
                    )
                
                data = response.json()
                if data["aud"] != self.google_client_id:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid client ID"
                    )
                
                return {
                    "email": data["email"],
                    "name": data["name"],
                    "oauth_id": data["sub"],
                    "provider": "google"
                }
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e)
                )

    async def verify_facebook_token(self, token: str) -> Dict:
        async with httpx.AsyncClient() as client:
            try:
                # First verify the token
                verify_response = await client.get(
                    f"https://graph.facebook.com/debug_token",
                    params={
                        "input_token": token,
                        "access_token": f"{self.facebook_app_id}|{self.facebook_app_secret}"
                    }
                )
                
                if verify_response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Facebook token"
                    )
                
                verify_data = verify_response.json()
                if not verify_data["data"]["is_valid"]:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Facebook token"
                    )
                
                # Get user info
                user_response = await client.get(
                    f"https://graph.facebook.com/me",
                    params={
                        "fields": "id,name,email",
                        "access_token": token
                    }
                )
                
                if user_response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not fetch user info"
                    )
                
                user_data = user_response.json()
                return {
                    "email": user_data["email"],
                    "name": user_data["name"],
                    "oauth_id": user_data["id"],
                    "provider": "facebook"
                }
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e)
                )

oauth_service = OAuthService() 