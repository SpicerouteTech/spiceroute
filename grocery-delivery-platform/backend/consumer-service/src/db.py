from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson import ObjectId
from .models import Consumer, Address, PaymentMethod, Cart, CartItem, Order
from .logging_service import logger

load_dotenv()

class DatabaseService:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
        self.db = self.client.spiceroute
        self.consumers = self.db.consumers
        self.orders = self.db.orders
        self.catalog = self.db.catalog  # For reading product information

    async def setup_indexes(self):
        """Setup database indexes"""
        try:
            # Create unique indexes
            await self.consumers.create_index("email", unique=True)
            await self.consumers.create_index([("oauth_provider", 1), ("oauth_id", 1)], unique=True)
            
            # Create regular indexes for frequent queries
            await self.consumers.create_index("created_at")
            await self.consumers.create_index("last_login")
            await self.consumers.create_index("phone")
            
            # New indexes for orders
            await self.orders.create_index("consumer_email")
            await self.orders.create_index("status")
            await self.orders.create_index("created_at")
            await self.orders.create_index([("consumer_email", 1), ("created_at", -1)])
            
            await logger.log("INFO", "Database indexes created successfully")
        except OperationFailure as e:
            await logger.log("ERROR", "Failed to create database indexes", {"error": str(e)})
            raise

    async def get_consumer_by_email(self, email: str) -> Optional[Consumer]:
        """Get consumer by email"""
        try:
            document = await self.consumers.find_one({"email": email})
            if document:
                return Consumer(**document)
            return None
        except Exception as e:
            await logger.log("ERROR", f"Error fetching consumer by email: {email}", {"error": str(e)})
            raise

    async def get_consumer_by_oauth(self, oauth_id: str, provider: str) -> Optional[Consumer]:
        """Get consumer by OAuth ID and provider"""
        try:
            document = await self.consumers.find_one({
                "oauth_id": oauth_id,
                "oauth_provider": provider
            })
            if document:
                return Consumer(**document)
            return None
        except Exception as e:
            await logger.log("ERROR", "Error fetching consumer by OAuth", {
                "oauth_id": oauth_id,
                "provider": provider,
                "error": str(e)
            })
            raise

    async def create_consumer(self, consumer: Consumer) -> Consumer:
        """Create new consumer"""
        try:
            document = consumer.dict()
            await self.consumers.insert_one(document)
            await logger.log("INFO", f"Created new consumer: {consumer.email}")
            return consumer
        except DuplicateKeyError:
            await logger.log("WARNING", f"Duplicate consumer: {consumer.email}")
            raise ValueError("Consumer already exists")
        except Exception as e:
            await logger.log("ERROR", "Error creating consumer", {
                "email": consumer.email,
                "error": str(e)
            })
            raise

    async def update_last_login(self, email: str) -> bool:
        """Update consumer's last login time"""
        try:
            result = await self.consumers.update_one(
                {"email": email},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            if result.modified_count:
                await logger.log("INFO", f"Updated last login for: {email}")
                return True
            await logger.log("WARNING", f"No consumer found to update login: {email}")
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error updating last login for: {email}", {"error": str(e)})
            raise

    async def add_address(self, email: str, address: Address) -> bool:
        """Add a new address for consumer"""
        try:
            # If this is the first address or marked as default, ensure it's set as default
            consumer = await self.get_consumer_by_email(email)
            if not consumer.addresses or address.is_default:
                # Reset all other addresses to non-default if this is default
                if address.is_default:
                    await self.consumers.update_one(
                        {"email": email},
                        {"$set": {"addresses.$[].is_default": False}}
                    )
            
            result = await self.consumers.update_one(
                {"email": email},
                {"$push": {"addresses": address.dict()}}
            )
            if result.modified_count:
                await logger.log("INFO", f"Added address for consumer: {email}")
                return True
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error adding address for: {email}", {"error": str(e)})
            raise

    async def add_payment_method(self, email: str, payment: PaymentMethod) -> bool:
        """Add a new payment method for consumer"""
        try:
            # If this is the first payment method or marked as default, ensure it's set as default
            consumer = await self.get_consumer_by_email(email)
            if not consumer.payment_methods or payment.is_default:
                # Reset all other payment methods to non-default if this is default
                if payment.is_default:
                    await self.consumers.update_one(
                        {"email": email},
                        {"$set": {"payment_methods.$[].is_default": False}}
                    )
            
            result = await self.consumers.update_one(
                {"email": email},
                {"$push": {"payment_methods": payment.dict()}}
            )
            if result.modified_count:
                await logger.log("INFO", f"Added payment method for consumer: {email}")
                return True
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error adding payment method for: {email}", {"error": str(e)})
            raise

    async def update_cart(self, email: str, cart: Cart) -> bool:
        """Update consumer's shopping cart"""
        try:
            cart.last_updated = datetime.utcnow()
            result = await self.consumers.update_one(
                {"email": email},
                {"$set": {"cart": cart.dict()}}
            )
            if result.modified_count:
                await logger.log("INFO", f"Updated cart for consumer: {email}")
                return True
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error updating cart for: {email}", {"error": str(e)})
            raise

    async def clear_cart(self, email: str) -> bool:
        """Clear consumer's shopping cart"""
        try:
            result = await self.consumers.update_one(
                {"email": email},
                {"$set": {"cart": None}}
            )
            if result.modified_count:
                await logger.log("INFO", f"Cleared cart for consumer: {email}")
                return True
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error clearing cart for: {email}", {"error": str(e)})
            raise

    async def create_order(self, order: Order) -> str:
        """Create a new order"""
        try:
            order_dict = order.dict()
            result = await self.orders.insert_one(order_dict)
            order_id = str(result.inserted_id)
            
            # Add order ID to consumer's orders list
            await self.consumers.update_one(
                {"email": order.consumer_email},
                {
                    "$push": {"orders": order_id},
                    "$set": {"cart": None}  # Clear cart after order creation
                }
            )
            
            await logger.log("INFO", f"Created order {order_id} for consumer: {order.consumer_email}")
            return order_id
        except Exception as e:
            await logger.log("ERROR", f"Error creating order for: {order.consumer_email}", {"error": str(e)})
            raise

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        try:
            order = await self.orders.find_one({"_id": ObjectId(order_id)})
            if order:
                order["order_id"] = str(order.pop("_id"))
                return Order(**order)
            return None
        except Exception as e:
            await logger.log("ERROR", f"Error fetching order: {order_id}", {"error": str(e)})
            raise

    async def get_consumer_orders(self, email: str, limit: int = 10, skip: int = 0) -> List[Order]:
        """Get consumer's orders with pagination"""
        try:
            cursor = self.orders.find({"consumer_email": email}) \
                              .sort("created_at", -1) \
                              .skip(skip) \
                              .limit(limit)
            
            orders = []
            async for order in cursor:
                order["order_id"] = str(order.pop("_id"))
                orders.append(Order(**order))
            
            return orders
        except Exception as e:
            await logger.log("ERROR", f"Error fetching orders for consumer: {email}", {"error": str(e)})
            raise

    async def update_order_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        try:
            result = await self.orders.update_one(
                {"_id": ObjectId(order_id)},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            if result.modified_count:
                await logger.log("INFO", f"Updated status for order: {order_id}")
                return True
            return False
        except Exception as e:
            await logger.log("ERROR", f"Error updating order status: {order_id}", {"error": str(e)})
            raise

    async def get_product_details(self, product_id: str) -> Optional[dict]:
        """Get product details from catalog"""
        try:
            product = await self.catalog.find_one({"_id": ObjectId(product_id)})
            if product:
                product["id"] = str(product.pop("_id"))
                return product
            return None
        except Exception as e:
            await logger.log("ERROR", f"Error fetching product: {product_id}", {"error": str(e)})
            raise

    async def close(self):
        """Close database connection"""
        self.client.close()

# Global database service instance
db = DatabaseService() 