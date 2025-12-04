---
description: Remove AI-generated code slop from current branch
---

# Slop Command

Check the diff against main and remove all AI-generated slop introduced in this branch.

## What is "Slop"?

AI-generated code often has tells that make it look unnatural:

### 1. Over-Commenting
```typescript
// BAD: AI slop
// Get the user from the database
const user = await db.getUser(id); // Fetch user by ID

// GOOD: Self-documenting, no comment needed
const user = await db.getUser(id);
```

### 2. Defensive Overkill
```typescript
// BAD: Unnecessary defensive checks
function processUser(user: User) {
  if (!user) {
    throw new Error('User is required');
  }
  if (!user.id) {
    throw new Error('User must have an id');
  }
  // ... when caller already validates
}

// GOOD: Trust internal callers
function processUser(user: User) {
  // Just do the work - caller handles validation
}
```

### 3. Type Escapes
```typescript
// BAD: Casting to escape type issues
const data = response as any;
const items = (result as unknown as Item[]);

// GOOD: Fix the actual type
const data: ResponseType = response;
```

### 4. Inconsistent Style
- Different naming conventions than the file uses
- Different error handling patterns
- Different import styles
- Added JSDoc when file doesn't use it (or vice versa)

### 5. Unnecessary Try/Catch
```typescript
// BAD: Wrapping things that don't throw
try {
  const x = a + b;
  return x;
} catch (error) {
  console.error('Failed to add numbers', error);
  throw error;
}

// GOOD: Just do it
return a + b;
```

### 6. Verbose Logging
```typescript
// BAD: Logging everything
console.log('Starting process...');
console.log('User ID:', userId);
console.log('Processing...');
console.log('Done!');

// GOOD: Log meaningful events only (or nothing for simple ops)
```

## Workflow

### 1. Get the Diff

```bash
git diff main...HEAD
```

Identify all files changed in this branch.

### 2. For Each Changed File

1. Read the FULL file (not just the diff) to understand existing patterns
2. Compare new code against existing style:
   - Comment density
   - Error handling approach
   - Naming conventions
   - Type annotation style
   - Import organization

### 3. Identify Slop

Look for code that:
- Has MORE comments than surrounding code
- Has MORE defensive checks than similar code paths
- Uses `any` or type assertions
- Has different formatting/style than the file
- Adds try/catch around non-throwing code
- Adds logging that doesn't match file patterns

### 4. Fix It

Remove or adjust:
- Delete unnecessary comments
- Remove redundant validation (if callers are trusted)
- Fix types properly instead of casting
- Match existing code style
- Remove pointless try/catch
- Remove excessive logging

**Use Edit tool to make changes.**

### 5. Report

End with a **1-3 sentence summary only**:

```
Removed 4 unnecessary comments, 2 redundant null checks, and fixed
1 `any` cast in UserService.ts. Deleted try/catch wrapper in
processPayment() since the caller handles errors.
```

## What NOT to Remove

- Comments that explain non-obvious business logic
- Validation at system boundaries (user input, external APIs)
- Error handling that matches the file's existing patterns
- Logging that matches existing patterns
- Type assertions that are genuinely necessary

## Example

**Before (AI slop):**
```typescript
/**
 * Fetches user data from the database
 * @param userId - The ID of the user to fetch
 * @returns The user object or null if not found
 */
async function getUser(userId: string): Promise<User | null> {
  // Validate the user ID
  if (!userId) {
    throw new Error('userId is required');
  }

  try {
    // Fetch the user from database
    const user = await db.users.findOne({ id: userId });

    // Return the user
    return user as any as User;
  } catch (error) {
    // Log the error
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

**After (cleaned):**
```typescript
async function getUser(userId: string): Promise<User | null> {
  return db.users.findOne({ id: userId });
}
```

**Report:** "Removed JSDoc (file doesn't use it), deleted redundant userId validation (TypeScript enforces it), removed try/catch (caller handles errors), fixed `any` cast by using proper return type."

## Notes

- Run AFTER implementation, before /review
- Focuses on style consistency, not functionality
- Be conservative - when unsure, leave it
- Check git diff after to verify changes make sense
