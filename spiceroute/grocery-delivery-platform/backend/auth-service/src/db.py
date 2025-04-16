from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError, OperationFailure
from .models import StoreOwner
from .logging_service import logger

load_dotenv()

class DatabaseService:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
        self.db = self.client.spiceroute
        self.store_owners = self.db.store_owners

    async def setup_indexes(self):
        """Setup database indexes"""
        try:
            # Create unique indexes
            await self.store_owners.create_index("email", unique=True)
            await self.store_owners.create_index([("oauth_provider", 1), ("oauth_id", 1)], unique=True)
            
            # Create regular indexes for frequent queries
            await self.store_owners.create_index("created_at")
            await self.store_owners.create_index("last_login")
            
            await logger.log("INFO", "Database indexes created successfully")
        except OperationFailure as e:
            await logger.log("ERROR", "Failed to create database indexes", {"error": str(e)})
            raise

    async def get_store_owner_by_email(self, email: str) -> StoreOwner:
        """Get store owner by email with error handling"""
        try:
            document = await self.store_owners.find_one({"email": email})
            if document:
                return StoreOwner(**document)
            return None
        except Exception as e:
            await logger.log("ERROR", f"Error fetching store owner by email: {email}", {"error": str(e)})
            raise

    async def get_store_owner_by_oauth(self, oauth_id: str, provider: str) -> StoreOwner:
        """Get store owner by OAuth ID and provider"""
        try:
            document = await self.store_owners.find_one({
                "oauth_id": oauth_id,
                "oauth_provider": provider
            })
            if document:
                return StoreOwner(**document)
            return None
        except Exception as e:
            await logger.log("ERROR", "Error fetching store owner by OAuth", {
                "oauth_id": oauth_id,
                "provider": provider,
                "error": str(e)
            })
            raise

    async def create_store_owner(self, store_owner: StoreOwner) -> StoreOwner:
        """Create new store owner with duplicate checking"""
        try:
            document = store_owner.dict()
            await self.store_owners.insert_one(document)
            await logger.log("INFO", f"Created new store owner: {store_owner.email}")
            return store_owner
        except DuplicateKeyError:
            await logger.log("WARNING", f"Duplicate store owner: {store_owner.email}")
            raise ValueError("Store owner already exists")
        except Exception as e:
            await logger.log("ERROR", "Error creating store owner", {
                "email": store_owner.email,
                "error": str(e)
            })
            raise

    async def update_last_login(self, email: str) -> bool:
        """Update store owner's last login time"""
        try:
            result = await self.store_owners.update_one(
                {"email": email},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            if result.modified_count:
                await logger.log("INFO", f"Updated last login for: {email}")
                return True
            await logger.log("WARNING", f"No store owner found to update login: {email}")
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error updating last login for: {email}", {"error": str(e)})
            raise

    async def close(self):
        """Close database connection"""
        self.client.close()

# Global database service instance
db = DatabaseService() 