from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .models import Token, StoreOwner
from .auth import auth_service

router = APIRouter()

@router.post("/auth/google", response_model=Token)
async def login_with_google(token: str):
    return await auth_service.authenticate_google(token)

@router.post("/auth/facebook", response_model=Token)
async def login_with_facebook(token: str):
    return await auth_service.authenticate_facebook(token)

@router.get("/me", response_model=StoreOwner)
async def get_current_user(current_user: StoreOwner = Depends(auth_service.get_current_user)):
    return current_user

@router.get("/health")
async def health_check():
    return {"status": "healthy"} 