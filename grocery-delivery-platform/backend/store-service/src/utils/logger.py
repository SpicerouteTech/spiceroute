import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add timestamp
        log_record['timestamp'] = datetime.utcnow().isoformat()
        
        # Add log level
        log_record['level'] = record.levelname
        
        # Add source information
        log_record['source'] = {
            'file': record.filename,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add correlation ID if available
        if hasattr(record, 'correlation_id'):
            log_record['correlation_id'] = record.correlation_id


def setup_logging(service_name: str = "store-service", log_level: str = "INFO") -> None:
    """Configure structured JSON logging"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    
    # Create formatter
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    
    # Add formatter to handler
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    # Set basic configuration
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Log initial message
    logger.info(
        "Logging configured",
        extra={
            'service': service_name,
            'log_level': log_level
        }
    )


class LoggerAdapter(logging.LoggerAdapter):
    """Custom logger adapter to add context to log messages"""
    
    def __init__(self, logger: logging.Logger, extra: Dict[str, Any] = None):
        super().__init__(logger, extra or {})
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Process the logging message and keyword arguments"""
        extra = kwargs.get('extra', {})
        
        # Add correlation ID if available
        if 'correlation_id' in self.extra:
            extra['correlation_id'] = self.extra['correlation_id']
        
        # Add any other context
        extra.update(self.extra)
        
        kwargs['extra'] = extra
        return msg, kwargs


def get_logger(name: str, **kwargs: Any) -> LoggerAdapter:
    """Get a logger instance with the given name and context"""
    logger = logging.getLogger(name)
    return LoggerAdapter(logger, kwargs) 