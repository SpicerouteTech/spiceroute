import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import structlog

from db import store_profile_db
from routes import router
from config.settings import Settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

# Load settings
settings = Settings()

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(
            "request_processed",
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration=process_time
        )
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to database with optimized settings
    logger.info("connecting_to_mongodb")
    await store_profile_db.connect_to_mongodb(settings.get_mongodb_options())
    logger.info("mongodb_connected")
    
    # Initialize Redis connection pool
    if settings.REDIS_URL:
        logger.info("connecting_to_redis")
        await store_profile_db.init_redis_pool(
            settings.REDIS_URL,
            settings.REDIS_POOL_SIZE
        )
        logger.info("redis_connected")
    
    yield
    
    # Shutdown: close connections
    logger.info("closing_connections")
    await store_profile_db.close_mongodb_connection()
    if settings.REDIS_URL:
        await store_profile_db.close_redis_pool()
    logger.info("connections_closed")

# Create FastAPI application
app = FastAPI(
    title="Store Profile Service",
    description="API for managing store owner profiles in the grocery delivery platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Add CORS middleware with optimized settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=settings.COMPRESSION_MINIMUM_SIZE
)

# Add performance monitoring middleware
app.add_middleware(PerformanceMiddleware)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Include routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("starting_service")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    ) 