from pydantic_settings import BaseSettings
from typing import Dict, List

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "catalog"
    
    # Image settings
    UPLOAD_DIR: str = "/tmp/catalog-images"
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    IMAGE_SIZES: Dict[str, tuple] = {
        "thumbnail": (150, 150),
        "small": (300, 300),
        "medium": (600, 600),
        "large": (1200, 1200)
    }
    
    class Config:
        env_file = ".env"

settings = Settings() 