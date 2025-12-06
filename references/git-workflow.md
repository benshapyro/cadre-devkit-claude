# Git Workflow Guide

## Branching Strategy

- All feature work branches from `main` (or `master` if that's the project default)
- Use squash merges to keep history clean
- Rebase frequently: `git pull --rebase`

## Branch Naming

Format: `{type}/{short-description}`

| Type | Use For |
|------|---------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `refactor/` | Code restructuring |
| `docs/` | Documentation |
| `test/` | Test additions |
| `chore/` | Maintenance tasks |

Examples:
- `feat/user-authentication`
- `fix/null-payload-handling`
- `refactor/api-middleware`

## Commit Format

Format: `type(scope): short summary`

- **type**: feat, fix, refactor, docs, test, chore
- **scope**: affected area (api, auth, ui, etc.)
- **summary**: imperative mood, lowercase, no period

Examples:
- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null payloads in POST requests`
- `refactor(middleware): extract validation logic`

## Common Commands

```bash
# Sync with remote
git pull --rebase

# Create feature branch
git checkout -b feat/my-feature

# Interactive staging
git add -p

# Commit with message
git commit -m "type(scope): message"

# Push new branch
git push -u origin HEAD

# Squash last N commits
git rebase -i HEAD~N
```

## Merge Strategy

1. Ensure branch is up to date: `git pull --rebase origin main`
2. Run tests before merging
3. Use squash merge for feature branches
4. Delete branch after merge
