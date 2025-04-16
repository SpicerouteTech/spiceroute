from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta
from .models import StoreOwner, Token, TokenData
from .db import store_owner_db
from .oauth import oauth_service
from .token import token_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    async def authenticate_google(self, token: str) -> Token:
        # Verify Google token
        google_user = await oauth_service.verify_google_token(token)
        if not google_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
            )

        # Check if user exists
        store_owner = await store_owner_db.get_store_owner_by_oauth_id(
            google_user["sub"], "google"
        )
        
        if not store_owner:
            # Create new store owner
            store_owner = StoreOwner(
                email=google_user["email"],
                oauth_id=google_user["sub"],
                oauth_provider="google",
                name=google_user.get("name", ""),
                picture=google_user.get("picture", ""),
            )
            await store_owner_db.create_store_owner(store_owner)
        else:
            # Update last login
            await store_owner_db.update_last_login(store_owner.email)

        # Create access token
        access_token = token_service.create_access_token(
            data={"sub": store_owner.email},
            expires_delta=timedelta(minutes=30)
        )
        
        return Token(access_token=access_token, token_type="bearer")

    async def authenticate_facebook(self, token: str) -> Token:
        # Verify Facebook token
        facebook_user = await oauth_service.verify_facebook_token(token)
        if not facebook_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Facebook token",
            )

        # Check if user exists
        store_owner = await store_owner_db.get_store_owner_by_oauth_id(
            facebook_user["id"], "facebook"
        )
        
        if not store_owner:
            # Create new store owner
            store_owner = StoreOwner(
                email=facebook_user["email"],
                oauth_id=facebook_user["id"],
                oauth_provider="facebook",
                name=facebook_user.get("name", ""),
                picture=facebook_user.get("picture", {}).get("data", {}).get("url", ""),
            )
            await store_owner_db.create_store_owner(store_owner)
        else:
            # Update last login
            await store_owner_db.update_last_login(store_owner.email)

        # Create access token
        access_token = token_service.create_access_token(
            data={"sub": store_owner.email},
            expires_delta=timedelta(minutes=30)
        )
        
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> StoreOwner:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = token_service.verify_token(token)
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
            
        store_owner = await store_owner_db.get_store_owner_by_email(token_data.email)
        if store_owner is None:
            raise credentials_exception
        return store_owner

auth_service = AuthService() 