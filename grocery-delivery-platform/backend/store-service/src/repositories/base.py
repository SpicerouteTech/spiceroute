from typing import Any, Dict, List, Optional, TypeVar, Generic
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from ..utils.errors import DatabaseError, ResourceNotFoundError
from ..utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository with common database operations"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def find_one(self, filter_query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document"""
        try:
            result = await self.collection.find_one(filter_query)
            return result
        except Exception as e:
            logger.error(f"Error finding document: {str(e)}")
            raise DatabaseError("find_one", {"error": str(e)})
    
    async def find_many(
        self,
        filter_query: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """Find multiple documents with pagination"""
        try:
            cursor = self.collection.find(filter_query).skip(skip).limit(limit)
            if sort:
                cursor = cursor.sort(sort)
            return await cursor.to_list(None)
        except Exception as e:
            logger.error(f"Error finding documents: {str(e)}")
            raise DatabaseError("find_many", {"error": str(e)})
    
    async def count(self, filter_query: Dict[str, Any]) -> int:
        """Count documents matching filter"""
        try:
            return await self.collection.count_documents(filter_query)
        except Exception as e:
            logger.error(f"Error counting documents: {str(e)}")
            raise DatabaseError("count", {"error": str(e)})
    
    async def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a single document"""
        try:
            result = await self.collection.insert_one(document)
            return await self.find_one({"_id": result.inserted_id})
        except Exception as e:
            logger.error(f"Error inserting document: {str(e)}")
            raise DatabaseError("insert_one", {"error": str(e)})
    
    async def update_one(
        self,
        filter_query: Dict[str, Any],
        update_data: Dict[str, Any],
        upsert: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Update a single document"""
        try:
            result = await self.collection.update_one(
                filter_query,
                {"$set": update_data},
                upsert=upsert
            )
            if result.matched_count == 0 and not upsert:
                return None
            return await self.find_one(filter_query)
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            raise DatabaseError("update_one", {"error": str(e)})
    
    async def delete_one(self, filter_query: Dict[str, Any]) -> bool:
        """Delete a single document"""
        try:
            result = await self.collection.delete_one(filter_query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise DatabaseError("delete_one", {"error": str(e)})
    
    async def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute an aggregation pipeline"""
        try:
            cursor = self.collection.aggregate(pipeline)
            return await cursor.to_list(None)
        except Exception as e:
            logger.error(f"Error executing aggregation: {str(e)}")
            raise DatabaseError("aggregate", {"error": str(e)})
    
    async def create_index(self, keys: List[tuple], unique: bool = False) -> str:
        """Create an index on the collection"""
        try:
            return await self.collection.create_index(keys, unique=unique)
        except Exception as e:
            logger.error(f"Error creating index: {str(e)}")
            raise DatabaseError("create_index", {"error": str(e)}) 