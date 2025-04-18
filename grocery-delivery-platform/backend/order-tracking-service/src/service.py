from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
import logging
import asyncio
from bson import ObjectId

from .models import (
    OrderTracking,
    OrderTrackingStatus,
    OrderStatusUpdate,
    DeliveryProvider,
    ItemSubstitution,
    GeoLocation,
    DriverDetails
)
from .notifications.service import NotificationService, NotificationPreference
from .delivery import UberDeliveryClient, DoorDashDeliveryClient
from .exceptions import (
    OrderTrackingError,
    StoreAcknowledgmentTimeout,
    DeliveryProviderError
)

logger = logging.getLogger(__name__)

class OrderTrackingService:
    def __init__(
        self,
        mongodb_url: str,
        database_name: str,
        uber_client: Optional[UberDeliveryClient] = None,
        doordash_client: Optional[DoorDashDeliveryClient] = None,
    ):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[database_name]
        self.collection = self.db.order_tracking
        self.notification_service = NotificationService()
        self.uber_client = uber_client
        self.doordash_client = doordash_client
        
        # Initialize indexes
        asyncio.create_task(self._init_indexes())
    
    async def _init_indexes(self) -> None:
        """Initialize required indexes for the order tracking collection."""
        try:
            await self.collection.create_index("order_id", unique=True)
            await self.collection.create_index("store_id")
            await self.collection.create_index("customer_id")
            await self.collection.create_index("current_status")
            await self.collection.create_index("delivery_provider")
            await self.collection.create_index("created_at")
            logger.info("Order tracking indexes initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize indexes: {str(e)}")
            raise
    
    async def init_order_tracking(
        self,
        order_id: str,
        store_id: str,
        customer_id: str,
        delivery_provider: DeliveryProvider,
        metadata: Optional[Dict[str, Any]] = None
    ) -> OrderTracking:
        """Initialize tracking for a new order."""
        try:
            tracking = OrderTracking(
                order_id=order_id,
                store_id=store_id,
                customer_id=customer_id,
                delivery_provider=delivery_provider,
                current_status=OrderTrackingStatus.SUBMITTED,
                status_history=[
                    OrderStatusUpdate(
                        status=OrderTrackingStatus.SUBMITTED,
                        timestamp=datetime.utcnow(),
                        updated_by="system",
                        metadata=metadata or {}
                    )
                ],
                metadata=metadata or {}
            )
            
            result = await self.collection.insert_one(tracking.dict())
            if not result.acknowledged:
                raise OrderTrackingError("Failed to initialize order tracking")
            
            # Start monitoring store acknowledgment
            asyncio.create_task(self._monitor_store_acknowledgment(order_id))
            
            return tracking
        except Exception as e:
            logger.error(f"Error initializing order tracking: {str(e)}")
            raise OrderTrackingError(f"Failed to initialize tracking: {str(e)}")
    
    async def _monitor_store_acknowledgment(self, order_id: str, timeout_seconds: int = 300) -> None:
        """Monitor store acknowledgment with timeout."""
        try:
            await asyncio.sleep(timeout_seconds)
            tracking = await self.get_order_tracking(order_id)
            
            if tracking.current_status == OrderTrackingStatus.STORE_NOTIFIED:
                # Store hasn't acknowledged yet
                await self.update_status(
                    order_id=order_id,
                    new_status=OrderTrackingStatus.FAILED,
                    updated_by="system",
                    notes="Store acknowledgment timeout"
                )
                raise StoreAcknowledgmentTimeout(f"Store failed to acknowledge order {order_id}")
        except Exception as e:
            logger.error(f"Error monitoring store acknowledgment: {str(e)}")
    
    async def update_status(
        self,
        order_id: str,
        new_status: OrderTrackingStatus,
        updated_by: str,
        notes: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> OrderTracking:
        """Update the status of an order with optimistic locking."""
        try:
            status_update = OrderStatusUpdate(
                status=new_status,
                timestamp=datetime.utcnow(),
                updated_by=updated_by,
                notes=notes,
                metadata=metadata or {}
            )
            
            result = await self.collection.find_one_and_update(
                {"order_id": order_id},
                {
                    "$set": {
                        "current_status": new_status,
                        "updated_at": datetime.utcnow()
                    },
                    "$push": {"status_history": status_update.dict()}
                },
                return_document=ReturnDocument.AFTER
            )
            
            if not result:
                raise OrderTrackingError(f"Order tracking not found: {order_id}")
            
            tracking = OrderTracking(**result)
            
            # Send notifications for status update
            await self._send_status_notifications(tracking, new_status)
            
            return tracking
        except Exception as e:
            logger.error(f"Error updating order status: {str(e)}")
            raise OrderTrackingError(f"Failed to update status: {str(e)}")
    
    async def _send_status_notifications(
        self,
        tracking: OrderTracking,
        status: OrderTrackingStatus
    ) -> None:
        """Send notifications for order status updates."""
        try:
            # Get customer notification preferences
            preferences = await self._get_customer_preferences(tracking.customer_id)
            
            # Prepare additional data for notifications
            additional_data = {
                "store_name": tracking.metadata.get("store_name", ""),
                "order_total": tracking.metadata.get("total_amount", 0),
                "eta": tracking.estimated_delivery_time.isoformat() if tracking.estimated_delivery_time else "",
            }
            
            # Add driver details if available
            if tracking.driver_details:
                additional_data.update({
                    "driver_name": tracking.driver_details.name,
                    "driver_phone": tracking.driver_details.phone
                })
            
            # Send notifications through preferred channels
            await self.notification_service.send_order_status_notification(
                customer_id=tracking.customer_id,
                order_id=tracking.order_id,
                status=status,
                preferences=preferences,
                additional_data=additional_data
            )
        except Exception as e:
            logger.error(f"Error sending notifications: {str(e)}")
            # Don't raise the error to avoid affecting the main flow
            # but log it for monitoring

    async def _get_customer_preferences(self, customer_id: str) -> NotificationPreference:
        """Get customer notification preferences from the database."""
        # This would typically fetch from a customer service or preferences database
        # For now, return default preferences
        return NotificationPreference(
            customer_id=customer_id,
            channels=["email", "push"],  # Default channels
            email="customer@example.com",  # This should come from customer profile
            phone="+1234567890",  # This should come from customer profile
            push_tokens=["device_token_1"],  # This should come from customer's devices
            whatsapp_opted_in=False
        )
    
    async def store_acknowledge(
        self,
        order_id: str,
        store_id: str
    ) -> OrderTracking:
        """Handle store acknowledgment of an order."""
        try:
            result = await self.collection.find_one_and_update(
                {
                    "order_id": order_id,
                    "store_id": store_id,
                    "current_status": OrderTrackingStatus.STORE_NOTIFIED
                },
                {
                    "$set": {
                        "current_status": OrderTrackingStatus.STORE_ACKNOWLEDGED,
                        "store_acknowledgment_time": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    },
                    "$push": {
                        "status_history": {
                            "status": OrderTrackingStatus.STORE_ACKNOWLEDGED,
                            "timestamp": datetime.utcnow(),
                            "updated_by": f"store_{store_id}"
                        }
                    }
                },
                return_document=ReturnDocument.AFTER
            )
            
            if not result:
                raise OrderTrackingError(f"Invalid order state for acknowledgment: {order_id}")
            
            return OrderTracking(**result)
        except Exception as e:
            logger.error(f"Error acknowledging order: {str(e)}")
            raise OrderTrackingError(f"Failed to acknowledge order: {str(e)}")
    
    async def update_substitutions(
        self,
        order_id: str,
        substitutions: List[ItemSubstitution]
    ) -> OrderTracking:
        """Update order substitutions and notify customer."""
        try:
            result = await self.collection.find_one_and_update(
                {"order_id": order_id},
                {
                    "$set": {
                        "substitutions": [sub.dict() for sub in substitutions],
                        "current_status": OrderTrackingStatus.SUBSTITUTIONS_NEEDED,
                        "updated_at": datetime.utcnow()
                    },
                    "$push": {
                        "status_history": {
                            "status": OrderTrackingStatus.SUBSTITUTIONS_NEEDED,
                            "timestamp": datetime.utcnow(),
                            "updated_by": "store",
                            "notes": f"Substitutions needed for {len(substitutions)} items"
                        }
                    }
                },
                return_document=ReturnDocument.AFTER
            )
            
            if not result:
                raise OrderTrackingError(f"Order tracking not found: {order_id}")
            
            # Trigger customer notification (implement in notification service)
            tracking = OrderTracking(**result)
            asyncio.create_task(self._notify_customer_substitutions(tracking))
            
            return tracking
        except Exception as e:
            logger.error(f"Error updating substitutions: {str(e)}")
            raise OrderTrackingError(f"Failed to update substitutions: {str(e)}")
    
    async def update_driver_location(
        self,
        order_id: str,
        location: GeoLocation,
        provider: DeliveryProvider
    ) -> OrderTracking:
        """Update driver's current location."""
        try:
            result = await self.collection.find_one_and_update(
                {
                    "order_id": order_id,
                    "delivery_provider": provider,
                    "current_status": {"$in": [
                        OrderTrackingStatus.DRIVER_PICKUP_COMPLETE,
                        OrderTrackingStatus.IN_TRANSIT
                    ]}
                },
                {
                    "$set": {
                        "driver_location": location.dict(),
                        "updated_at": datetime.utcnow()
                    }
                },
                return_document=ReturnDocument.AFTER
            )
            
            if not result:
                raise OrderTrackingError(f"Invalid order state for location update: {order_id}")
            
            return OrderTracking(**result)
        except Exception as e:
            logger.error(f"Error updating driver location: {str(e)}")
            raise OrderTrackingError(f"Failed to update driver location: {str(e)}")
    
    async def assign_delivery(
        self,
        order_id: str,
        driver_details: DriverDetails,
        provider: DeliveryProvider
    ) -> OrderTracking:
        """Assign a delivery driver to the order."""
        try:
            result = await self.collection.find_one_and_update(
                {
                    "order_id": order_id,
                    "current_status": OrderTrackingStatus.READY_FOR_PICKUP
                },
                {
                    "$set": {
                        "current_status": OrderTrackingStatus.DRIVER_ASSIGNED,
                        "driver_details": driver_details.dict(),
                        "updated_at": datetime.utcnow()
                    },
                    "$push": {
                        "status_history": {
                            "status": OrderTrackingStatus.DRIVER_ASSIGNED,
                            "timestamp": datetime.utcnow(),
                            "updated_by": f"delivery_{provider}",
                            "metadata": {"driver_id": driver_details.driver_id}
                        }
                    }
                },
                return_document=ReturnDocument.AFTER
            )
            
            if not result:
                raise OrderTrackingError(f"Invalid order state for driver assignment: {order_id}")
            
            return OrderTracking(**result)
        except Exception as e:
            logger.error(f"Error assigning delivery: {str(e)}")
            raise OrderTrackingError(f"Failed to assign delivery: {str(e)}")
    
    async def mark_delivered(
        self,
        order_id: str,
        provider: DeliveryProvider,
        proof_of_delivery: Optional[Dict[str, Any]] = None
    ) -> OrderTracking:
        """Mark an order as delivered with proof of delivery."""
        try:
            result = await self.collection.find_one_and_update(
                {
                    "order_id": order_id,
                    "delivery_provider": provider,
                    "current_status": OrderTrackingStatus.IN_TRANSIT
                },
                {
                    "$set": {
                        "current_status": OrderTrackingStatus.DELIVERED,
                        "actual_delivery_time": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    },
                    "$push": {
                        "status_history": {
                            "status": OrderTrackingStatus.DELIVERED,
                            "timestamp": datetime.utcnow(),
                            "updated_by": f"delivery_{provider}",
                            "metadata": proof_of_delivery or {}
                        }
                    }
                },
                return_document=ReturnDocument.AFTER
            )
            
            if not result:
                raise OrderTrackingError(f"Invalid order state for delivery completion: {order_id}")
            
            tracking = OrderTracking(**result)
            # Trigger delivery completion handlers
            asyncio.create_task(self._handle_delivery_completion(tracking))
            
            return tracking
        except Exception as e:
            logger.error(f"Error marking order as delivered: {str(e)}")
            raise OrderTrackingError(f"Failed to mark order as delivered: {str(e)}")
    
    async def get_order_tracking(self, order_id: str) -> OrderTracking:
        """Retrieve order tracking details."""
        try:
            result = await self.collection.find_one({"order_id": order_id})
            if not result:
                raise OrderTrackingError(f"Order tracking not found: {order_id}")
            return OrderTracking(**result)
        except Exception as e:
            logger.error(f"Error retrieving order tracking: {str(e)}")
            raise OrderTrackingError(f"Failed to retrieve tracking: {str(e)}")
    
    async def _notify_customer_substitutions(self, tracking: OrderTracking) -> None:
        """Handle customer notification for substitutions asynchronously."""
        try:
            # Implement notification logic here
            logger.info(f"Customer notification sent for substitutions: {tracking.order_id}")
        except Exception as e:
            logger.error(f"Error notifying customer of substitutions: {str(e)}")
    
    async def _handle_delivery_completion(self, tracking: OrderTracking) -> None:
        """Handle post-delivery tasks asynchronously."""
        try:
            # Implement post-delivery handlers here
            logger.info(f"Delivery completion handled for order: {tracking.order_id}")
        except Exception as e:
            logger.error(f"Error handling delivery completion: {str(e)}") 