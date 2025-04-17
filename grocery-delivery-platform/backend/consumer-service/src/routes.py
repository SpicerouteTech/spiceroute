from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from .models import Token, Consumer, Address, PaymentMethod, Cart, CartItem, Order, OrderStatus
from .auth import auth_service
from .db import db
import uuid

router = APIRouter()

# Authentication routes
@router.post("/auth/google", response_model=Token)
async def login_with_google(token: str):
    """Authenticate consumer with Google"""
    return await auth_service.authenticate_google(token)

@router.post("/auth/facebook", response_model=Token)
async def login_with_facebook(token: str):
    """Authenticate consumer with Facebook"""
    return await auth_service.authenticate_facebook(token)

@router.get("/me", response_model=Consumer)
async def get_current_user(current_user: Consumer = Depends(auth_service.get_current_user)):
    """Get current consumer profile"""
    return current_user

# Profile management routes
@router.post("/me/addresses", response_model=bool)
async def add_address(
    address: Address,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Add a new delivery address"""
    return await db.add_address(current_user.email, address)

@router.post("/me/payment-methods", response_model=bool)
async def add_payment_method(
    payment: PaymentMethod,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Add a new payment method"""
    return await db.add_payment_method(current_user.email, payment)

@router.put("/me/addresses/{index}/default")
async def set_default_address(
    index: int,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Set an address as default"""
    if index < 0 or index >= len(current_user.addresses):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    # Update all addresses to non-default
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$set": {"addresses.$[].is_default": False}}
    )
    
    # Set the selected address as default
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$set": {f"addresses.{index}.is_default": True}}
    )
    
    return {"message": "Default address updated successfully"}

@router.put("/me/payment-methods/{index}/default")
async def set_default_payment(
    index: int,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Set a payment method as default"""
    if index < 0 or index >= len(current_user.payment_methods):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    
    # Update all payment methods to non-default
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$set": {"payment_methods.$[].is_default": False}}
    )
    
    # Set the selected payment method as default
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$set": {f"payment_methods.{index}.is_default": True}}
    )
    
    return {"message": "Default payment method updated successfully"}

@router.delete("/me/addresses/{index}")
async def delete_address(
    index: int,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Delete a delivery address"""
    if index < 0 or index >= len(current_user.addresses):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$unset": {f"addresses.{index}": 1}}
    )
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$pull": {"addresses": None}}
    )
    
    return {"message": "Address deleted successfully"}

@router.delete("/me/payment-methods/{index}")
async def delete_payment_method(
    index: int,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Delete a payment method"""
    if index < 0 or index >= len(current_user.payment_methods):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$unset": {f"payment_methods.{index}": 1}}
    )
    await db.consumers.update_one(
        {"email": current_user.email},
        {"$pull": {"payment_methods": None}}
    )
    
    return {"message": "Payment method deleted successfully"}

# Profile update route
@router.put("/me", response_model=Consumer)
async def update_profile(
    updates: dict,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Update consumer profile"""
    allowed_fields = {"name", "phone", "picture"}
    update_data = {k: v for k, v in updates.items() if k in allowed_fields}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    
    result = await db.consumers.update_one(
        {"email": current_user.email},
        {"$set": update_data}
    )
    
    if result.modified_count:
        updated_user = await db.get_consumer_by_email(current_user.email)
        return updated_user
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Profile update failed"
    )

# Shopping routes
@router.get("/cart", response_model=Optional[Cart])
async def get_cart(current_user: Consumer = Depends(auth_service.get_current_user)):
    """Get current user's shopping cart"""
    return current_user.cart

@router.post("/cart/items")
async def add_to_cart(
    product_id: str,
    quantity: int = Query(..., gt=0),
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Add item to cart"""
    # Get product details
    product = await db.get_product_details(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Create or update cart
    cart = current_user.cart or Cart()
    
    # Check if item already exists in cart
    for item in cart.items:
        if item.product_id == product_id:
            item.quantity += quantity
            break
    else:
        # Add new item
        cart.items.append(CartItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=product["price"],
            name=product["name"],
            image_url=product.get("image_url")
        ))
    
    # Update cart
    await db.update_cart(current_user.email, cart)
    return {"message": "Item added to cart"}

@router.put("/cart/items/{product_id}")
async def update_cart_item(
    product_id: str,
    quantity: int = Query(..., gt=0),
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Update item quantity in cart"""
    if not current_user.cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart is empty"
        )
    
    # Find and update item
    for item in current_user.cart.items:
        if item.product_id == product_id:
            item.quantity = quantity
            await db.update_cart(current_user.email, current_user.cart)
            return {"message": "Cart updated"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found in cart"
    )

@router.delete("/cart/items/{product_id}")
async def remove_from_cart(
    product_id: str,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Remove item from cart"""
    if not current_user.cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart is empty"
        )
    
    # Remove item
    current_user.cart.items = [
        item for item in current_user.cart.items
        if item.product_id != product_id
    ]
    
    if not current_user.cart.items:
        # Clear cart if empty
        await db.clear_cart(current_user.email)
        return {"message": "Cart cleared"}
    
    # Update cart
    await db.update_cart(current_user.email, current_user.cart)
    return {"message": "Item removed from cart"}

@router.post("/orders", response_model=Order)
async def create_order(
    address_index: int = Query(..., ge=0),
    payment_index: int = Query(..., ge=0),
    delivery_notes: Optional[str] = None,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Create a new order from cart"""
    if not current_user.cart or not current_user.cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    if address_index >= len(current_user.addresses):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid delivery address"
        )
    
    if payment_index >= len(current_user.payment_methods):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment method"
        )
    
    # Create order
    order = Order(
        order_id=str(uuid.uuid4()),
        consumer_email=current_user.email,
        items=current_user.cart.items,
        total_amount=current_user.cart.total,
        delivery_address=current_user.addresses[address_index],
        payment_method=current_user.payment_methods[payment_index],
        status=OrderStatus.PENDING,
        delivery_notes=delivery_notes
    )
    
    # Save order and clear cart
    order_id = await db.create_order(order)
    order.order_id = order_id
    return order

@router.get("/orders", response_model=List[Order])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """List user's orders"""
    return await db.get_consumer_orders(current_user.email, limit, skip)

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Get order details"""
    order = await db.get_order(order_id)
    if not order or order.consumer_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.post("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: str,
    current_user: Consumer = Depends(auth_service.get_current_user)
):
    """Cancel an order"""
    order = await db.get_order(order_id)
    if not order or order.consumer_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled"
        )
    
    await db.update_order_status(order_id, OrderStatus.CANCELLED)
    return {"message": "Order cancelled successfully"} 