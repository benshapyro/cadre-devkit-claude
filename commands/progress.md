---
description: Save research findings as reusable knowledge documents
argument-hint: [optional: topic name]
---

# Progress Command

Compress learned knowledge into reusable documents for future sessions.

## Purpose

After deep exploration or research, save findings so future sessions don't need to re-learn the same things. Creates "cheat sheets" for your codebase.

## When to Use

- After `/research` sessions with valuable findings
- After exploring a complex part of the codebase
- When you've learned something that will be useful again
- When starting work in a new area of the codebase

## File Naming Convention

**Format:** `YYYY-MM-DD-NNN-description.md`

- `YYYY-MM-DD` - Today's date (use actual current date)
- `NNN` - Sequential number for the day (001, 002, etc.)
- `description` - Short kebab-case description of topic

**Examples:**
- `2025-12-03-001-authentication-system.md`
- `2025-12-03-002-payment-processing.md`
- `2025-12-04-001-api-rate-limiting.md`

**To determine next number:**
1. List existing files in `docs/` for today's date
2. Find highest NNN for today
3. Increment by 1 (or start at 001 if first of day)

## Workflow

### 1. Identify What Was Learned

Review the current conversation for:
- Files and entry points discovered
- Patterns and conventions identified
- Gotchas and edge cases found
- Key relationships between components
- External documentation links

### 2. Propose Knowledge Document

**Output Format:**
```
## Proposed Knowledge Document

**Topic:** [topic name]
**File:** `docs/YYYY-MM-DD-NNN-description.md`

### Preview

# [Topic] - Quick Reference

**Date:** YYYY-MM-DD
**Context:** [What prompted this research]

**Key Files:**
- `path/to/main/file.ts:line` - [description]
- `path/to/related/file.ts` - [description]

**Entry Points:**
- [Where to start for common tasks]

**Key Patterns:**
- [Pattern 1]
- [Pattern 2]

**Gotchas:**
- [Common mistake or edge case]

**Related Docs:**
- [Link to external docs]

---
Save this document? (yes / edit first / cancel)
```

### 3. Await Approval

Wait for user to:
- **Approve** - Create the file
- **Edit** - User provides changes, then save
- **Cancel** - Don't save

### 4. Save Document

If approved:
1. Create `docs/` directory if it doesn't exist
2. Determine correct sequence number for today
3. Write the knowledge document with correct filename
4. Confirm save location

## Knowledge Document Template

```markdown
# [Topic] - Quick Reference

**Date:** YYYY-MM-DD
**Context:** [Brief context of what prompted this research]

## Overview

[1-2 sentence summary of what this covers]

## Key Files

| File | Purpose |
|------|---------|
| `path/to/file.ts:line` | [What it does] |
| `path/to/other.ts` | [What it does] |

## Entry Points

**For [common task 1]:** Start at `file.ts:functionName()`
**For [common task 2]:** Start at `other.ts:methodName()`

## Patterns & Conventions

### [Pattern Name]
[Description with code example if helpful]

### [Convention Name]
[How things are done in this area]

## Gotchas & Edge Cases

- **[Gotcha 1]:** [What to watch out for]
- **[Edge case]:** [When this happens, do this]

## External Resources

- [Official Docs](url) - [What it covers]
- [Related Guide](url) - [What it covers]
```

## Example

**After researching authentication in a project:**

```
## Proposed Knowledge Document

**Topic:** Authentication System
**File:** `docs/2025-12-03-001-authentication-system.md`

### Preview

# Authentication System - Quick Reference

**Date:** 2025-12-03
**Context:** Researching how to add OAuth support to existing auth

**Key Files:**
- `src/auth/AuthController.ts:34` - Main entry point
- `src/auth/SessionManager.ts` - Redis-backed sessions
- `src/middleware/authMiddleware.ts:12` - Route protection

**Entry Points:**
- Login flow: `AuthController.login()`
- Token validation: `SessionManager.validateToken()`
- Protecting routes: Use `authMiddleware`

**Key Patterns:**
- All auth errors throw `AuthenticationError`
- Sessions expire after 24h, refresh tokens last 7d
- User context available via `req.user` after middleware

**Gotchas:**
- Always call `validateToken()` before `getUser()` - order matters
- Redis connection must be established before auth routes load
- Test users in `__fixtures__/users.ts`, not hardcoded

**Related Docs:**
- [Express Session Docs](https://expressjs.com/en/resources/middleware/session.html)

---
Save this document?
```

## Managing Knowledge

### List Existing Knowledge
```bash
ls docs/*.md | grep -E "^\d{4}-\d{2}-\d{2}"
```

### Reference in Sessions
At the start of relevant work, find and read relevant knowledge docs:
```
"I'm working on auth. Let me check for existing knowledge docs..."
ls docs/ | grep auth
```

### Finding Relevant Docs
- By date: `ls docs/2025-12-*`
- By topic: `ls docs/ | grep payment`
- Recent: `ls -lt docs/ | head`

## Directory Structure

```
project/
├── docs/
│   ├── 2025-12-01-001-authentication-system.md
│   ├── 2025-12-01-002-database-schema.md
│   ├── 2025-12-03-001-payment-processing.md
│   └── README.md (if exists, don't modify)
├── src/
└── ...
```

## Notes

- Knowledge docs should be concise (1-2 pages max)
- Focus on "what you wish you knew when you started"
- Include file:line references for quick navigation
- Always create NEW files (don't overwrite existing)
- These are for AI context, not human documentation
- The date-based naming makes it easy to find recent learnings
