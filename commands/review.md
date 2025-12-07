---
description: Review code changes for quality and best practices
allowed-tools: Read, Grep, Glob, Bash(git:*), Task
---

# Review Command

**Purpose:** Qualitative code review - checks code quality, style, security, and best practices.

**Distinct from /validate:** This command does human-like code review. Use `/validate` for automated checks (types, lint, tests, build).

**Workflow:** `/review` → `/validate` → `/ship`

## Process

### 1. Gather Changes

Get the current diff to review:

!`git diff --name-only`
!`git diff --staged --name-only`

If there are changes, get the full diff:

!`git diff`
!`git diff --staged`

If no changes found, inform the user and stop.

### 2. Perform Review

Use the code-reviewer agent for comprehensive review. The agent has `skills: code-formatter, error-handler` which auto-load.

```
Task(
  subagent_type="code-reviewer",
  prompt="Review the following code changes for quality, security, and best practices.

Files changed:
[list files from step 1]

Review focus:
- Code quality and maintainability (DRY, KISS, YAGNI)
- Security vulnerabilities (comprehensive OWASP checklist)
- Style consistency (via code-formatter skill)
- Error handling patterns (via error-handler skill)
- Test coverage for new/changed code

Provide a structured review with:
- Overall assessment (APPROVE / REQUEST CHANGES)
- Positive findings
- Required changes (with file:line references)
- Suggestions for improvement
- Security concerns (if any)"
)
```

### 3. Present Results

Present the agent's review to the user with clear next steps.

## Next Steps

After review is complete:

- **If APPROVED**: Run `/validate` to verify automated checks, then `/ship` to commit
- **If NEEDS CHANGES**: Fix the identified issues and re-run `/review`

## Example Flow

```
User: /review

Claude:
1. Gathers git diff (3 files changed)
2. Spawns code-reviewer agent with diff context
3. Agent reviews using its skills and security checklist
4. Presents structured review:

## Code Review Summary

**Overall Assessment**: APPROVE

### Positive Findings
- Clean separation of concerns in new utility functions
- Good error handling with descriptive messages

### Suggestions
- `src/utils/parser.ts:45` - Consider extracting the regex to a named constant

### Security Concerns
- None identified

---
Ready for `/validate` → `/ship`
```
