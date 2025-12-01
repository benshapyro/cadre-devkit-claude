# Express.js API Examples

## Basic CRUD API

```typescript
import express, { Router } from 'express';
import { z } from 'zod';

const router = Router();

// Validation schemas
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

const updateUserSchema = createUserSchema.partial();

// List users with pagination
router.get('/users', async (req, res, next) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const perPage = parseInt(req.query.perPage as string) || 20;
    const offset = (page - 1) * perPage;

    const [users, total] = await Promise.all([
      db.user.findMany({ skip: offset, take: perPage }),
      db.user.count(),
    ]);

    res.json({
      data: users,
      meta: {
        total,
        page,
        perPage,
        totalPages: Math.ceil(total / perPage),
      },
      links: {
        first: `/api/v1/users?page=1&perPage=${perPage}`,
        prev: page > 1 ? `/api/v1/users?page=${page - 1}&perPage=${perPage}` : null,
        next: page < Math.ceil(total / perPage) ? `/api/v1/users?page=${page + 1}&perPage=${perPage}` : null,
        last: `/api/v1/users?page=${Math.ceil(total / perPage)}&perPage=${perPage}`,
      },
    });
  } catch (error) {
    next(error);
  }
});

// Get single user
router.get('/users/:id', async (req, res, next) => {
  try {
    const user = await db.user.findUnique({ where: { id: req.params.id } });

    if (!user) {
      return res.status(404).json({
        error: {
          code: 'NOT_FOUND',
          message: 'User not found',
        },
      });
    }

    res.json({ data: user });
  } catch (error) {
    next(error);
  }
});

// Create user
router.post('/users', async (req, res, next) => {
  try {
    const validatedData = createUserSchema.parse(req.body);

    const existing = await db.user.findUnique({
      where: { email: validatedData.email },
    });

    if (existing) {
      return res.status(409).json({
        error: {
          code: 'DUPLICATE',
          message: 'User with this email already exists',
        },
      });
    }

    const user = await db.user.create({ data: validatedData });
    res.status(201).json({ data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input data',
          details: error.errors,
        },
      });
    }
    next(error);
  }
});

// Update user (partial)
router.patch('/users/:id', async (req, res, next) => {
  try {
    const validatedData = updateUserSchema.parse(req.body);

    const user = await db.user.update({
      where: { id: req.params.id },
      data: validatedData,
    });

    res.json({ data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input data',
          details: error.errors,
        },
      });
    }
    next(error);
  }
});

// Delete user
router.delete('/users/:id', async (req, res, next) => {
  try {
    await db.user.delete({ where: { id: req.params.id } });
    res.status(204).send();
  } catch (error) {
    next(error);
  }
});

export default router;
```

## Middleware Patterns

```typescript
// Authentication middleware
function requireAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({
      error: { code: 'UNAUTHORIZED', message: 'Authentication required' },
    });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' },
    });
  }
}

// Authorization middleware
function requireRole(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      });
    }
    next();
  };
}

// Rate limiting
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later',
    },
  },
});

// Usage
app.use('/api/', limiter);
router.get('/users', requireAuth, async (req, res) => { /* ... */ });
router.delete('/users/:id', requireAuth, requireRole('admin'), async (req, res) => { /* ... */ });
```

## Testing

```typescript
import request from 'supertest';
import app from './app';

describe('GET /api/v1/users', () => {
  it('returns paginated users', async () => {
    const response = await request(app)
      .get('/api/v1/users?page=1&perPage=10')
      .expect(200);

    expect(response.body).toHaveProperty('data');
    expect(response.body).toHaveProperty('meta');
    expect(response.body.meta.page).toBe(1);
  });

  it('returns 401 without auth token', async () => {
    await request(app)
      .get('/api/v1/users')
      .expect(401);
  });
});
```
