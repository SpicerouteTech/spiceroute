from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from .models import OrderTracking, OrderTrackingStatus
from .store_management import StoreOrderManagementService
from .service import OrderTrackingService
from .auth import get_current_store_owner

router = APIRouter(prefix="/store/orders", tags=["store-orders"])

# Initialize services
tracking_service = OrderTrackingService()
store_management = StoreOrderManagementService(tracking_service)

@router.get("/")
async def get_store_orders(
    status: Optional[List[OrderTrackingStatus]] = Query(None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    search_query: Optional[str] = Query(None),
    search_type: Optional[str] = Query(None, enum=["order_id", "phone", "customer_name"]),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_store = Depends(get_current_store_owner)
):
    """Get orders for the current store with filtering and pagination."""
    return await store_management.get_store_orders(
        store_id=str(current_store.id),
        status=status,
        start_date=start_date,
        end_date=end_date,
        search_query=search_query,
        search_type=search_type,
        page=page,
        page_size=page_size
    )

@router.get("/search")
async def search_orders(
    query: str = Query(..., min_length=1),
    search_type: str = Query(..., enum=["order_id", "phone", "customer_name"]),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_store = Depends(get_current_store_owner)
):
    """Search orders by order ID, customer phone, or customer name."""
    result = await store_management.search_orders(
        store_id=str(current_store.id),
        search_query=query,
        search_type=search_type,
        page=page,
        page_size=page_size
    )
    
    # Record successful search
    await store_management._record_search(
        store_id=str(current_store.id),
        search_query=query,
        search_type=search_type
    )
    
    return result

@router.get("/search/recent")
async def get_recent_searches(
    limit: int = Query(5, ge=1, le=20),
    current_store = Depends(get_current_store_owner)
):
    """Get recent successful searches for the store."""
    return await store_management.get_recent_searches(
        store_id=str(current_store.id),
        limit=limit
    )

@router.post("/{order_id}/accept")
async def accept_order(
    order_id: str,
    estimated_preparation_time: int = Query(..., gt=0),
    current_store = Depends(get_current_store_owner)
):
    """Accept an order and provide estimated preparation time."""
    return await store_management.accept_order(
        order_id=order_id,
        store_id=str(current_store.id),
        estimated_preparation_time=estimated_preparation_time
    )

@router.post("/{order_id}/reject")
async def reject_order(
    order_id: str,
    reason: str = Query(..., min_length=1),
    current_store = Depends(get_current_store_owner)
):
    """Reject an order with a reason."""
    return await store_management.reject_order(
        order_id=order_id,
        store_id=str(current_store.id),
        reason=reason
    )

@router.post("/{order_id}/ready")
async def mark_order_ready(
    order_id: str,
    current_store = Depends(get_current_store_owner)
):
    """Mark an order as ready for pickup."""
    return await store_management.mark_order_ready(
        order_id=order_id,
        store_id=str(current_store.id)
    )

@router.post("/{order_id}/refund")
async def request_refund(
    order_id: str,
    reason: str = Query(..., min_length=1),
    amount: float = Query(..., gt=0),
    items: List[str] = Query(...),
    current_store = Depends(get_current_store_owner)
):
    """Request a refund for an order or specific items."""
    return await store_management.request_refund(
        order_id=order_id,
        store_id=str(current_store.id),
        reason=reason,
        amount=amount,
        items=items
    )

@router.post("/{order_id}/start-preparation")
async def start_order_preparation(
    order_id: str,
    current_store = Depends(get_current_store_owner)
):
    """Start preparing an order."""
    return await store_management.start_order_preparation(
        order_id=order_id,
        store_id=str(current_store.id)
    )

@router.get("/dashboard/summary")
async def get_store_dashboard(
    current_store = Depends(get_current_store_owner)
):
    """Get a summary of store orders for the dashboard."""
    store_id = str(current_store.id)
    
    # Get counts for different order statuses
    pipeline = [
        {"$match": {"store_id": store_id}},
        {
            "$group": {
                "_id": "$current_status",
                "count": {"$sum": 1}
            }
        }
    ]
    
    status_counts = await tracking_service.collection.aggregate(pipeline).to_list(None)
    
    # Get today's orders
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_orders = await tracking_service.collection.count_documents({
        "store_id": store_id,
        "created_at": {"$gte": today_start}
    })
    
    # Get orders requiring attention (new orders, substitutions needed)
    attention_needed = await tracking_service.collection.count_documents({
        "store_id": store_id,
        "current_status": {
            "$in": [
                OrderTrackingStatus.STORE_NOTIFIED,
                OrderTrackingStatus.SUBSTITUTIONS_NEEDED
            ]
        }
    })
    
    return {
        "status_counts": {
            item["_id"]: item["count"] for item in status_counts
        },
        "today_orders": today_orders,
        "attention_needed": attention_needed
    } 