from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .models import (
    OrderTracking,
    OrderTrackingStatus,
    DeliveryProvider,
    DriverDetails,
    GeoLocation,
    ItemSubstitution
)
from .service import OrderTrackingService
from .auth import get_current_user, get_current_store

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize service (you'll need to implement the actual initialization)
tracking_service = OrderTrackingService()

@router.post("/tracking/init", response_model=OrderTracking)
async def initialize_order_tracking(
    order_id: str,
    store_id: str,
    customer_id: str,
    delivery_provider: DeliveryProvider,
    current_user = Depends(get_current_user)
):
    """Initialize tracking for a new order."""
    try:
        tracking = await tracking_service.init_order_tracking(
            order_id=order_id,
            store_id=store_id,
            customer_id=customer_id,
            delivery_provider=delivery_provider
        )
        return tracking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/tracking/{order_id}", response_model=OrderTracking)
async def get_order_tracking(
    order_id: str,
    current_user = Depends(get_current_user)
):
    """Get tracking information for an order."""
    tracking = await tracking_service.get_order_tracking(order_id)
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order tracking not found for order {order_id}"
        )
    return tracking

@router.post("/tracking/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: OrderTrackingStatus,
    notes: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Update the status of an order."""
    try:
        await tracking_service.update_status(
            order_id=order_id,
            status=status,
            updated_by=str(current_user.id),
            notes=notes
        )
        return {"message": "Status updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/tracking/{order_id}/store/acknowledge")
async def store_acknowledge_order(
    order_id: str,
    estimated_preparation_time: int,
    current_store = Depends(get_current_store)
):
    """Store acknowledges the order and provides estimated preparation time."""
    try:
        await tracking_service.store_acknowledge(
            order_id=order_id,
            store_id=str(current_store.id),
            estimated_preparation_time=estimated_preparation_time
        )
        return {"message": "Order acknowledged successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/tracking/{order_id}/substitutions")
async def update_order_substitutions(
    order_id: str,
    substitutions: List[ItemSubstitution],
    current_store = Depends(get_current_store)
):
    """Update substitutions for an order."""
    try:
        await tracking_service.update_substitutions(
            order_id=order_id,
            store_id=str(current_store.id),
            substitutions=substitutions
        )
        return {"message": "Substitutions updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/tracking/{order_id}/delivery/assign")
async def assign_delivery(
    order_id: str,
    driver_details: DriverDetails,
    estimated_pickup_time: datetime,
    estimated_delivery_time: datetime,
    current_user = Depends(get_current_user)
):
    """Assign a delivery driver to an order."""
    try:
        await tracking_service.assign_delivery(
            order_id=order_id,
            driver_details=driver_details,
            estimated_pickup_time=estimated_pickup_time,
            estimated_delivery_time=estimated_delivery_time
        )
        return {"message": "Delivery assigned successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/tracking/{order_id}/delivery/location")
async def update_driver_location(
    order_id: str,
    location: GeoLocation,
    current_user = Depends(get_current_user)
):
    """Update the current location of the delivery driver."""
    try:
        await tracking_service.update_driver_location(
            order_id=order_id,
            location=location
        )
        return {"message": "Driver location updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/tracking/{order_id}/delivery/complete")
async def mark_order_delivered(
    order_id: str,
    current_user = Depends(get_current_user)
):
    """Mark an order as delivered."""
    try:
        await tracking_service.mark_delivered(
            order_id=order_id
        )
        return {"message": "Order marked as delivered successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "order-tracking"} 