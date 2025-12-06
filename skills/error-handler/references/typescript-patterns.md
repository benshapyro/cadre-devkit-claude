# TypeScript/JavaScript Error Handling Patterns

## Custom Error Classes

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

## Function-Level Error Handling

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

## Express Error Handling

### Error Middleware

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

### Async Wrapper

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

## Promise Error Handling

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

## React Error Boundaries

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
