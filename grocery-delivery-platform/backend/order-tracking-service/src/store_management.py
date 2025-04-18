from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from .models import OrderTracking, OrderTrackingStatus, ItemSubstitution
from .service import OrderTrackingService

class StoreOrderManagementService:
    def __init__(self, tracking_service: OrderTrackingService):
        self.tracking_service = tracking_service

    async def get_store_orders(
        self,
        store_id: str,
        status: Optional[List[OrderTrackingStatus]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search_query: Optional[str] = None,
        search_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Get orders for a specific store with filtering, search and pagination."""
        query = {"store_id": store_id}
        
        if status:
            query["current_status"] = {"$in": status}
        if start_date and end_date:
            query["created_at"] = {
                "$gte": start_date,
                "$lte": end_date
            }
            
        # Add search functionality
        if search_query:
            if search_type == "order_id":
                query["order_id"] = {"$regex": search_query, "$options": "i"}
            elif search_type == "phone":
                query["customer_details.phone"] = {"$regex": search_query, "$options": "i"}
            elif search_type == "customer_name":
                query["customer_details.name"] = {"$regex": search_query, "$options": "i"}

        total = await self.tracking_service.collection.count_documents(query)
        skip = (page - 1) * page_size

        orders = await self.tracking_service.collection.find(query) \
            .sort("created_at", -1) \
            .skip(skip) \
            .limit(page_size) \
            .to_list(length=page_size)

        return {
            "orders": [OrderTracking(**order) for order in orders],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

    async def search_orders(
        self,
        store_id: str,
        search_query: str,
        search_type: str,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Search orders by different criteria.
        search_type can be: order_id, phone, customer_name
        """
        query = {"store_id": store_id}
        
        if search_type == "order_id":
            query["order_id"] = {"$regex": search_query, "$options": "i"}
        elif search_type == "phone":
            query["customer_details.phone"] = {"$regex": search_query, "$options": "i"}
        elif search_type == "customer_name":
            query["customer_details.name"] = {"$regex": search_query, "$options": "i"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid search type"
            )

        total = await self.tracking_service.collection.count_documents(query)
        skip = (page - 1) * page_size

        orders = await self.tracking_service.collection.find(query) \
            .sort("created_at", -1) \
            .skip(skip) \
            .limit(page_size) \
            .to_list(length=page_size)

        return {
            "orders": [OrderTracking(**order) for order in orders],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "search_type": search_type,
            "search_query": search_query
        }

    async def get_recent_searches(
        self,
        store_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get recent successful searches for the store."""
        pipeline = [
            {"$match": {
                "store_id": store_id,
                "metadata.search_history": {"$exists": True}
            }},
            {"$unwind": "$metadata.search_history"},
            {"$sort": {"metadata.search_history.timestamp": -1}},
            {"$group": {
                "_id": "$metadata.search_history.query",
                "last_used": {"$first": "$metadata.search_history.timestamp"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"last_used": -1}},
            {"$limit": limit}
        ]
        
        recent_searches = await self.tracking_service.collection.aggregate(pipeline).to_list(None)
        return recent_searches

    async def accept_order(
        self,
        order_id: str,
        store_id: str,
        estimated_preparation_time: int
    ) -> OrderTracking:
        """Accept an order and provide estimated preparation time."""
        tracking = await self.tracking_service.get_order_tracking(order_id)
        
        if tracking.store_id != store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Store not authorized to manage this order"
            )

        if tracking.current_status != OrderTrackingStatus.STORE_NOTIFIED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot accept order in {tracking.current_status} status"
            )

        return await self.tracking_service.store_acknowledge(
            order_id=order_id,
            store_id=store_id,
            estimated_preparation_time=estimated_preparation_time
        )

    async def reject_order(
        self,
        order_id: str,
        store_id: str,
        reason: str
    ) -> OrderTracking:
        """Reject an order with a reason."""
        tracking = await self.tracking_service.get_order_tracking(order_id)
        
        if tracking.store_id != store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Store not authorized to manage this order"
            )

        if tracking.current_status not in [OrderTrackingStatus.STORE_NOTIFIED, OrderTrackingStatus.SUBMITTED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot reject order in {tracking.current_status} status"
            )

        return await self.tracking_service.update_status(
            order_id=order_id,
            new_status=OrderTrackingStatus.CANCELLED,
            updated_by=f"store_{store_id}",
            notes=f"Rejected by store: {reason}"
        )

    async def mark_order_ready(
        self,
        order_id: str,
        store_id: str
    ) -> OrderTracking:
        """Mark an order as ready for pickup."""
        tracking = await self.tracking_service.get_order_tracking(order_id)
        
        if tracking.store_id != store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Store not authorized to manage this order"
            )

        if tracking.current_status not in [
            OrderTrackingStatus.PICKING_IN_PROGRESS,
            OrderTrackingStatus.SUBSTITUTIONS_APPROVED,
            OrderTrackingStatus.PACKING_IN_PROGRESS
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot mark order ready in {tracking.current_status} status"
            )

        return await self.tracking_service.update_status(
            order_id=order_id,
            new_status=OrderTrackingStatus.READY_FOR_PICKUP,
            updated_by=f"store_{store_id}"
        )

    async def request_refund(
        self,
        order_id: str,
        store_id: str,
        reason: str,
        amount: float,
        items: List[str]
    ) -> OrderTracking:
        """Request a refund for an order or specific items."""
        tracking = await self.tracking_service.get_order_tracking(order_id)
        
        if tracking.store_id != store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Store not authorized to manage this order"
            )

        # Add refund request to metadata
        refund_request = {
            "reason": reason,
            "amount": amount,
            "items": items,
            "requested_at": datetime.utcnow(),
            "status": "pending"
        }

        tracking.metadata["refund_request"] = refund_request
        
        # Update the tracking record
        result = await self.tracking_service.collection.find_one_and_update(
            {"order_id": order_id},
            {
                "$set": {
                    "metadata": tracking.metadata,
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )

        return OrderTracking(**result)

    async def start_order_preparation(
        self,
        order_id: str,
        store_id: str
    ) -> OrderTracking:
        """Start preparing an order."""
        tracking = await self.tracking_service.get_order_tracking(order_id)
        
        if tracking.store_id != store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Store not authorized to manage this order"
            )

        if tracking.current_status != OrderTrackingStatus.STORE_ACKNOWLEDGED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot start preparation in {tracking.current_status} status"
            )

        return await self.tracking_service.update_status(
            order_id=order_id,
            new_status=OrderTrackingStatus.PICKING_IN_PROGRESS,
            updated_by=f"store_{store_id}"
        )

    async def _record_search(
        self,
        store_id: str,
        search_query: str,
        search_type: str
    ) -> None:
        """Record search query in store's metadata for search history."""
        search_record = {
            "query": search_query,
            "type": search_type,
            "timestamp": datetime.utcnow()
        }
        
        await self.tracking_service.collection.update_one(
            {"store_id": store_id},
            {
                "$push": {
                    "metadata.search_history": {
                        "$each": [search_record],
                        "$slice": -50  # Keep last 50 searches
                    }
                }
            }
        ) 