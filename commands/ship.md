---
description: Commit and ship validated changes
allowed-tools: Bash(git:*)
argument-hint: [optional commit message]
---

# Ship Command

Commit validated changes with proper formatting.

## Pre-Ship Checks

**Verify validation passed:**
- Has `/validate` been run?
- Were there any failures?

**Check git status:**
!`git status`

## Gather Information

**Staged changes:**
!`git diff --staged --stat`

**Recent commits for style:**
!`git log --oneline -5`

**Current branch:**
!`git branch --show-current`

## Generate Commit

### Analyze Changes

Based on the diff, determine:
- **Type**: feat, fix, docs, style, refactor, test, chore
- **Scope**: Component or module affected
- **Subject**: What the commit does (imperative mood)

### Commit Format

```
type(scope): subject

Body explaining why this change was made.
- Detail 1
- Detail 2

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### If Argument Provided

Use $1 as the commit message subject.

## Execute Commit

**Stage all changes (if not already staged):**
Ask user before staging untracked files.

**Create commit:**
```bash
git commit -m "$(cat <<'EOF'
[generated message]
EOF
)"
```

**Verify success:**
!`git log -1 --oneline`

## Report

```
## Ship Complete

✅ Commit created successfully

**Commit:** [hash]
**Message:** [subject]
**Files changed:** [count]

### Next Steps
- Push to remote: `git push`
- Create PR: `gh pr create`
- Continue developing
```

## Safety Rules

- Never force push
- Never push to main/master without approval
- Always verify commit authorship before amend
- Report any pre-commit hook failures
