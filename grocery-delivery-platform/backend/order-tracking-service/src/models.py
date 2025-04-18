from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class OrderTrackingStatus(str, Enum):
    """Enum representing possible order tracking statuses."""
    SUBMITTED = "submitted"
    STORE_NOTIFIED = "store_notified"
    STORE_ACKNOWLEDGED = "store_acknowledged"
    PICKING_IN_PROGRESS = "picking_in_progress"
    SUBSTITUTIONS_NEEDED = "substitutions_needed"
    SUBSTITUTIONS_APPROVED = "substitutions_approved"
    PACKING_IN_PROGRESS = "packing_in_progress"
    READY_FOR_PICKUP = "ready_for_pickup"
    DRIVER_ASSIGNED = "driver_assigned"
    DRIVER_EN_ROUTE_TO_STORE = "driver_en_route_to_store"
    DRIVER_ARRIVED_AT_STORE = "driver_arrived_at_store"
    DRIVER_PICKUP_COMPLETE = "driver_pickup_complete"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"

class DeliveryProvider(str, Enum):
    """Enum representing supported delivery providers."""
    UBER = "uber"
    DOORDASH = "doordash"
    INTERNAL = "internal"

class GeoLocation(BaseModel):
    """Model representing a geographical location."""
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    accuracy: Optional[float] = Field(None, description="Accuracy of the location in meters")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the location update")

class DriverDetails(BaseModel):
    """Model representing delivery driver details."""
    driver_id: str = Field(..., description="Unique identifier for the driver")
    name: str = Field(..., description="Driver's name")
    phone: Optional[str] = Field(None, description="Driver's contact number")
    vehicle_type: Optional[str] = Field(None, description="Type of vehicle being used")
    vehicle_id: Optional[str] = Field(None, description="Vehicle identifier (license plate, etc.)")
    photo_url: Optional[str] = Field(None, description="URL to driver's photo")
    rating: Optional[float] = Field(None, description="Driver's rating")

class ItemSubstitution(BaseModel):
    """Model representing an item substitution."""
    original_item_id: str = Field(..., description="ID of the original item")
    original_item_name: str = Field(..., description="Name of the original item")
    substitute_item_id: str = Field(..., description="ID of the substitute item")
    substitute_item_name: str = Field(..., description="Name of the substitute item")
    price_difference: float = Field(..., description="Price difference between original and substitute")
    reason: str = Field(..., description="Reason for substitution")
    customer_approved: Optional[bool] = Field(None, description="Whether customer approved the substitution")

class OrderStatusUpdate(BaseModel):
    """Model representing a status update in the order tracking history."""
    status: OrderTrackingStatus = Field(..., description="Status of the order")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of the status update")
    updated_by: str = Field(..., description="Entity that updated the status")
    notes: Optional[str] = Field(None, description="Additional notes about the status update")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the status update")

class OrderTracking(BaseModel):
    """Main model for order tracking."""
    order_id: str = Field(..., description="Unique identifier for the order")
    store_id: str = Field(..., description="ID of the store fulfilling the order")
    customer_id: str = Field(..., description="ID of the customer who placed the order")
    delivery_provider: DeliveryProvider = Field(..., description="Selected delivery provider")
    current_status: OrderTrackingStatus = Field(..., description="Current status of the order")
    status_history: List[OrderStatusUpdate] = Field(default_factory=list, description="History of status updates")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Time when tracking was initialized")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Time of last update")
    
    store_acknowledgment_time: Optional[datetime] = Field(None, description="Time when store acknowledged the order")
    estimated_preparation_time: Optional[int] = Field(None, description="Estimated preparation time in minutes")
    estimated_pickup_time: Optional[datetime] = Field(None, description="Estimated time for driver pickup")
    estimated_delivery_time: Optional[datetime] = Field(None, description="Estimated time of delivery")
    actual_delivery_time: Optional[datetime] = Field(None, description="Actual time of delivery")
    
    driver_details: Optional[DriverDetails] = Field(None, description="Details of assigned driver")
    driver_location: Optional[GeoLocation] = Field(None, description="Current location of the driver")
    
    substitutions: List[ItemSubstitution] = Field(default_factory=list, description="List of item substitutions")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the order tracking")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 