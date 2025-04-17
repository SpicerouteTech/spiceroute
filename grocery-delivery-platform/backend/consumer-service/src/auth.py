from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta
from .models import Consumer, Token, TokenData
from .db import db
from .oauth import oauth_service
from .token import token_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    async def authenticate_google(self, token: str) -> Token:
        """Authenticate consumer with Google token"""
        # Verify Google token
        google_user = await oauth_service.verify_google_token(token)
        if not google_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
            )

        # Check if consumer exists
        consumer = await db.get_consumer_by_oauth(
            google_user["sub"], "google"
        )
        
        if not consumer:
            # Create new consumer
            consumer = Consumer(
                email=google_user["email"],
                oauth_id=google_user["sub"],
                oauth_provider="google",
                name=google_user.get("name", ""),
                picture=google_user.get("picture", ""),
            )
            await db.create_consumer(consumer)
        else:
            # Update last login
            await db.update_last_login(consumer.email)

        # Create access token
        access_token = token_service.create_access_token(
            data={"sub": consumer.email, "type": "consumer"},
            expires_delta=timedelta(minutes=30)
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutes in seconds
        )

    async def authenticate_facebook(self, token: str) -> Token:
        """Authenticate consumer with Facebook token"""
        # Verify Facebook token
        facebook_user = await oauth_service.verify_facebook_token(token)
        if not facebook_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Facebook token",
            )

        # Check if consumer exists
        consumer = await db.get_consumer_by_oauth(
            facebook_user["id"], "facebook"
        )
        
        if not consumer:
            # Create new consumer
            consumer = Consumer(
                email=facebook_user["email"],
                oauth_id=facebook_user["id"],
                oauth_provider="facebook",
                name=facebook_user.get("name", ""),
                picture=facebook_user.get("picture", {}).get("data", {}).get("url", ""),
            )
            await db.create_consumer(consumer)
        else:
            # Update last login
            await db.update_last_login(consumer.email)

        # Create access token
        access_token = token_service.create_access_token(
            data={"sub": consumer.email, "type": "consumer"},
            expires_delta=timedelta(minutes=30)
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutes in seconds
        )

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Consumer:
        """Get current authenticated consumer"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = token_service.verify_token(token)
            email: str = payload.get("sub")
            user_type: str = payload.get("type")
            
            if email is None or user_type != "consumer":
                raise credentials_exception
                
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
            
        consumer = await db.get_consumer_by_email(token_data.email)
        if consumer is None:
            raise credentials_exception
            
        return consumer

# Global auth service instance
auth_service = AuthService() 