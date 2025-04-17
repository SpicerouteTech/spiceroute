import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import StoreOwnerProfile, StoreOwnerProfileUpdate
import pymongo
from fastapi import HTTPException, status


logger = logging.getLogger(__name__)

# MongoDB setup
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "spiceroute")
COLLECTION_NAME = "store_profiles"


class StoreProfileDB:
    client: AsyncIOMotorClient = None
    
    async def connect_to_mongodb(self):
        """Connect to MongoDB database."""
        logger.info(f"Connecting to MongoDB at {MONGODB_URL}")
        self.client = AsyncIOMotorClient(MONGODB_URL)
        await self.create_indexes()
        logger.info("Connected to MongoDB")
    
    async def close_mongodb_connection(self):
        """Close MongoDB connection."""
        if self.client is not None:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    async def create_indexes(self):
        """Create indexes for the collection."""
        db = self.client[DB_NAME]
        await db[COLLECTION_NAME].create_index([("user_id", pymongo.ASCENDING)], unique=True)
        await db[COLLECTION_NAME].create_index([("store_name", pymongo.TEXT)])
        await db[COLLECTION_NAME].create_index([("email", pymongo.ASCENDING)])
        await db[COLLECTION_NAME].create_index([("category", pymongo.ASCENDING)])
    
    async def get_profile_by_id(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Get a store profile by its ID."""
        if not ObjectId.is_valid(profile_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid profile ID format: {profile_id}"
            )
        
        db = self.client[DB_NAME]
        profile = await db[COLLECTION_NAME].find_one({"_id": ObjectId(profile_id)})
        return profile
    
    async def get_profile_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a store profile by user ID."""
        db = self.client[DB_NAME]
        profile = await db[COLLECTION_NAME].find_one({"user_id": user_id})
        return profile
    
    async def create_profile(self, profile_data: StoreOwnerProfile) -> Dict[str, Any]:
        """Create a new store profile."""
        db = self.client[DB_NAME]
        profile_dict = profile_data.dict(by_alias=True)
        
        # Check if a profile for this user_id already exists
        existing_profile = await db[COLLECTION_NAME].find_one({"user_id": profile_dict["user_id"]})
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A profile already exists for user_id: {profile_dict['user_id']}"
            )
        
        # Insert the new profile
        result = await db[COLLECTION_NAME].insert_one(profile_dict)
        
        # Get the newly created profile
        new_profile = await db[COLLECTION_NAME].find_one({"_id": result.inserted_id})
        return new_profile
    
    async def update_profile(self, profile_id: str, update_data: StoreOwnerProfileUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing store profile."""
        if not ObjectId.is_valid(profile_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid profile ID format: {profile_id}"
            )
        
        db = self.client[DB_NAME]
        
        # Exclude None values (don't update fields that weren't provided)
        update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
        
        if not update_dict:
            # No valid fields to update
            return await self.get_profile_by_id(profile_id)
        
        # Add updated_at timestamp
        update_dict["updated_at"] = datetime.utcnow()
        
        # Use the $set operator to update only the fields provided
        result = await db[COLLECTION_NAME].update_one(
            {"_id": ObjectId(profile_id)},
            {"$set": update_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile with ID {profile_id} not found"
            )
        
        return await self.get_profile_by_id(profile_id)
    
    async def delete_profile(self, profile_id: str) -> bool:
        """Delete a store profile by its ID."""
        if not ObjectId.is_valid(profile_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid profile ID format: {profile_id}"
            )
        
        db = self.client[DB_NAME]
        result = await db[COLLECTION_NAME].delete_one({"_id": ObjectId(profile_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile with ID {profile_id} not found"
            )
        
        return True
    
    async def list_profiles(self, skip: int = 0, limit: int = 10, 
                           filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """List store profiles with pagination and optional filtering."""
        db = self.client[DB_NAME]
        query = filters or {}
        
        # Get total count for pagination
        total = await db[COLLECTION_NAME].count_documents(query)
        
        # Get paginated results
        cursor = db[COLLECTION_NAME].find(query).skip(skip).limit(limit)
        profiles = await cursor.to_list(length=limit)
        
        return {
            "total": total,
            "page": skip // limit + 1,
            "limit": limit,
            "items": profiles
        }
    
    async def search_profiles(self, query: str, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """Search store profiles by text."""
        db = self.client[DB_NAME]
        
        # Use text search on indexed fields
        text_query = {"$text": {"$search": query}}
        
        # Get total count for pagination
        total = await db[COLLECTION_NAME].count_documents(text_query)
        
        # Get paginated results with relevance sorting
        cursor = db[COLLECTION_NAME].find(
            text_query,
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).skip(skip).limit(limit)
        
        profiles = await cursor.to_list(length=limit)
        
        return {
            "total": total,
            "page": skip // limit + 1,
            "limit": limit,
            "items": profiles
        }


# Create a singleton instance
store_profile_db = StoreProfileDB() 