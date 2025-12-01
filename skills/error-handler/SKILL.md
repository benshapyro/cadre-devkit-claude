---
name: error-handler
description: Provides battle-tested error handling patterns for TypeScript and Python. Use when implementing error handling, creating try/catch blocks, or handling exceptions.
---

# Error Handler Skill

Implements robust error handling patterns that provide meaningful errors, graceful degradation, and proper logging.

## Core Principles

1. **Fail Fast, Fail Loudly** - Catch errors early, make them visible
2. **Context is King** - Include relevant information in error messages
3. **Never Swallow Errors** - Always log, re-throw, or handle explicitly
4. **User-Friendly Messages** - Show generic messages to users, log details server-side
5. **Typed Errors** - Use custom error classes for different failure types

## TypeScript/JavaScript Patterns

### Custom Error Classes

```typescript
// Base error class with context
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific error types
export class ValidationError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, context);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(
      `${resource} not found`,
      'NOT_FOUND',
      404,
      { resource, id }
    );
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

export class DatabaseError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, 'DATABASE_ERROR', 500, context);
  }
}
```

### Function-Level Error Handling

```typescript
// Async function with comprehensive error handling
async function fetchUserData(userId: string): Promise<User> {
  // Input validation
  if (!userId || typeof userId !== 'string') {
    throw new ValidationError('Invalid user ID', { userId });
  }

  try {
    const user = await db.users.findUnique({ where: { id: userId } });

    if (!user) {
      throw new NotFoundError('User', userId);
    }

    return user;
  } catch (error) {
    // Re-throw known errors
    if (error instanceof AppError) {
      throw error;
    }

    // Wrap unknown errors
    throw new DatabaseError('Failed to fetch user', {
      userId,
      originalError: error instanceof Error ? error.message : String(error),
    });
  }
}
```

### API Route Error Handling (Express)

```typescript
// Error handling middleware
function errorHandler(
  err: Error,
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
) {
  // Log error with context
  logger.error('Request error', {
    error: err.message,
    stack: err.stack,
    method: req.method,
    path: req.path,
    userId: req.user?.id,
  });

  // Handle known errors
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        // Don't send context to client (may contain sensitive data)
      },
    });
  }

  // Handle unknown errors (don't leak details)
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
}

// Use in routes
app.get('/api/users/:id', async (req, res, next) => {
  try {
    const user = await fetchUserData(req.params.id);
    res.json({ data: user });
  } catch (error) {
    next(error); // Pass to error handler
  }
});
```

### Async Wrapper for Route Handlers

```typescript
// Eliminates try/catch boilerplate
function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage
app.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await fetchUserData(req.params.id);
  res.json({ data: user });
}));
```

### Promise Error Handling

```typescript
// Always handle rejections
async function processData(data: unknown): Promise<Result> {
  return apiClient
    .post('/process', data)
    .then((response) => response.data)
    .catch((error) => {
      if (error.response?.status === 404) {
        throw new NotFoundError('Endpoint', '/process');
      }
      throw new AppError('Processing failed', 'PROCESS_ERROR', 500, {
        originalError: error.message,
      });
    });
}

// Or with async/await (preferred)
async function processData(data: unknown): Promise<Result> {
  try {
    const response = await apiClient.post('/process', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      throw new NotFoundError('Endpoint', '/process');
    }
    throw new AppError('Processing failed', 'PROCESS_ERROR', 500, {
      originalError: error instanceof Error ? error.message : String(error),
    });
  }
}
```

### React Error Boundaries

```typescript
// Error boundary component
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  state = { hasError: false, error: undefined };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error('React error boundary caught error', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h1>Something went wrong</h1>
          <p>We've been notified and are working on it.</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Python Patterns

### Custom Exception Classes

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

### Function-Level Error Handling

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

### FastAPI Error Handling

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

### Context Managers for Resource Cleanup

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

### Retry Logic with Exponential Backoff

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

## Best Practices

### ✅ DO

- Use custom error classes for different error types
- Include context in errors (but sanitize before sending to client)
- Log errors with structured data (method, path, user ID, etc.)
- Provide user-friendly error messages
- Handle errors at appropriate levels (function, route, global)
- Always clean up resources (use try/finally or context managers)
- Add retry logic for transient failures
- Test error paths (negative tests)

### ❌ DON'T

- Swallow errors silently (`catch (e) {}`)
- Leak sensitive information in error messages
- Use generic error messages without context
- Ignore promise rejections
- Re-throw errors without adding context
- Return errors as values when exceptions are better
- Use errors for control flow

## Error Logging Format

```typescript
// Good logging format
logger.error('Operation failed', {
  error: error.message,
  stack: error.stack,
  context: {
    userId: user.id,
    operation: 'fetchData',
    params: { id: '123' },
  },
});

// Bad logging format
console.log('Error:', error); // Unstructured, hard to query
```

## Testing Error Handling

```typescript
// Test that errors are thrown correctly
test('throws ValidationError for invalid input', async () => {
  await expect(fetchUserData('')).rejects.toThrow(ValidationError);
});

// Test that errors contain proper context
test('includes user ID in NotFoundError', async () => {
  try {
    await fetchUserData('nonexistent');
    fail('Should have thrown');
  } catch (error) {
    expect(error).toBeInstanceOf(NotFoundError);
    expect(error.context).toEqual({
      resource: 'User',
      id: 'nonexistent',
    });
  }
});
```

Remember: Good error handling prevents debugging nightmares and provides a better user experience.
