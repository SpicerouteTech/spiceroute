from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
import jwt
from config import settings
from .models import StoreOwnerCreate, StoreOwnerInDB, StoreOwnerInvite
from .oauth import OAuthService

router = APIRouter(prefix="/auth/store-owner", tags=["store-owner-auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/google/login")
async def google_login():
    """Redirect to Google OAuth login page"""
    return {"url": OAuthService.get_google_auth_url()}

@router.get("/facebook/login")
async def facebook_login():
    """Redirect to Facebook OAuth login page"""
    return {"url": OAuthService.get_facebook_auth_url()}

@router.get("/google/callback")
async def google_callback(code: str):
    """Handle Google OAuth callback"""
    # Exchange code for token
    # Verify token and get user info
    # Check if user is invited
    # Create or update store owner
    # Return JWT token
    pass

@router.get("/facebook/callback")
async def facebook_callback(code: str):
    """Handle Facebook OAuth callback"""
    # Similar to Google callback
    pass

@router.post("/invite")
async def invite_store_owner(
    email: str,
    current_user: StoreOwnerInDB = Depends(get_current_user)
):
    """Invite a new store owner"""
    # Generate invite token
    # Send invitation email
    # Save invite to database
    pass

@router.get("/verify-invite/{token}")
async def verify_invite(token: str):
    """Verify store owner invitation"""
    # Check if invite is valid
    # Return invite details
    pass

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> StoreOwnerInDB:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    # Get user from database
    # Return StoreOwnerInDB
    pass 