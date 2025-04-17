from datetime import datetime, timedelta
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..models.cart import Cart, CartItem
from ..config import settings

class CartService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.carts
        
    async def init_indexes(self):
        """Initialize database indexes"""
        await self.collection.create_index("session_id", unique=True)
        await self.collection.create_index("user_id")
        await self.collection.create_index("expires_at", expireAfterSeconds=0)
    
    async def get_cart(self, session_id: str) -> Optional[Cart]:
        """Get cart by session ID"""
        cart_data = await self.collection.find_one({"session_id": session_id})
        if cart_data:
            return Cart(**cart_data)
        return None
    
    async def create_cart(self, session_id: str, user_id: Optional[str] = None) -> Cart:
        """Create a new cart"""
        cart = Cart(
            session_id=session_id,
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(days=settings.CART_EXPIRY_DAYS)
        )
        await self.collection.insert_one(cart.dict())
        return cart
    
    async def get_or_create_cart(self, session_id: str, user_id: Optional[str] = None) -> Cart:
        """Get existing cart or create new one"""
        cart = await self.get_cart(session_id)
        if not cart:
            cart = await self.create_cart(session_id, user_id)
        return cart
    
    async def add_item(self, session_id: str, item: CartItem) -> Cart:
        """Add item to cart"""
        cart = await self.get_or_create_cart(session_id)
        cart.add_item(item)
        await self.collection.update_one(
            {"session_id": session_id},
            {"$set": cart.dict()}
        )
        return cart
    
    async def remove_item(self, session_id: str, product_id: str) -> Cart:
        """Remove item from cart"""
        cart = await self.get_cart(session_id)
        if cart:
            cart.remove_item(product_id)
            await self.collection.update_one(
                {"session_id": session_id},
                {"$set": cart.dict()}
            )
        return cart
    
    async def update_item_quantity(self, session_id: str, product_id: str, quantity: int) -> Cart:
        """Update item quantity in cart"""
        cart = await self.get_cart(session_id)
        if cart:
            cart.update_item_quantity(product_id, quantity)
            await self.collection.update_one(
                {"session_id": session_id},
                {"$set": cart.dict()}
            )
        return cart
    
    async def clear_cart(self, session_id: str) -> None:
        """Clear all items from cart"""
        cart = await self.get_cart(session_id)
        if cart:
            cart.clear()
            await self.collection.update_one(
                {"session_id": session_id},
                {"$set": cart.dict()}
            )
    
    async def delete_cart(self, session_id: str) -> None:
        """Delete cart"""
        await self.collection.delete_one({"session_id": session_id})
    
    async def merge_carts(self, source_session_id: str, target_session_id: str) -> Cart:
        """Merge items from source cart into target cart"""
        source_cart = await self.get_cart(source_session_id)
        target_cart = await self.get_cart(target_session_id)
        
        if source_cart and target_cart:
            for item in source_cart.items:
                target_cart.add_item(item)
            
            await self.collection.update_one(
                {"session_id": target_session_id},
                {"$set": target_cart.dict()}
            )
            await self.delete_cart(source_session_id)
            
        return target_cart

# Create service instance
cart_service = None

async def init_cart_service(db: AsyncIOMotorDatabase):
    global cart_service
    cart_service = CartService(db)
    await cart_service.init_indexes() 