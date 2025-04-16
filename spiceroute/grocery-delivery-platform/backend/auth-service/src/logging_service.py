from elasticsearch import AsyncElasticsearch
from datetime import datetime
import uuid
import os
from .models import ErrorLog

class LoggingService:
    def __init__(self):
        self.es = AsyncElasticsearch([os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")])
        self.index_name = "auth-service-logs"

    async def setup_index(self):
        """Create index with mapping if it doesn't exist"""
        mapping = {
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date"},
                    "level": {"type": "keyword"},
                    "service": {"type": "keyword"},
                    "message": {"type": "text"},
                    "details": {"type": "object"},
                    "trace_id": {"type": "keyword"}
                }
            },
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            }
        }
        
        if not await self.es.indices.exists(index=self.index_name):
            await self.es.indices.create(index=self.index_name, body=mapping)

    async def log(self, level: str, message: str, details: dict = None):
        """Log a message to Elasticsearch"""
        log_entry = ErrorLog(
            level=level,
            message=message,
            details=details,
            trace_id=str(uuid.uuid4())
        )
        
        try:
            await self.es.index(
                index=self.index_name,
                document=log_entry.dict(),
                refresh=True
            )
        except Exception as e:
            # Fallback to console logging if Elasticsearch is unavailable
            print(f"Failed to log to Elasticsearch: {str(e)}")
            print(f"Log entry: {log_entry.dict()}")

    async def close(self):
        """Close Elasticsearch connection"""
        await self.es.close()

# Global logging service instance
logger = LoggingService() 