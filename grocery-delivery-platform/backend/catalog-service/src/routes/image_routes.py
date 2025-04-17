from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import aiofiles
import os
import uuid
from PIL import Image
import io
import shutil

from ..config import settings
from ..auth import get_current_user
from ..models import StoreOwner
from ..db import db

router = APIRouter(prefix="/images", tags=["images"])

async def save_image(image_data: bytes, image_id: str, size_name: str, size: tuple) -> str:
    """Save image with specified dimensions and return the file path."""
    try:
        # Create size directory if it doesn't exist
        size_dir = os.path.join(settings.UPLOAD_DIR, size_name)
        os.makedirs(size_dir, exist_ok=True)
        
        # Resize image
        img = Image.open(io.BytesIO(image_data))
        img = img.convert('RGB')  # Convert to RGB to ensure JPEG compatibility
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save resized image
        file_path = os.path.join(size_dir, f"{image_id}.jpg")
        img.save(file_path, "JPEG", quality=85)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

async def process_image(image_data: bytes, image_id: str):
    """Process and save image in all required sizes."""
    for size_name, dimensions in settings.IMAGE_SIZES.items():
        await save_image(image_data, image_id, size_name, dimensions)

@router.post("/upload/{product_id}")
async def upload_image(
    product_id: str,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    current_user: StoreOwner = Depends(get_current_user)
) -> dict:
    """Upload a product image and create variants in different sizes."""
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Read file content
    content = await file.read()
    if len(content) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Verify product ownership
    product = await db.get_product(product_id)
    if not product or str(product.store_id) != str(current_user.store_id):
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Generate unique image ID
    image_id = str(uuid.uuid4())
    
    # Process image in background
    background_tasks.add_task(process_image, content, image_id)
    
    # Update product with image ID
    await db.update_product(product_id, {"image_id": image_id})
    
    # Return image URLs for all sizes
    return {
        size: f"/images/{size}/{image_id}" 
        for size in settings.IMAGE_SIZES.keys()
    }

@router.delete("/{image_id}")
async def delete_image(
    image_id: str,
    current_user: StoreOwner = Depends(get_current_user)
) -> dict:
    """Delete an image and all its size variants."""
    
    # Verify image ownership through product
    product = await db.get_product_by_image(image_id)
    if not product or str(product.store_id) != str(current_user.store_id):
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Delete all size variants
    for size_name in settings.IMAGE_SIZES.keys():
        file_path = os.path.join(settings.UPLOAD_DIR, size_name, f"{image_id}.jpg")
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass  # Ignore if file doesn't exist
    
    # Update product to remove image reference
    await db.update_product(str(product.id), {"image_id": None})
    
    return {"message": "Image deleted successfully"}

@router.get("/{size}/{image_id}")
async def get_image(size: str, image_id: str):
    """Retrieve an image in the specified size."""
    if size not in settings.IMAGE_SIZES:
        raise HTTPException(status_code=400, detail="Invalid size")
    
    file_path = os.path.join(settings.UPLOAD_DIR, size, f"{image_id}.jpg")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path, media_type="image/jpeg") 