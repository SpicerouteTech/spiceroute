import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile
from PIL import Image
import aiofiles
import uuid
from datetime import datetime

class ImageService:
    def __init__(self):
        self.base_path = Path("data/images")
        self.base_url = "/images"  # Local URL path
        self.sizes = {
            "thumbnail": (150, 150),
            "medium": (300, 300),
            "large": (800, 800)
        }
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        for size in self.sizes.keys():
            (self.base_path / size).mkdir(parents=True, exist_ok=True)

    async def save_image(self, file: UploadFile, product_id: str) -> dict:
        """
        Save an image in multiple sizes and return URLs
        """
        # Generate unique filename
        ext = Path(file.filename).suffix
        filename = f"{product_id}_{uuid.uuid4()}{ext}"
        
        # Save original file temporarily
        temp_path = self.base_path / "temp" / filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Save uploaded file
            async with aiofiles.open(temp_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            # Process images in different sizes
            urls = {}
            with Image.open(temp_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create different sizes
                for size_name, dimensions in self.sizes.items():
                    resized = self._resize_image(img, dimensions)
                    size_path = self.base_path / size_name / filename
                    resized.save(size_path, quality=85, optimize=True)
                    urls[size_name] = f"{self.base_url}/{size_name}/{filename}"

            return {
                "id": filename,
                "urls": urls,
                "original_filename": file.filename,
                "created_at": datetime.utcnow().isoformat()
            }

        finally:
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()

    def _resize_image(self, img: Image.Image, size: tuple[int, int]) -> Image.Image:
        """Resize image maintaining aspect ratio"""
        return img.copy().thumbnail(size, Image.Resampling.LANCZOS)

    async def delete_image(self, image_id: str):
        """Delete all sizes of an image"""
        for size in self.sizes.keys():
            path = self.base_path / size / image_id
            if path.exists():
                path.unlink()

    def get_image_url(self, image_id: str, size: str = "medium") -> Optional[str]:
        """Get URL for an image of specified size"""
        if size not in self.sizes:
            raise ValueError(f"Invalid size: {size}")
        
        path = self.base_path / size / image_id
        if not path.exists():
            return None
            
        return f"{self.base_url}/{size}/{image_id}"

# Create global instance
image_service = ImageService() 