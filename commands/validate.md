---
description: Validate implementation before shipping
allowed-tools: Bash(npm:*), Bash(pytest:*), Bash(tsc:*), Bash(git:*), Read
---

# Validate Command

Run all validations before shipping code.

## Validation Steps

### 1. Type Checking

**TypeScript projects:**
!`npx tsc --noEmit 2>&1 || true`

**Python projects:**
Check for mypy or pyright configuration.

### 2. Linting

**JavaScript/TypeScript:**
!`npm run lint 2>&1 || true`

**Python:**
!`ruff check . 2>&1 || true`

### 3. Tests

**Run test suite:**
!`npm test 2>&1 || true`

Or for Python:
!`pytest -q 2>&1 || true`

### 4. Build Check

**Verify build succeeds:**
!`npm run build 2>&1 || true`

### 5. SelfCheck Protocol

Answer these questions with evidence:

**Q1: Are tests passing?**
- Show actual test output
- Report pass/fail counts

**Q2: Are all requirements met?**
- Map requirements to implementation
- Confirm nothing missed

**Q3: No unverified assumptions?**
- External APIs verified
- Libraries documented

**Q4: Is there evidence?**
- Include validation output
- Show build success

## Report Format

```
## Validation Report

### Type Checking
[✅ Passed / ❌ Failed]
[Details if failed]

### Linting
[✅ Passed / ❌ Failed]
[Details if failed]

### Tests
[✅ X passed, Y failed / ❌ Failed to run]
[Failure details if any]

### Build
[✅ Passed / ❌ Failed]
[Details if failed]

### Summary
[READY TO SHIP / NEEDS FIXES]
```

## Next Steps

- If all pass: `/ship` to commit
- If issues found: Fix and re-run `/validate`
