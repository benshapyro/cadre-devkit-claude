---
description: Validate implementation before shipping
allowed-tools: Bash, Read, Glob
---

# Validate Command

**Purpose:** Quantitative validation - runs automated checks (types, lint, tests, build).

**Distinct from /review:** This command runs automated tooling. Use `/review` first for qualitative code review (style, security, best practices).

**Workflow:** `/review` → `/validate` → `/ship`

Run all validations before shipping code. Automatically detects the project's tech stack and runs only relevant checks.

## 1. Detect Tech Stack

First, check which config files exist to determine the project type:

- `package.json` → Node.js/TypeScript project
- `tsconfig.json` → TypeScript
- `pyproject.toml` or `requirements.txt` → Python
- `Cargo.toml` → Rust
- `go.mod` → Go

Use Glob to check for these files before running language-specific checks.

## 2. Run Relevant Checks

### TypeScript/Node.js (if package.json exists)

**Type checking:**
!`npx tsc --noEmit 2>&1 || true`

**Linting (if lint script exists):**
!`npm run lint 2>&1 || true`

**Tests:**
!`npm test 2>&1 || true`

**Build:**
!`npm run build 2>&1 || true`

### Python (only if pyproject.toml or requirements.txt exists)

**Linting:**
!`ruff check . 2>&1 || true`

**Type checking:**
!`mypy . 2>&1 || true`

**Tests:**
!`pytest -q 2>&1 || true`

### Rust (only if Cargo.toml exists)

**Check:**
!`cargo check 2>&1 || true`

**Clippy:**
!`cargo clippy -- -D warnings 2>&1 || true`

**Tests:**
!`cargo test 2>&1 || true`

### Go (only if go.mod exists)

**Build:**
!`go build ./... 2>&1 || true`

**Vet:**
!`go vet ./... 2>&1 || true`

**Tests:**
!`go test ./... 2>&1 || true`

## 3. SelfCheck Protocol

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

### Tech Stack Detected
[List detected languages/frameworks]

### Type Checking
[✅ Passed / ❌ Failed / ⏭️ Skipped (not applicable)]
[Details if failed]

### Linting
[✅ Passed / ❌ Failed / ⏭️ Skipped (not applicable)]
[Details if failed]

### Tests
[✅ X passed, Y failed / ❌ Failed to run / ⏭️ Skipped]
[Failure details if any]

### Build
[✅ Passed / ❌ Failed / ⏭️ Skipped (not applicable)]
[Details if failed]

### Summary
[READY TO SHIP / NEEDS FIXES]
```

## Next Steps

- If all pass: `/ship` to commit
- If issues found: Fix and re-run `/validate`
