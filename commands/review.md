---
description: Review code changes for quality and best practices
allowed-tools: Read, Grep, Glob, Bash(git:*)
---

# Review Command

**Purpose:** Qualitative code review - checks code quality, style, security, and best practices.

**Distinct from /validate:** This command does human-like code review. Use `/validate` for automated checks (types, lint, tests, build).

**Workflow:** `/review` → `/validate` → `/ship`

Review current code changes against project standards.

## Gather Changes

**Get staged and unstaged changes:**
!`git diff --name-only`
!`git diff --staged --name-only`

**Get full diff:**
!`git diff`
!`git diff --staged`

## Review Checklist

For each changed file, check:

### Code Quality
- [ ] **Readability**: Code is self-documenting and clear
- [ ] **DRY**: No unnecessary duplication
- [ ] **KISS**: Solutions are simple and straightforward
- [ ] **YAGNI**: Only implements what's needed

### Naming Conventions
- [ ] Files: `lowercase_with_underscores`
- [ ] Variables: `camelCase`
- [ ] Components/Classes: `PascalCase`

### Style
- [ ] Max line length: 100 characters
- [ ] Trailing commas for multi-line objects/arrays
- [ ] ES Modules (no `require`)
- [ ] `async/await` for promises

### Security
- [ ] No hardcoded credentials or secrets
- [ ] Input validation present
- [ ] No SQL injection risks
- [ ] No XSS vulnerabilities

### Error Handling
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are informative
- [ ] Edge cases are considered

### Testing
- [ ] Tests exist for new functionality
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases are tested

## Report Format

```
## Code Review Summary

### Files Reviewed
- `path/file1.ts` - [status]
- `path/file2.ts` - [status]

### Issues Found

#### Critical
- [none or list]

#### Suggestions
- [improvements]

### What's Good
- [positive aspects]

### Verdict
[APPROVED / NEEDS CHANGES]
```

## Next Steps

- If approved: `/validate` then `/ship`
- If changes needed: Fix issues and re-run `/review`
