---
name: code-formatter
description: Formats code according to Ben's style guidelines for TypeScript, Python, and general best practices. Use when formatting code, fixing linting issues, checking naming conventions, organizing imports, or when user mentions formatting, style, linting, Prettier, Black, or ESLint.
allowed-tools: Read, Grep, Glob
---

# Code Formatter Skill

Apply consistent code formatting and style according to established guidelines.

## Formatting Standards

### File Naming
- **All files**: `lowercase_with_underscores`
- Examples: `user_service.py`, `api_client.ts`, `data_helper.js`

### Variable Naming
- **Variables/Functions**: `camelCase`
- **Classes/Components**: `PascalCase`
- **Constants**: `UPPER_CASE_SNAKE_CASE`

```typescript
// Good
const userName = 'John';
const API_KEY = 'secret';

class UserService {}
function getUserData() {}

// Bad
const UserName = 'John';
const api_key = 'secret';

class userService {}
function get_user_data() {}
```

### Code Style

#### Line Length
- Maximum 100 characters per line
- Break long lines logically at operators or delimiters

#### Commas
- Use trailing commas for multi-line objects and arrays

```typescript
// Good
const config = {
  host: 'localhost',
  port: 3000,
  timeout: 5000,  // trailing comma
};

const items = [
  'first',
  'second',
  'third',  // trailing comma
];

// Bad
const config = {
  host: 'localhost',
  port: 3000,
  timeout: 5000  // missing trailing comma
};
```

#### Imports
- Use explicit imports (no wildcard `*`)
- ES Modules only (no `require`)
- Group imports: external libraries first, then internal modules

```typescript
// Good
import { useState, useEffect } from 'react';
import { fetchUser } from '../api/users';

// Bad
import * from 'react';
const users = require('../api/users');
```

#### Async/Await
- Prefer `async/await` over `.then()` chains

```typescript
// Good
async function fetchData() {
  const response = await apiClient.get('/data');
  return response.data;
}

// Bad
function fetchData() {
  return apiClient.get('/data').then(res => res.data);
}
```

### TypeScript Standards
- Enable strict mode
- Avoid `any` type (use `unknown` if type is truly unknown)
- Define interfaces for object shapes
- Use type annotations for function parameters and returns

```typescript
// Good
interface User {
  id: number;
  name: string;
  email: string;
}

async function getUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Bad
async function getUser(id) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

### Python Standards (PEP 8)
- 4 spaces for indentation (no tabs)
- Snake_case for functions and variables
- PascalCase for classes
- Use type hints where beneficial

```python
# Good
def calculate_total(items: list[dict]) -> float:
    """Calculate total price of items."""
    return sum(item['price'] for item in items)

class UserService:
    """Service for user operations."""
    pass

# Bad
def CalculateTotal(items):
    return sum(item['price'] for item in items)

class user_service:
    pass
```

### Comments
- Write comments only for non-obvious logic
- Explain "why" not "what"
- Keep comments updated with code changes

```typescript
// Good
// Use exponential backoff to avoid overwhelming the API during outages
const retryDelay = Math.pow(2, attemptNumber) * 1000;

// Bad
// Set retry delay
const retryDelay = Math.pow(2, attemptNumber) * 1000;
```

## Formatting Tools

### JavaScript/TypeScript
- **Prettier**: For consistent formatting
- **ESLint**: For code quality and style enforcement

```bash
# Format with Prettier
npx prettier --write "src/**/*.{ts,tsx,js,jsx}"

# Lint with ESLint
npx eslint src/ --fix
```

### Python
- **Black**: For formatting
- **isort**: For import sorting

```bash
# Format code
black .

# Sort imports
isort .

# Both together
black . && isort .
```

## Common Formatting Issues

### Fix These Automatically
1. Inconsistent indentation
2. Missing trailing commas
3. Lines exceeding 100 characters
4. Inconsistent quote styles (prefer single quotes for TS, double for Python)
5. Extra whitespace
6. Import ordering

### Require Manual Review
1. Complex expressions that need breaking
2. Unclear variable names
3. Missing type annotations
4. Ambiguous logic requiring comments

## Formatting Process

When formatting code:
1. Check file naming convention
2. Verify variable/class naming follows standards
3. Ensure imports are explicit and properly ordered
4. Check line length (max 100 chars)
5. Add trailing commas to multi-line structures
6. Replace `.then()` with `async/await`
7. Add type annotations where missing (TypeScript/Python)
8. Remove unnecessary comments, add helpful ones
9. Verify consistent indentation

Always provide a summary of changes made and reasoning for significant modifications.

---

## Version
- v1.1.0 (2025-12-05): Added allowed-tools restriction, enriched trigger keywords
- v1.0.0 (2025-11-15): Initial version
