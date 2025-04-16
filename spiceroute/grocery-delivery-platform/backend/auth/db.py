from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional
from .models import StoreOwnerCreate, StoreOwnerInDB, StoreOwnerInvite
from config import settings
import secrets
from pymongo import IndexModel, ASCENDING, TEXT
import os

class StoreOwnerDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.store_owners = self.db.store_owners
        self.invites = self.db.store_owner_invites

    async def create_store_owner(self, store_owner: StoreOwnerCreate) -> StoreOwnerInDB:
        store_owner_dict = store_owner.dict()
        store_owner_dict["created_at"] = datetime.utcnow()
        store_owner_dict["updated_at"] = datetime.utcnow()
        
        result = await self.store_owners.insert_one(store_owner_dict)
        store_owner_dict["id"] = str(result.inserted_id)
        
        return StoreOwnerInDB(**store_owner_dict)

    async def get_store_owner_by_email(self, email: str) -> Optional[StoreOwnerInDB]:
        store_owner = await self.store_owners.find_one({"email": email})
        if store_owner:
            store_owner["id"] = str(store_owner["_id"])
            return StoreOwnerInDB(**store_owner)
        return None

    async def get_store_owner_by_oauth_id(self, provider: str, oauth_id: str) -> Optional[StoreOwnerInDB]:
        store_owner = await self.store_owners.find_one({
            "oauth_provider": provider,
            "oauth_id": oauth_id
        })
        if store_owner:
            store_owner["id"] = str(store_owner["_id"])
            return StoreOwnerInDB(**store_owner)
        return None

    async def create_invite(self, email: str, invited_by: str) -> StoreOwnerInvite:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        invite = StoreOwnerInvite(
            email=email,
            invited_by=invited_by,
            expires_at=expires_at,
            token=token,
            is_used=False
        )
        
        await self.invites.insert_one(invite.dict())
        return invite

    async def get_invite_by_token(self, token: str) -> Optional[StoreOwnerInvite]:
        invite = await self.invites.find_one({"token": token})
        if invite:
            return StoreOwnerInvite(**invite)
        return None

    async def mark_invite_as_used(self, token: str):
        await self.invites.update_one(
            {"token": token},
            {"$set": {"is_used": True}}
        )

    async def update_store_owner(self, email: str, update_data: dict):
        update_data["updated_at"] = datetime.utcnow()
        await self.store_owners.update_one(
            {"email": email},
            {"$set": update_data}
        )

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.spiceroute

# Collections
users = db.users
stores = db.stores

# Create indexes
async def create_indexes():
    # User indexes
    await users.create_indexes([
        IndexModel([("email", ASCENDING)], unique=True),
        IndexModel([("user_id", ASCENDING)], unique=True),
        IndexModel([("contract_id", ASCENDING)], unique=True),
        IndexModel([("phone_number", ASCENDING)], unique=True),
        IndexModel([("first_name", TEXT), ("last_name", TEXT)]),
        IndexModel([("customer_desc", TEXT)]),
        IndexModel([("store_id", ASCENDING)])
    ])
    
    # Store indexes
    await stores.create_indexes([
        IndexModel([("store_id", ASCENDING)], unique=True),
        IndexModel([("name", TEXT)])
    ])

# User operations
async def get_user_by_email(email: str) -> Optional[dict]:
    return await users.find_one({"email": email})

async def get_user_by_id(user_id: str) -> Optional[dict]:
    return await users.find_one({"user_id": user_id})

async def create_user(user_data: dict) -> dict:
    result = await users.insert_one(user_data)
    return await get_user_by_id(user_data["user_id"])

async def update_user(user_id: str, update_data: dict) -> Optional[dict]:
    await users.update_one({"user_id": user_id}, {"$set": update_data})
    return await get_user_by_id(user_id)

# Store operations
async def get_store_by_id(store_id: str) -> Optional[dict]:
    return await stores.find_one({"store_id": store_id})

async def create_store(store_data: dict) -> dict:
    result = await stores.insert_one(store_data)
    return await get_store_by_id(store_data["store_id"])

async def update_store(store_id: str, update_data: dict) -> Optional[dict]:
    await stores.update_one({"store_id": store_id}, {"$set": update_data})
    return await get_store_by_id(store_id)

store_owner_db = StoreOwnerDB() 