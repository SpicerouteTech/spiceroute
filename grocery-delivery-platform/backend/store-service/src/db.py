import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import Store, Category, Product
import pymongo
from fastapi import HTTPException, status
from pymongo import ASCENDING, DESCENDING, IndexModel


logger = logging.getLogger(__name__)

# MongoDB setup
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "spiceroute")


class DatabaseService:
    def __init__(self, mongo_url: str, database_name: str = "spiceroute"):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[database_name]
        
        # Collections
        self.stores = self.db.stores
        self.categories = self.db.categories
        self.products = self.db.products
        
    async def init_indexes(self):
        """Initialize database indexes"""
        try:
            # Store indexes
            await self.stores.create_indexes([
                IndexModel([("store_id", ASCENDING)], unique=True),
                IndexModel([("owner_email", ASCENDING)]),
                IndexModel([("location.coordinates", "2dsphere")])
            ])
            
            # Category indexes
            await self.categories.create_indexes([
                IndexModel([("category_id", ASCENDING)], unique=True),
                IndexModel([("store_id", ASCENDING)]),
                IndexModel([("parent_id", ASCENDING)])
            ])
            
            # Product indexes
            await self.products.create_indexes([
                IndexModel([("product_id", ASCENDING)], unique=True),
                IndexModel([("store_id", ASCENDING)]),
                IndexModel([("category_id", ASCENDING)]),
                IndexModel([("name", "text"), ("description", "text")])
            ])
            
            logger.info("Database indexes initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database indexes: {str(e)}")
            raise
    
    # Store Operations
    
    async def create_store(self, store: Store) -> Dict:
        """Create a new store"""
        try:
            result = await self.stores.insert_one(store.dict())
            return await self.get_store(store.store_id)
        except Exception as e:
            logger.error(f"Error creating store: {str(e)}")
            raise
    
    async def get_store(self, store_id: str) -> Optional[Dict]:
        """Get store by ID"""
        return await self.stores.find_one({"store_id": store_id})
    
    async def get_stores_by_owner(self, owner_email: str) -> List[Dict]:
        """Get all stores owned by a store owner"""
        cursor = self.stores.find({"owner_email": owner_email})
        return await cursor.to_list(None)
    
    async def update_store(self, store_id: str, update_data: Dict) -> Optional[Dict]:
        """Update store information"""
        update_data["updated_at"] = datetime.utcnow()
        await self.stores.update_one(
            {"store_id": store_id},
            {"$set": update_data}
        )
        return await self.get_store(store_id)
    
    # Category Operations
    
    async def create_category(self, category: Category) -> Dict:
        """Create a new category"""
        try:
            # Verify store exists
            store = await self.get_store(category.store_id)
            if not store:
                raise ValueError("Store not found")
                
            result = await self.categories.insert_one(category.dict())
            return await self.get_category(category.category_id)
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            raise
    
    async def get_category(self, category_id: str) -> Optional[Dict]:
        """Get category by ID"""
        return await self.categories.find_one({"category_id": category_id})
    
    async def get_store_categories(self, store_id: str) -> List[Dict]:
        """Get all categories for a store"""
        cursor = self.categories.find({"store_id": store_id})
        return await cursor.to_list(None)
    
    async def update_category(self, category_id: str, update_data: Dict) -> Optional[Dict]:
        """Update category information"""
        update_data["updated_at"] = datetime.utcnow()
        await self.categories.update_one(
            {"category_id": category_id},
            {"$set": update_data}
        )
        return await self.get_category(category_id)
    
    # Product Operations
    
    async def create_product(self, product: Product) -> Dict:
        """Create a new product"""
        try:
            # Verify store and category exist
            store = await self.get_store(product.store_id)
            if not store:
                raise ValueError("Store not found")
                
            category = await self.get_category(product.category_id)
            if not category:
                raise ValueError("Category not found")
                
            result = await self.products.insert_one(product.dict())
            return await self.get_product(product.product_id)
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            raise
    
    async def get_product(self, product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        return await self.products.find_one({"product_id": product_id})
    
    async def get_category_products(self, category_id: str) -> List[Dict]:
        """Get all products in a category"""
        cursor = self.products.find({"category_id": category_id})
        return await cursor.to_list(None)
    
    async def get_store_products(self, store_id: str, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get all products for a store with pagination"""
        cursor = self.products.find({"store_id": store_id}).skip(skip).limit(limit)
        return await cursor.to_list(None)
    
    async def update_product(self, product_id: str, update_data: Dict) -> Optional[Dict]:
        """Update product information"""
        update_data["updated_at"] = datetime.utcnow()
        await self.products.update_one(
            {"product_id": product_id},
            {"$set": update_data}
        )
        return await self.get_product(product_id)
    
    async def search_products(self, store_id: str, query: str, skip: int = 0, limit: int = 20) -> List[Dict]:
        """Search products by text query within a store"""
        cursor = self.products.find({
            "store_id": store_id,
            "$text": {"$search": query}
        }).skip(skip).limit(limit)
        return await cursor.to_list(None)
    
    async def update_product_stock(self, product_id: str, quantity_change: int) -> Optional[Dict]:
        """Update product stock quantity"""
        try:
            await self.products.update_one(
                {"product_id": product_id},
                {
                    "$inc": {"stock_quantity": quantity_change},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return await self.get_product(product_id)
        except Exception as e:
            logger.error(f"Error updating product stock: {str(e)}")
            raise 