---
description: Start a new feature with proper planning
argument-hint: [--tdd] [feature description]
---

# Plan Command

Plan a new feature or task with proper structure before implementation.

## Flags

- `--tdd` - Enable Test-Driven Development mode (write tests first)

## Validation

If no feature description provided, ask for one.

## Planning Steps

### 1. Gather Context (REQUIRED)

**You MUST read relevant files before creating a plan.** Don't plan based on assumptions.

Before planning:
- Read relevant CLAUDE.md files
- **Read the actual files** that will be modified
- Identify existing patterns and conventions
- Understand related code and dependencies

Use `Explore` agent or direct file reads to understand:
- Current implementation
- Existing patterns in similar code
- Test file locations and patterns

### 2. Requirements Clarification

Ask clarifying questions if needed:
- What is the expected behavior?
- What are the edge cases?
- What are the acceptance criteria?
- Are there performance requirements?

### 3. Create Plan

Structure the implementation with **specific details**:

**Detail Level Guidelines:**

| Change Type | Detail Level |
|-------------|--------------|
| Complex/risky changes | Line numbers + code snippets |
| Medium changes | Function/method names |
| Simple/obvious changes | File paths only |
| New files | File path + structure outline |

**Output Format:**
```
## Feature: [description]

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Technical Approach
1. Step 1 - [description]
   - Why: [reasoning for this approach]
2. Step 2 - [description]

### Files to Modify

#### `path/to/file.ts` (lines 45-67)
**Current:** [brief description of current state]
**Change:** [what will change]
```typescript
// Example of the change (for complex modifications)
function existingFunction() {
  // Add: new caching logic here
}
```

#### `path/to/new-file.ts` (NEW)
**Purpose:** [why this file is needed]
**Structure:**
- `functionA()` - [purpose]
- `functionB()` - [purpose]

### Dependencies
- [list any new dependencies]

### Testing Strategy
- Unit tests: [specific test cases]
- Integration tests: [approach]
- Test file: `path/to/tests/file.test.ts`

### Alternatives Considered
- [Alternative 1] - [why not chosen]

### Risks
- [potential issue] - [mitigation]

### Complexity
- [low/medium/high] - [justification]
```

### 4. TDD Mode (if --tdd flag)

When `--tdd` is specified, modify the plan to include:

```
### TDD Implementation Order

1. **Acceptance Criteria → Test Cases**
   - [ ] Test: [criteria 1 as test]
   - [ ] Test: [criteria 2 as test]

2. **Write Failing Tests First**
   Files to create/modify:
   - `__tests__/feature.test.ts` - [test descriptions]

3. **Implement to Pass Tests**
   - Implement minimum code to pass each test
   - Run tests after each change

4. **Refactor**
   - Clean up while keeping tests green
```

**TDD Workflow:**
```
Write test → Run (FAIL) → Implement → Run (PASS) → Refactor → Run (PASS)
```

### 5. Confidence Check

Run Pre-Implementation Confidence Check before proceeding.

### 6. Await Approval

Present plan and wait for user approval before implementation.

**Key review points for user:**
- Are the file changes correct?
- Is the approach sound?
- Any concerns about the changes?

## Example (Standard)

```
## Feature: Add rate limiting to API

### Requirements
- [ ] Limit requests to 100/minute per user
- [ ] Return 429 when exceeded
- [ ] Log rate limit hits

### Technical Approach
1. Add rate limiting middleware using existing Express pattern
   - Why: Consistent with authMiddleware.ts approach
2. Store counters in Redis (already used for sessions)

### Files to Modify

#### `src/middleware/rateLimitMiddleware.ts` (NEW)
**Purpose:** Rate limiting middleware
**Structure:**
- `rateLimiter()` - Express middleware
- `getRateKey()` - Generate Redis key

#### `src/app.ts` (line 23)
**Current:** Auth middleware only
**Change:** Add rate limiter after auth
```typescript
app.use(authMiddleware);
app.use(rateLimiter({ limit: 100, window: 60 })); // ADD
```

### Testing Strategy
- Unit tests: Mock Redis, test limit logic
- Integration tests: Hit endpoint 101 times
- Test file: `__tests__/middleware/rateLimitMiddleware.test.ts`

### Alternatives Considered
- express-rate-limit package - Adds dependency, we can do simpler

### Risks
- Redis connection issues - Fail open (allow requests)

### Complexity
- Medium - New middleware but follows existing patterns
```

## Example (TDD Mode)

```
/plan --tdd Add rate limiting to API
```

```
## Feature: Add rate limiting to API (TDD)

### TDD Implementation Order

1. **Acceptance Criteria → Test Cases**
   - [ ] Test: Returns 200 for requests under limit
   - [ ] Test: Returns 429 when limit exceeded
   - [ ] Test: Resets after window expires
   - [ ] Test: Different users have separate limits

2. **Write Failing Tests First**
   File: `__tests__/middleware/rateLimitMiddleware.test.ts`
   ```typescript
   describe('rateLimiter', () => {
     it('allows requests under limit', async () => { ... });
     it('returns 429 when limit exceeded', async () => { ... });
     it('resets after window expires', async () => { ... });
   });
   ```

3. **Implement to Pass Tests**
   - Create `rateLimitMiddleware.ts`
   - Implement `rateLimiter()` function
   - Run tests after each addition

4. **Refactor**
   - Extract Redis key generation
   - Add JSDoc comments
```

## Next Steps

After approval:
- If `--tdd`: Write tests first, then implement
- Otherwise: Start implementation
- Use `/review` for code review
- Use `/validate` to verify before completion
- Use `/ship` when ready to commit
