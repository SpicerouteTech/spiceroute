import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db import catalog_db
from routes import router
from .routes import image_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to database
    logger.info("Connecting to MongoDB...")
    await catalog_db.connect_to_mongodb()
    logger.info("MongoDB connection established")
    
    yield
    
    # Shutdown: close database connection
    logger.info("Closing MongoDB connection...")
    await catalog_db.close_mongodb_connection()
    logger.info("MongoDB connection closed")


# Create FastAPI application
app = FastAPI(
    title="Catalog Service",
    description="API for managing store catalogs in the grocery delivery platform",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


# Include the API router
app.include_router(router, prefix="/api/v1")

# Register routes
app.include_router(image_routes.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint to check if the service is running."""
    return {
        "service": "Catalog Service",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Catalog Service...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 