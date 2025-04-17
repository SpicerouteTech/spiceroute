import json
from typing import Any, Optional, Union
from redis.asyncio import Redis
from functools import wraps
import pickle
from datetime import timedelta

from ..config.settings import settings
from .logger import get_logger

logger = get_logger(__name__)


class AsyncRedisCache:
    def __init__(self):
        self.redis: Optional[Redis] = None
    
    async def init(self) -> None:
        """Initialize Redis connection"""
        if settings.REDIS_URL:
            self.redis = Redis.from_url(
                settings.REDIS_URL,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            try:
                await self.redis.ping()
                logger.info("Redis connection established")
            except Exception as e:
                logger.error(f"Redis connection failed: {str(e)}")
                self.redis = None
    
    async def close(self) -> None:
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            return None
        
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Set value in cache"""
        if not self.redis:
            return False
        
        try:
            await self.redis.set(
                key,
                json.dumps(value),
                ex=expire or settings.CACHE_TTL
            )
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.redis:
            return False
        
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {str(e)}")
            return False
    
    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern"""
        if not self.redis:
            return False
        
        try:
            cursor = 0
            while True:
                cursor, keys = await self.redis.scan(cursor, match=pattern)
                if keys:
                    await self.redis.delete(*keys)
                if cursor == 0:
                    break
            return True
        except Exception as e:
            logger.error(f"Error clearing cache pattern: {str(e)}")
            return False


# Create global cache instance
cache = AsyncRedisCache()


def cached(
    key_prefix: str,
    expire: Optional[int] = None,
    include_args: bool = True
):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}"
            if include_args:
                args_str = ":".join(str(arg) for arg in args[1:])  # Skip self
                kwargs_str = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                if args_str:
                    cache_key += f":{args_str}"
                if kwargs_str:
                    cache_key += f":{kwargs_str}"
            
            # Try to get from cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_value
            
            # If not in cache, execute function
            logger.debug(f"Cache miss for key: {cache_key}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            await cache.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator 