from typing import Optional
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
    
    # MongoDB settings
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    MONGODB_DB_NAME: str = Field("spiceroute", env="MONGODB_DB_NAME")
    
    # Redis settings (for caching)
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")
    
    # Cache settings
    CACHE_TTL: int = Field(3600, env="CACHE_TTL")  # Default 1 hour
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = Field(50, env="DEFAULT_PAGE_SIZE")
    MAX_PAGE_SIZE: int = Field(100, env="MAX_PAGE_SIZE")
    
    # Security
    CORS_ORIGINS: list = Field(["*"], env="CORS_ORIGINS")
    
    # Rate limiting
    RATE_LIMIT_PER_SECOND: int = Field(10, env="RATE_LIMIT_PER_SECOND")
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create a global settings instance
settings = get_settings() 