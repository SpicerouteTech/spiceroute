from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, validator
from functools import lru_cache


class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str = "store-service"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(False, env="DEBUG")
    
    # Server settings
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    WORKERS: int = Field(4, env="WORKERS")  # Number of Gunicorn workers
    WORKER_CLASS: str = Field("uvicorn.workers.UvicornWorker", env="WORKER_CLASS")
    
    # MongoDB settings
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    MONGODB_DB_NAME: str = Field("spiceroute", env="MONGODB_DB_NAME")
    MONGODB_MAX_POOL_SIZE: int = Field(100, env="MONGODB_MAX_POOL_SIZE")
    MONGODB_MIN_POOL_SIZE: int = Field(10, env="MONGODB_MIN_POOL_SIZE")
    MONGODB_MAX_IDLE_TIME_MS: int = Field(10000, env="MONGODB_MAX_IDLE_TIME_MS")
    
    # Redis settings (for caching)
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")
    REDIS_POOL_SIZE: int = Field(100, env="REDIS_POOL_SIZE")
    
    # Cache settings
    CACHE_TTL: int = Field(3600, env="CACHE_TTL")  # Default 1 hour
    CACHE_PREFIX: str = Field("store_service:", env="CACHE_PREFIX")
    
    # Performance settings
    COMPRESSION_MINIMUM_SIZE: int = Field(1000, env="COMPRESSION_MINIMUM_SIZE")  # in bytes
    BATCH_SIZE: int = Field(100, env="BATCH_SIZE")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = Field(50, env="DEFAULT_PAGE_SIZE")
    MAX_PAGE_SIZE: int = Field(100, env="MAX_PAGE_SIZE")
    
    # Security
    CORS_ORIGINS: list = Field(["*"], env="CORS_ORIGINS")
    CORS_ALLOW_CREDENTIALS: bool = Field(True, env="CORS_ALLOW_CREDENTIALS")
    
    # Rate limiting
    RATE_LIMIT_PER_SECOND: int = Field(10, env="RATE_LIMIT_PER_SECOND")
    RATE_LIMIT_BURST: int = Field(20, env="RATE_LIMIT_BURST")
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v: str) -> str:
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of {allowed_levels}")
        return v.upper()
    
    @validator("MONGODB_URL")
    def validate_mongodb_url(cls, v: str) -> str:
        if not v.startswith(("mongodb://", "mongodb+srv://")):
            raise ValueError("Invalid MongoDB URL format")
        return v
    
    def get_mongodb_options(self) -> Dict[str, Any]:
        """Get MongoDB connection options with optimized settings"""
        return {
            "maxPoolSize": self.MONGODB_MAX_POOL_SIZE,
            "minPoolSize": self.MONGODB_MIN_POOL_SIZE,
            "maxIdleTimeMS": self.MONGODB_MAX_IDLE_TIME_MS,
            "retryWrites": True,
            "w": "majority",  # Write concern
            "readPreference": "secondaryPreferred",  # Read preference
            "connectTimeoutMS": 5000,
            "serverSelectionTimeoutMS": 5000,
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create a global settings instance
settings = get_settings() 