from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Dict, Any
from bson import ObjectId

from models import CatalogItem, CatalogItemUpdate, PaginatedResponse
from db import catalog_db

# Setup OAuth2 with Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter()


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Get the current user ID from the JWT token.
    In a production environment, this would validate the token with the auth service.
    """
    # For now, we'll just extract the user ID from the token payload
    # In a real implementation, this would decode and verify the JWT
    try:
        # Simulated extraction for now
        # In production, this would decode the JWT and validate it properly
        user_id = token.split("|")[1] if "|" in token else token
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Admin middleware to verify store ownership would be implemented here
# For now, we'll check ownership manually in each endpoint that requires it


@router.post("/items", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_item(item: CatalogItem, _: str = Depends(get_current_user_id)):
    """Create a new catalog item. Requires authentication."""
    # In a real implementation, we would verify that the user owns the store_id in the item
    created_item = await catalog_db.create_item(item)
    return created_item


@router.get("/items/{item_id}", response_model=Dict[str, Any])
async def get_item(item_id: str = Path(..., description="The ID of the item to get")):
    """Get a catalog item by ID. Public access."""
    return await catalog_db.get_item_by_id(item_id)


@router.put("/items/{item_id}", response_model=Dict[str, Any])
async def update_item(
    update_data: CatalogItemUpdate,
    item_id: str = Path(..., description="The ID of the item to update"),
    _: str = Depends(get_current_user_id)
):
    """Update a catalog item. Requires authentication."""
    # In a real implementation, we would verify that the user owns the store that owns this item
    return await catalog_db.update_item(item_id, update_data)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str = Path(..., description="The ID of the item to delete"),
    _: str = Depends(get_current_user_id)
):
    """Delete a catalog item. Requires authentication."""
    # In a real implementation, we would verify that the user owns the store that owns this item
    await catalog_db.delete_item(item_id)


@router.get("/items", response_model=PaginatedResponse)
async def list_items(
    skip: int = Query(0, ge=0, description="Skip the first n results"),
    limit: int = Query(20, ge=1, le=100, description="Limit the number of results"),
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    is_organic: Optional[bool] = Query(None, description="Filter by organic status"),
    is_vegan: Optional[bool] = Query(None, description="Filter by vegan status"),
    is_gluten_free: Optional[bool] = Query(None, description="Filter by gluten-free status"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_desc: bool = Query(True, description="Sort in descending order")
):
    """List catalog items with pagination, filtering, and sorting. Public access."""
    # Build filters based on query parameters
    filters = {}
    
    if category:
        filters["category"] = category
    if subcategory:
        filters["subcategory"] = subcategory
    if is_organic is not None:
        filters["is_organic"] = is_organic
    if is_vegan is not None:
        filters["is_vegan"] = is_vegan
    if is_gluten_free is not None:
        filters["is_gluten_free"] = is_gluten_free
        
    # Price range
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        filters["price"] = price_filter
    
    # Get items with filters, pagination, and sorting
    return await catalog_db.list_items(skip, limit, filters, sort_by, sort_desc)


@router.get("/stores/{store_id}/items", response_model=PaginatedResponse)
async def get_store_items(
    store_id: str = Path(..., description="The ID of the store"),
    skip: int = Query(0, ge=0, description="Skip the first n results"),
    limit: int = Query(20, ge=1, le=100, description="Limit the number of results"),
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    is_organic: Optional[bool] = Query(None, description="Filter by organic status"),
    is_vegan: Optional[bool] = Query(None, description="Filter by vegan status"),
    is_gluten_free: Optional[bool] = Query(None, description="Filter by gluten-free status"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_desc: bool = Query(True, description="Sort in descending order")
):
    """Get all items for a specific store with pagination, filtering, and sorting. Public access."""
    # Build filters based on query parameters
    filters = {}
    
    if category:
        filters["category"] = category
    if subcategory:
        filters["subcategory"] = subcategory
    if is_organic is not None:
        filters["is_organic"] = is_organic
    if is_vegan is not None:
        filters["is_vegan"] = is_vegan
    if is_gluten_free is not None:
        filters["is_gluten_free"] = is_gluten_free
        
    # Price range
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        filters["price"] = price_filter
    
    # Get items with filters, pagination, and sorting
    return await catalog_db.get_store_items(store_id, skip, limit, filters, sort_by, sort_desc)


@router.get("/search", response_model=PaginatedResponse)
async def search_items(
    q: str = Query(..., description="Search query"),
    store_id: Optional[str] = Query(None, description="Filter by store ID"),
    skip: int = Query(0, ge=0, description="Skip the first n results"),
    limit: int = Query(20, ge=1, le=100, description="Limit the number of results")
):
    """Search catalog items by text. Public access."""
    return await catalog_db.search_items(q, store_id, skip, limit)


@router.get("/featured", response_model=List[Dict[str, Any]])
async def get_featured_items(
    store_id: Optional[str] = Query(None, description="Filter by store ID"),
    limit: int = Query(10, ge=1, le=50, description="Limit the number of results")
):
    """Get featured items, optionally filtered by store. Public access."""
    return await catalog_db.get_featured_items(store_id, limit)


@router.put("/items/{item_id}/stock", response_model=Dict[str, Any])
async def update_item_stock(
    item_id: str = Path(..., description="The ID of the item to update"),
    quantity_change: int = Query(..., description="Quantity to add (positive) or subtract (negative)"),
    _: str = Depends(get_current_user_id)
):
    """Update the stock quantity of an item. Requires authentication."""
    # In a real implementation, we would verify that the user owns the store that owns this item
    return await catalog_db.update_stock(item_id, quantity_change)


@router.get("/health", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "catalog-service"} 