---
name: documentation-templates
description: Generates README files, API documentation, and inline code comments following best practices. Use when creating project documentation, writing READMEs, documenting APIs, or explaining complex code.
allowed-tools: Read, Grep, Glob
---

# Documentation Templates Skill

Create clear, maintainable documentation for projects and code.

## Resources

For full templates, see:
- `references/readme-template.md` - Complete README template
- `references/api-docs-template.md` - API documentation template

## Core Principles

1. **Explain Why, Not What** - Code shows what; docs explain why
2. **Keep it Updated** - Outdated docs are worse than no docs
3. **Write for Humans** - Clear, concise, jargon-free
4. **Progressive Disclosure** - Start simple, provide details on demand
5. **Examples are King** - Show, don't just tell

## README Quick Structure

```markdown
# Project Name
Brief description (1-2 sentences)

## Features
## Prerequisites
## Installation
## Configuration
## Usage
## Development
## Deployment
## Contributing
## License
```

## Function Documentation

### TypeScript (JSDoc)
```typescript
/**
 * Fetches user data from the database.
 *
 * @param userId - The unique identifier of the user
 * @returns Promise resolving to the user object
 * @throws {NotFoundError} If user doesn't exist
 *
 * @example
 * const user = await fetchUserData('123');
 */
async function fetchUserData(userId: string): Promise<User> {
  // ...
}
```

### Python (Docstring)
```python
def fetch_user_data(user_id: str) -> User:
    """
    Fetch user data from the database.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        User object containing user data.

    Raises:
        NotFoundError: If user doesn't exist.

    Example:
        >>> user = fetch_user_data('123')
    """
```

## Inline Comments

```typescript
// BAD: Obvious
// Increment counter
counter++;

// GOOD: Explain why
// Increment before checking because first request counts
counter++;

// Cache disabled for premium users after stale data issue (INC-5678)
if (!user.isPremium) {
  cache.set(key, value);
}
```

## Architecture Decision Record (ADR)

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need ACID transactions, complex queries, strong consistency.

## Decision
Use PostgreSQL as the primary database.

## Consequences
**Positive:** ACID compliance, rich queries, strong ecosystem
**Negative:** Horizontal scaling requires more effort
```

## Best Practices

### Do
- Start with clear, one-sentence description
- Include practical examples
- Document "why" decisions were made
- Keep documentation close to code
- Update docs when code changes

### Don't
- Write obvious comments
- Let docs get out of sync
- Use jargon without explanation
- Skip examples
- Document implementation details that change often

## Documentation Checklist

- [ ] Clear project description
- [ ] Installation instructions work
- [ ] Environment variables documented
- [ ] API endpoints with examples
- [ ] Common errors and solutions
- [ ] Examples are runnable
- [ ] No sensitive information exposed

---

Good documentation saves hours of debugging. Write for the developer who joins in 6 months.

---

## Version
- v1.1.0 (2025-12-05): Added allowed-tools restriction, enriched trigger keywords
- v1.0.0 (2025-11-15): Initial version
