from typing import Any, Optional


class BaseAppException(Exception):
    """Base exception for all application exceptions."""

    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 500,
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(BaseAppException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str = "Resource", resource_id: Any = None):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=message, status_code=404)


class BadRequestException(BaseAppException):
    """Raised for invalid request data."""

    def __init__(self, message: str = "Bad request", details: Optional[Any] = None):
        super().__init__(message=message, status_code=400, details=details)


class UnauthorizedException(BaseAppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=401)


class ForbiddenException(BaseAppException):
    """Raised when user lacks permission."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message=message, status_code=403)


class ConflictException(BaseAppException):
    """Raised when there's a conflict (e.g., duplicate resource)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=409)


class ValidationException(BaseAppException):
    """Raised for validation errors."""

    def __init__(self, message: str = "Validation error", details: Optional[Any] = None):
        super().__init__(message=message, status_code=422, details=details)


class DatabaseException(BaseAppException):
    """Raised for database-related errors."""

    def __init__(self, message: str = "Database error"):
        super().__init__(message=message, status_code=500)
