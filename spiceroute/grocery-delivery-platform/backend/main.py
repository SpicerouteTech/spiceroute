from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
from typing import Optional, List, Dict, Any

# Initialize FastAPI app
app = FastAPI(
    title="SpiceRoute.ai API",
    description="Grocery Delivery Platform API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
mongodb_url = os.getenv("MONGODB_URL", "mongodb://spiceroute:spiceroute123@localhost:27017")
mongodb_db_name = os.getenv("MONGODB_DB_NAME", "spiceroute")

# Database instance
db = None

@app.on_event("startup")
async def startup_db_client():
    global db
    mongo_client = AsyncIOMotorClient(mongodb_url)
    db = mongo_client[mongodb_db_name]
    
    # Check MongoDB connection
    try:
        await mongo_client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    global db
    if db:
        db.client.close()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "SpiceRoute.ai API"}

# API root
@app.get("/")
async def root():
    return {
        "message": "Welcome to SpiceRoute.ai API",
        "docs": "/docs",
        "health": "/health"
    }

# Sample endpoints
@app.get("/api/v1/store-owners")
async def get_store_owners():
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    store_owners = await db.store_owners.find().to_list(length=100)
    return {"store_owners": store_owners}

@app.get("/api/v1/orders")
async def get_orders():
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    # Sample data since order collection might not exist yet
    return {
        "orders": [
            {
                "id": "sample_order_1",
                "customer_id": "customer_123",
                "store_id": "store_456",
                "status": "ORDER_RECEIVED",
                "total_amount": 45.99,
                "created_at": "2023-04-07T12:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 