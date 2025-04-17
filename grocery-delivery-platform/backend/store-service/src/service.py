from datetime import datetime
from typing import List, Optional, Dict
from fastapi import HTTPException, status
import logging
from uuid import uuid4

from .models import Store, Category, Product
from .db import DatabaseService

logger = logging.getLogger(__name__)

class StoreService:
    def __init__(self, database_service: DatabaseService):
        self.db = database_service
    
    # Store Management
    
    async def create_store(self, store_data: Store) -> Dict:
        """Create a new store"""
        try:
            # Generate unique store ID
            store_data.store_id = str(uuid4())
            store_data.created_at = datetime.utcnow()
            store_data.updated_at = datetime.utcnow()
            
            return await self.db.create_store(store_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error creating store: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating store"
            )
    
    async def get_store(self, store_id: str) -> Dict:
        """Get store details"""
        store = await self.db.get_store(store_id)
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Store not found"
            )
        return store
    
    async def get_owner_stores(self, owner_email: str) -> List[Dict]:
        """Get all stores owned by a store owner"""
        return await self.db.get_stores_by_owner(owner_email)
    
    async def update_store(self, store_id: str, update_data: Dict) -> Dict:
        """Update store information"""
        store = await self.get_store(store_id)  # Verify store exists
        updated_store = await self.db.update_store(store_id, update_data)
        if not updated_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Store not found"
            )
        return updated_store
    
    # Category Management
    
    async def create_category(self, category_data: Category) -> Dict:
        """Create a new category"""
        try:
            # Generate unique category ID
            category_data.category_id = str(uuid4())
            category_data.created_at = datetime.utcnow()
            category_data.updated_at = datetime.utcnow()
            
            return await self.db.create_category(category_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating category"
            )
    
    async def get_store_categories(self, store_id: str) -> List[Dict]:
        """Get all categories for a store"""
        # Verify store exists
        await self.get_store(store_id)
        return await self.db.get_store_categories(store_id)
    
    async def update_category(self, category_id: str, update_data: Dict) -> Dict:
        """Update category information"""
        category = await self.db.get_category(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return await self.db.update_category(category_id, update_data)
    
    # Product Management
    
    async def create_product(self, product_data: Product) -> Dict:
        """Create a new product"""
        try:
            # Generate unique product ID
            product_data.product_id = str(uuid4())
            product_data.created_at = datetime.utcnow()
            product_data.updated_at = datetime.utcnow()
            
            return await self.db.create_product(product_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating product"
            )
    
    async def get_product(self, product_id: str) -> Dict:
        """Get product details"""
        product = await self.db.get_product(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    
    async def get_category_products(self, category_id: str) -> List[Dict]:
        """Get all products in a category"""
        # Verify category exists
        category = await self.db.get_category(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return await self.db.get_category_products(category_id)
    
    async def get_store_products(self, store_id: str, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get all products for a store with pagination"""
        # Verify store exists
        await self.get_store(store_id)
        return await self.db.get_store_products(store_id, skip, limit)
    
    async def update_product(self, product_id: str, update_data: Dict) -> Dict:
        """Update product information"""
        product = await self.get_product(product_id)  # Verify product exists
        return await self.db.update_product(product_id, update_data)
    
    async def search_products(self, store_id: str, query: str, skip: int = 0, limit: int = 20) -> List[Dict]:
        """Search products by text query within a store"""
        # Verify store exists
        await self.get_store(store_id)
        return await self.db.search_products(store_id, query, skip, limit)
    
    async def update_product_stock(self, product_id: str, quantity_change: int) -> Dict:
        """Update product stock quantity"""
        product = await self.get_product(product_id)  # Verify product exists
        
        # Prevent negative stock
        if product["stock_quantity"] + quantity_change < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock quantity"
            )
        
        return await self.db.update_product_stock(product_id, quantity_change) 