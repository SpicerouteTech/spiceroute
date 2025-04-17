from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Dict, Any
from bson import ObjectId

from models import StoreOwnerProfile, StoreOwnerProfileUpdate
from db import store_profile_db

# Setup OAuth2 with Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter()


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Get the current user ID from the JWT token.
    In a production environment, this would validate the token with the auth service.
    """
    # For now, we'll just extract the user ID from the token payload
    # In a real implementation, this would decode and verify the JWT
    try:
        # Simulated extraction for now
        # In production, this would decode the JWT and validate it properly
        user_id = token.split("|")[1] if "|" in token else token
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/profiles", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: StoreOwnerProfile,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new store owner profile."""
    # Override the user_id to ensure it matches the authenticated user
    profile.user_id = user_id
    
    # Create the profile
    created_profile = await store_profile_db.create_profile(profile)
    return created_profile


@router.get("/profiles/me", response_model=Dict[str, Any])
async def get_my_profile(user_id: str = Depends(get_current_user_id)):
    """Get the profile of the current authenticated user."""
    profile = await store_profile_db.get_profile_by_user_id(user_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found for the current user"
        )
    
    return profile


@router.get("/profiles/{profile_id}", response_model=Dict[str, Any])
async def get_profile(
    profile_id: str = Path(..., description="The ID of the profile to get")
):
    """Get a store owner profile by ID."""
    profile = await store_profile_db.get_profile_by_id(profile_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID {profile_id} not found"
        )
    
    return profile


@router.put("/profiles/{profile_id}", response_model=Dict[str, Any])
async def update_profile(
    update_data: StoreOwnerProfileUpdate,
    profile_id: str = Path(..., description="The ID of the profile to update"),
    user_id: str = Depends(get_current_user_id)
):
    """Update a store owner profile."""
    # Get the current profile to check ownership
    current_profile = await store_profile_db.get_profile_by_id(profile_id)
    
    if not current_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID {profile_id} not found"
        )
    
    # Check if the authenticated user owns this profile
    if current_profile.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this profile"
        )
    
    # Update the profile
    updated_profile = await store_profile_db.update_profile(profile_id, update_data)
    return updated_profile


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: str = Path(..., description="The ID of the profile to delete"),
    user_id: str = Depends(get_current_user_id)
):
    """Delete a store owner profile."""
    # Get the current profile to check ownership
    current_profile = await store_profile_db.get_profile_by_id(profile_id)
    
    if not current_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID {profile_id} not found"
        )
    
    # Check if the authenticated user owns this profile
    if current_profile.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this profile"
        )
    
    # Delete the profile
    await store_profile_db.delete_profile(profile_id)


@router.get("/profiles", response_model=Dict[str, Any])
async def list_profiles(
    skip: int = Query(0, ge=0, description="Skip the first n results"),
    limit: int = Query(10, ge=1, le=100, description="Limit the number of results"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search term")
):
    """List store owner profiles with pagination and filtering."""
    if search:
        # If search term is provided, use text search
        return await store_profile_db.search_profiles(search, skip, limit)
    
    # Build filter based on query parameters
    filters = {}
    if category:
        filters["category"] = category
    
    # Use regular listing with optional filters
    return await store_profile_db.list_profiles(skip, limit, filters)


@router.get("/health", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "store-profile-service"} 