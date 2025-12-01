---
name: helpers
description: Common procedures referenced across workflows
---

# Helper Procedures

## Load-Project-Context

Load project documentation to understand requirements and architecture.

1. Check for project CLAUDE.md files (recursively in subdirectories)
2. Check for docs/ directory with PRD, architecture, or design docs
3. Check for README.md with project overview
4. Build context map with:
   - Project purpose and scope
   - Architecture decisions
   - Current implementation state
   - Key dependencies

## Initialize-Development-Session

Prepare for a development session with full project context.

1. Execute: helpers.md#Load-Project-Context
2. Read PLANNING.md (if exists)
   - Load non-negotiable rules
   - Understand technology stack
   - Review quality standards
3. Read KNOWLEDGE.md (if exists)
   - Apply lessons learned
   - Note troubleshooting patterns
4. Read TASK.md or TODO.md (if exists)
   - Identify current priorities
   - Review known issues
5. Report session ready with summary

## Validate-TypeScript-Project

Ensure TypeScript project has no type errors before proceeding.

1. Check for tsconfig.json in project root
2. Run: `npx tsc --noEmit`
3. If errors:
   - Report errors with file:line references
   - Group by file for easier resolution
   - Halt implementation until resolved
4. If no errors:
   - Report "TypeScript validation passed"
   - Proceed with next steps

## Validate-Python-Project

Ensure Python project passes type checks and linting.

1. Check for pyproject.toml or setup.py
2. Run type checking: `mypy .` or `pyright .` (if configured)
3. Run linting: `ruff check .` or `flake8 .` (if configured)
4. If errors:
   - Report errors grouped by severity
   - Halt implementation until resolved
5. If clean:
   - Report "Python validation passed"
   - Proceed with next steps

## Run-Test-Suite

Execute tests appropriate to the project type.

1. Identify test framework:
   - JavaScript/TypeScript: Check for jest.config.* or vitest.config.*
   - Python: Check for pytest.ini, pyproject.toml [tool.pytest], or conftest.py
2. Run tests:
   - JS/TS: `npm test` or `npm run test`
   - Python: `pytest -q`
3. Report results:
   - Pass count, fail count, skip count
   - Details of any failures

## Git-Commit-Workflow

Create a well-formatted commit following project conventions.

1. Run `git status` to verify staged changes
2. Run `git diff --staged` to review what will be committed
3. Draft commit message following format:
   - `type(scope): short summary`
   - Types: feat, fix, docs, style, refactor, test, chore
4. Ensure message ends with:
   ```

   [Claude Code attribution footer]
   ```
5. Execute commit with proper formatting
6. Run `git status` to verify success

## Code-Review-Checklist

Review code for quality before completion.

1. **Correctness**: Does code solve the stated problem?
2. **Clarity**: Is code self-documenting and readable?
3. **Completeness**: Are edge cases handled?
4. **Consistency**: Does it follow project style?
5. **Security**: Any potential vulnerabilities? (input validation, injection risks)
6. **Performance**: Any obvious inefficiencies?
7. **Testing**: Is there adequate test coverage?

## Error-Investigation

Systematically debug errors and exceptions.

1. Read the full error message and stack trace
2. Identify the error location (file:line)
3. Read the relevant code section with context
4. Determine error category:
   - Syntax error
   - Type error
   - Runtime exception
   - Logic error
5. Form hypothesis about cause
6. Verify hypothesis before implementing fix
7. Implement minimal fix
8. Verify fix resolves error without side effects

## Refactor-Safely

Refactor code while maintaining behavior.

1. Identify test coverage for code being refactored
2. If insufficient coverage, add tests first
3. Run tests to establish baseline (all should pass)
4. Make incremental changes
5. Run tests after each change
6. If tests fail, revert and reconsider approach
7. Document refactoring rationale in commit

## Search-Codebase

Find relevant code efficiently.

1. Start with file patterns: `**/*.{ts,tsx}` or `**/*.py`
2. Use grep for specific identifiers or patterns
3. Check imports/exports for dependency chains
4. Read key files to understand structure
5. Build mental model before making changes

## Create-Feature-Branch

Set up a new feature branch following conventions.

1. Ensure on main branch: `git checkout main`
2. Pull latest: `git pull --rebase`
3. Create branch: `git checkout -b {type}/{description}`
   - feat/ for new features
   - fix/ for bug fixes
   - refactor/ for refactoring
   - docs/ for documentation
4. Verify branch created: `git branch --show-current`
