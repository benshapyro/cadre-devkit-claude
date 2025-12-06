# Python Error Handling Patterns

## Custom Exception Classes

```python
# Base exception with context
class AppError(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        context: dict | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message, "VALIDATION_ERROR", 400, context)


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            f"{resource} not found",
            "NOT_FOUND",
            404,
            {"resource": resource, "id": resource_id},
        )


class DatabaseError(AppError):
    """Raised when database operations fail."""

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message, "DATABASE_ERROR", 500, context)
```

## Function-Level Error Handling

```python
# Comprehensive error handling in functions
async def fetch_user_data(user_id: str) -> User:
    """Fetch user data with comprehensive error handling."""

    # Input validation
    if not user_id or not isinstance(user_id, str):
        raise ValidationError("Invalid user ID", {"user_id": user_id})

    try:
        user = await db.users.find_unique(where={"id": user_id})

        if user is None:
            raise NotFoundError("User", user_id)

        return user

    except AppError:
        # Re-raise known errors
        raise

    except Exception as e:
        # Wrap unknown errors
        raise DatabaseError(
            "Failed to fetch user",
            {"user_id": user_id, "original_error": str(e)},
        ) from e
```

## FastAPI Error Handling

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Custom exception handler
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle application errors."""

    # Log error with context
    logger.error(
        "Request error",
        extra={
            "error": exc.message,
            "code": exc.code,
            "method": request.method,
            "path": request.url.path,
            "context": exc.context,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )

# Handle validation errors
@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors(),
            }
        },
    )

# Handle unexpected errors
@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    """Handle unexpected errors (don't leak details)."""

    logger.exception(
        "Unexpected error",
        extra={
            "method": request.method,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )
```

## Context Managers for Resource Cleanup

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_transaction():
    """Context manager for database transactions."""

    transaction = await db.begin()
    try:
        yield transaction
        await transaction.commit()
    except Exception as e:
        await transaction.rollback()
        logger.error("Transaction rolled back", extra={"error": str(e)})
        raise
    finally:
        await transaction.close()

# Usage
async def create_user(user_data: dict) -> User:
    async with database_transaction() as txn:
        user = await txn.users.create(data=user_data)
        await txn.audit_log.create(data={"action": "user_created"})
        return user
```

## Retry Logic with Exponential Backoff

```python
import asyncio
from functools import wraps

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """Retry decorator with exponential backoff."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        # Last attempt, raise the error
                        raise

                    wait_time = backoff_factor ** attempt
                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {wait_time}s",
                        extra={"error": str(e)},
                    )
                    await asyncio.sleep(wait_time)

        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, exceptions=(DatabaseError,))
async def fetch_with_retry(url: str):
    return await api_client.get(url)
```

## Flask Error Handling

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(AppError)
def handle_app_error(error):
    """Handle application errors."""
    logger.error(
        "Request error",
        extra={
            "error": error.message,
            "code": error.code,
            "context": error.context,
        },
    )

    return jsonify({
        "error": {
            "code": error.code,
            "message": error.message,
        }
    }), error.status_code

@app.errorhandler(Exception)
def handle_generic_error(error):
    """Handle unexpected errors."""
    logger.exception("Unexpected error")

    return jsonify({
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
        }
    }), 500
```
