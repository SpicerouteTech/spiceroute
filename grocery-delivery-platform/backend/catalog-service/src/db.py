import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import CatalogItem, CatalogItemUpdate, PaginatedResponse
import pymongo
from fastapi import HTTPException, status


logger = logging.getLogger(__name__)

# MongoDB setup
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "spiceroute")
COLLECTION_NAME = "catalog_items"


class CatalogDB:
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
        # Index for store_id to quickly find all items for a specific store
        await db[COLLECTION_NAME].create_index([("store_id", pymongo.ASCENDING)])
        # Text index for name and description for search functionality
        await db[COLLECTION_NAME].create_index([("name", pymongo.TEXT), ("description", pymongo.TEXT)])
        # Index for categories and tags for filtering
        await db[COLLECTION_NAME].create_index([("category", pymongo.ASCENDING)])
        await db[COLLECTION_NAME].create_index([("tags", pymongo.ASCENDING)])
        # Index for sorting by price
        await db[COLLECTION_NAME].create_index([("price", pymongo.ASCENDING)])
        # Index for finding featured items
        await db[COLLECTION_NAME].create_index([("featured", pymongo.DESCENDING)])
    
    async def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a catalog item by its ID."""
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid item ID format: {item_id}"
            )
        
        db = self.client[DB_NAME]
        item = await db[COLLECTION_NAME].find_one({"_id": ObjectId(item_id)})
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
            
        return item
    
    async def create_item(self, item_data: CatalogItem) -> Dict[str, Any]:
        """Create a new catalog item."""
        db = self.client[DB_NAME]
        item_dict = item_data.dict(by_alias=True)
        
        # Insert the new item
        result = await db[COLLECTION_NAME].insert_one(item_dict)
        
        # Get the newly created item
        new_item = await db[COLLECTION_NAME].find_one({"_id": result.inserted_id})
        return new_item
    
    async def update_item(self, item_id: str, update_data: CatalogItemUpdate) -> Dict[str, Any]:
        """Update an existing catalog item."""
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid item ID format: {item_id}"
            )
        
        db = self.client[DB_NAME]
        
        # Exclude None values (don't update fields that weren't provided)
        update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
        
        if not update_dict:
            # No valid fields to update
            return await self.get_item_by_id(item_id)
        
        # Add updated_at timestamp
        update_dict["updated_at"] = datetime.utcnow()
        
        # Use the $set operator to update only the fields provided
        result = await db[COLLECTION_NAME].update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        return await self.get_item_by_id(item_id)
    
    async def delete_item(self, item_id: str) -> bool:
        """Delete a catalog item by its ID."""
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid item ID format: {item_id}"
            )
        
        db = self.client[DB_NAME]
        result = await db[COLLECTION_NAME].delete_one({"_id": ObjectId(item_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        return True
    
    async def list_items(self, skip: int = 0, limit: int = 20, 
                        filters: Dict[str, Any] = None,
                        sort_by: str = "created_at",
                        sort_desc: bool = True) -> PaginatedResponse:
        """List catalog items with pagination, filtering and sorting."""
        db = self.client[DB_NAME]
        query = filters or {}
        
        # Get total count for pagination
        total = await db[COLLECTION_NAME].count_documents(query)
        
        # Sort direction
        sort_direction = pymongo.DESCENDING if sort_desc else pymongo.ASCENDING
        
        # Get paginated results
        cursor = db[COLLECTION_NAME].find(query).sort(sort_by, sort_direction).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        
        return PaginatedResponse(
            total=total,
            page=skip // limit + 1,
            limit=limit,
            items=items
        )
    
    async def get_store_items(self, store_id: str, skip: int = 0, limit: int = 20,
                             filters: Dict[str, Any] = None,
                             sort_by: str = "created_at",
                             sort_desc: bool = True) -> PaginatedResponse:
        """Get all items for a specific store with pagination, filtering and sorting."""
        if not ObjectId.is_valid(store_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid store ID format: {store_id}"
            )
        
        # Build filter
        query = filters or {}
        query["store_id"] = ObjectId(store_id)
        
        return await self.list_items(skip, limit, query, sort_by, sort_desc)
    
    async def search_items(self, query_text: str, store_id: Optional[str] = None,
                          skip: int = 0, limit: int = 20) -> PaginatedResponse:
        """Search catalog items by text with optional store filter."""
        db = self.client[DB_NAME]
        
        # Build query
        search_query = {"$text": {"$search": query_text}}
        
        # Add store filter if provided
        if store_id:
            if not ObjectId.is_valid(store_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"Invalid store ID format: {store_id}"
                )
            search_query["store_id"] = ObjectId(store_id)
        
        # Get total count for pagination
        total = await db[COLLECTION_NAME].count_documents(search_query)
        
        # Get paginated results with relevance sorting
        cursor = db[COLLECTION_NAME].find(
            search_query,
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).skip(skip).limit(limit)
        
        items = await cursor.to_list(length=limit)
        
        return PaginatedResponse(
            total=total,
            page=skip // limit + 1,
            limit=limit,
            items=items
        )
    
    async def get_featured_items(self, store_id: Optional[str] = None, 
                                limit: int = 10) -> List[Dict[str, Any]]:
        """Get featured items, optionally filtered by store."""
        db = self.client[DB_NAME]
        
        # Build query
        query = {"featured": True}
        
        # Add store filter if provided
        if store_id:
            if not ObjectId.is_valid(store_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"Invalid store ID format: {store_id}"
                )
            query["store_id"] = ObjectId(store_id)
        
        # Get featured items
        cursor = db[COLLECTION_NAME].find(query).limit(limit)
        items = await cursor.to_list(length=limit)
        
        return items
    
    async def update_stock(self, item_id: str, quantity_change: int) -> Dict[str, Any]:
        """Update stock quantity for an item (increase or decrease)."""
        if not ObjectId.is_valid(item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid item ID format: {item_id}"
            )
        
        db = self.client[DB_NAME]
        
        # Use the $inc operator to atomically update the stock quantity
        result = await db[COLLECTION_NAME].update_one(
            {"_id": ObjectId(item_id)},
            {
                "$inc": {"stock_quantity": quantity_change},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        # Check if stock went negative and fix it
        await db[COLLECTION_NAME].update_one(
            {"_id": ObjectId(item_id), "stock_quantity": {"$lt": 0}},
            {"$set": {"stock_quantity": 0}}
        )
        
        # Return the updated item
        return await self.get_item_by_id(item_id)


# Create a singleton instance
catalog_db = CatalogDB() 