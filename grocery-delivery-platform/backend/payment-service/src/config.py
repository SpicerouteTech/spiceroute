from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "payments"
    
    # Toast API settings
    TOAST_API_URL: str = "https://api.toasttab.com/v1"
    TOAST_API_KEY: str
    TOAST_WEBHOOK_SECRET: str
    
    # Payment settings
    PLATFORM_FEE_RATE: float = 0.05  # 5% platform fee
    TAX_RATE: float = 0.08  # 8% tax rate
    MIN_PAYOUT_AMOUNT: float = 1.00  # Minimum amount for payouts
    PAYOUT_SCHEDULE_HOURS: int = 24  # Process payouts every 24 hours
    
    # Security settings
    API_KEY_HEADER: str = "X-API-Key"
    WEBHOOK_SIGNATURE_HEADER: str = "X-Toast-Signature"
    
    class Config:
        env_file = ".env"

settings = Settings() 