from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class StoreServiceError(Exception):
    """Base exception for store service"""
    def __init__(self, message: str, code: str, status_code: int, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ResourceNotFoundError(StoreServiceError):
    """Raised when a requested resource is not found"""
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found with identifier: {identifier}",
            code="RESOURCE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "identifier": identifier}
        )


class ValidationError(StoreServiceError):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class DatabaseError(StoreServiceError):
    """Raised when database operations fail"""
    def __init__(self, operation: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Database operation failed: {operation}",
            code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class BusinessLogicError(StoreServiceError):
    """Raised when business logic validation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="BUSINESS_LOGIC_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


def error_handler(error: Exception) -> HTTPException:
    """Convert exceptions to HTTPException with proper error response"""
    if isinstance(error, StoreServiceError):
        return HTTPException(
            status_code=error.status_code,
            detail=ErrorResponse(
                code=error.code,
                message=error.message,
                details=error.details
            ).dict()
        )
    
    # Handle unexpected errors
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            details={"error": str(error)}
        ).dict()
    ) 