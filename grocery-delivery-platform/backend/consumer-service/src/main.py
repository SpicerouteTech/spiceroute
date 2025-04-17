from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .db import db
from .logging_service import logger

app = FastAPI(
    title="Grocery Delivery Platform Consumer Service",
    description="Authentication and profile management service for consumers",
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

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Setup database indexes
        await db.setup_indexes()
        # Setup Elasticsearch index
        await logger.setup_index()
        await logger.log("INFO", "Consumer service started successfully")
    except Exception as e:
        print(f"Failed to initialize services: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        await db.close()
        await logger.log("INFO", "Consumer service shut down successfully")
    except Exception as e:
        print(f"Error during shutdown: {str(e)}")

# Include routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 