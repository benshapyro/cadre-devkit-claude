# DevKit Components Explained

This guide explains each piece of the DevKit - what it does and when it helps.

## Overview

The DevKit has four types of components:

| Type | What It Is | Analogy |
|------|-----------|---------|
| **Commands** | Actions you explicitly run | Tools in a toolbox |
| **Skills** | Knowledge Claude can access | Reference books |
| **Agents** | Specialized assistants | Expert consultants |
| **Hooks** | Background automation | Automatic safety systems |

---

## Commands (4)

Commands are actions you run with `/command-name`. Think of them as your main workflow tools.

### /plan

**What it does:** Helps you think through a feature before writing code.

**When to use:** Starting any new feature or significant change.

**What happens:**
1. Claude asks clarifying questions about requirements
2. Identifies edge cases you might not have considered
3. Creates a structured implementation plan
4. Lists files that will need changes

**Example:**
```
/plan add email notifications for password reset
```

**Why it matters:** Spending 10 minutes planning saves hours of rework. This command forces that discipline.

---

### /review

**What it does:** Reviews your code changes against Cadre standards.

**When to use:** After making changes, before committing.

**What happens:**
1. Claude looks at your staged/unstaged changes
2. Checks for:
   - Code quality (readability, duplication, complexity)
   - Naming conventions
   - Security issues (hardcoded secrets, injection risks)
   - Missing error handling
   - Test coverage
3. Provides specific feedback with file:line references

**Example:**
```
/review
```

**Why it matters:** Catches issues before they become problems. Like having a senior dev look over your shoulder.

---

### /validate

**What it does:** Runs all automated checks (types, lint, tests, build).

**When to use:** Before committing, to make sure nothing is broken.

**What happens:**
1. Runs TypeScript type checking (`tsc --noEmit`)
2. Runs linter (`npm run lint` or `ruff check`)
3. Runs test suite (`npm test` or `pytest`)
4. Runs build (`npm run build`)
5. Reports pass/fail for each step

**Example:**
```
/validate
```

**Why it matters:** One command instead of remembering to run four different checks.

---

### /ship

**What it does:** Creates a properly formatted commit.

**When to use:** When you're ready to commit your changes.

**What happens:**
1. Shows you what will be committed
2. Generates a commit message following our conventions
3. Stages files (asks before adding untracked files)
4. Creates the commit

**Example:**
```
/ship
```

Or with a custom message:
```
/ship fix login timeout issue
```

**Why it matters:** Consistent commit messages make git history useful.

---

## Skills (5)

Skills are specialized knowledge that Claude can tap into. They activate automatically when relevant, or you can load them manually.

### api-design-patterns

**What it knows:** REST API best practices, endpoint design, status codes, request/response formats, authentication patterns.

**When it helps:**
- Designing new API endpoints
- Reviewing API code
- Questions about REST conventions

**Example triggers:** "create an endpoint", "design the API", "what status code should I use"

---

### code-formatter

**What it knows:** Cadre's coding style - naming conventions, line length, import style, TypeScript/Python standards.

**When it helps:**
- Formatting code
- Fixing linting issues
- Questions about style conventions

**Example triggers:** "format this code", "fix the linting errors", "what's our naming convention"

---

### documentation-templates

**What it knows:** How to write READMEs, API documentation, code comments.

**When it helps:**
- Creating project documentation
- Writing API docs
- Adding meaningful comments

**Example triggers:** "write a README", "document this function", "add API docs"

---

### error-handler

**What it knows:** Error handling patterns for TypeScript and Python - custom error classes, try/catch strategies, error responses.

**When it helps:**
- Adding error handling to code
- Designing error responses
- Debugging exception issues

**Example triggers:** "handle this error", "add try/catch", "create error classes"

---

### test-generator

**What it knows:** How to write tests with Jest (TypeScript) and Pytest (Python) - test structure, mocking, fixtures, assertions.

**When it helps:**
- Writing new tests
- Improving test coverage
- Questions about testing patterns

**Example triggers:** "write tests for this", "add test coverage", "create a mock"

---

## Agents (7)

Agents are like specialized consultants. They have specific expertise and a defined approach to problems.

### code-reviewer

**Expertise:** Code quality, security, style compliance.

**When it activates:** When you ask for a code review or use `/review`.

**What it does:** Systematic review against our standards with specific, actionable feedback.

---

### debugger

**Expertise:** Error analysis, stack traces, root cause identification.

**When it activates:** When you're dealing with bugs, errors, or unexpected behavior.

**What it does:** Methodically analyzes the problem, forms hypotheses, and identifies the root cause (not just symptoms).

---

### spec-discovery

**Expertise:** Requirements clarification, edge case identification.

**When it activates:** When requirements are vague or you're starting something new.

**What it does:** Asks probing questions to uncover hidden assumptions and missing requirements.

---

### git-helper

**Expertise:** Git workflows, branching, commit conventions.

**When it activates:** When you're doing git operations.

**What it does:** Helps with branch naming, commit messages, rebasing - following our conventions.

---

### documentation-researcher

**Expertise:** Finding current, official documentation.

**When it activates:** When you need to look up how a library or API works.

**What it does:** Searches official docs (not outdated training data) and provides current information with sources.

---

### refactoring-assistant

**Expertise:** Safe code restructuring.

**When it activates:** When you want to refactor, extract, or reorganize code.

**What it does:** Helps restructure code while preserving behavior, with test verification at each step.

---

### performance-optimizer

**Expertise:** Performance analysis and optimization.

**When it activates:** When dealing with slow code or performance issues.

**What it does:** Profiles, identifies bottlenecks, and suggests targeted optimizations.

---

## Hooks (3)

Hooks run automatically in the background. You don't invoke them - they just work.

### Skill Activation Hook

**What it does:** Watches your prompts and suggests relevant skills/agents.

**How it works:** When you type something like "write tests", it notices the keyword and suggests the test-generator skill.

**You see:** A note like "Relevant skills detected: test-generator"

---

### Dangerous Command Blocker

**What it does:** Prevents destructive shell commands from running.

**What it blocks:**
- `rm -rf /` (delete everything)
- `chmod 777` (insecure permissions)
- `git push --force` to main
- `sudo` commands
- Disk formatting commands

**You see:** "BLOCKED: Dangerous command pattern detected"

---

### Sensitive File Guard

**What it does:** Prevents access to files containing secrets.

**What it protects:**
- `.env` files
- Credential files (`.key`, `.pem`, `credentials.json`)
- SSH keys (`id_rsa`, `id_ed25519`)
- AWS credentials

**You see:** "BLOCKED: Sensitive file access detected"

---

## How They Work Together

Here's a typical flow showing multiple components:

1. **You:** "I need to add a password reset feature"
2. **Skill Activation Hook:** Suggests spec-discovery agent
3. **spec-discovery agent:** Asks clarifying questions
4. **You:** `/plan add password reset`
5. **/plan command:** Creates structured implementation plan
6. **You:** [Implement with Claude's help]
7. **api-design-patterns skill:** Guides API endpoint design
8. **error-handler skill:** Helps with error handling
9. **You:** `/review`
10. **code-reviewer agent:** Reviews against standards
11. **You:** `/validate`
12. **test-generator skill:** (if tests needed)
13. **/validate command:** Runs all checks
14. **You:** `/ship`
15. **git-helper agent:** (if needed)
16. **/ship command:** Creates commit

The pieces work together seamlessly - you just focus on the work.
