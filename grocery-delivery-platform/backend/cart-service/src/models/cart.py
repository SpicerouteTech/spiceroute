from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class CartItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    store_id: str = Field(..., description="ID of the store this product belongs to")
    quantity: int = Field(..., ge=1, description="Quantity of the product")
    unit_price: float = Field(..., gt=0, description="Price per unit")
    name: str = Field(..., description="Product name")
    image_url: Optional[str] = Field(None, description="Product image URL")
    
    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), description="Cart ID")
    session_id: str = Field(..., description="Session ID for the cart")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    items: List[CartItem] = Field(default_factory=list, description="Items in the cart")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(..., description="Cart expiration timestamp")
    
    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)
    
    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)
    
    @property
    def stores(self) -> List[str]:
        """Get unique store IDs in the cart"""
        return list(set(item.store_id for item in self.items))
    
    def add_item(self, item: CartItem) -> None:
        """Add or update item in cart"""
        # Check if item from same store exists
        existing_item = next(
            (i for i in self.items if i.product_id == item.product_id),
            None
        )
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            self.items.append(item)
        self.updated_at = datetime.utcnow()
    
    def remove_item(self, product_id: str) -> None:
        """Remove item from cart"""
        self.items = [i for i in self.items if i.product_id != product_id]
        self.updated_at = datetime.utcnow()
    
    def update_item_quantity(self, product_id: str, quantity: int) -> None:
        """Update item quantity"""
        for item in self.items:
            if item.product_id == product_id:
                item.quantity = quantity
                self.updated_at = datetime.utcnow()
                break
    
    def clear(self) -> None:
        """Clear all items from cart"""
        self.items = []
        self.updated_at = datetime.utcnow() 