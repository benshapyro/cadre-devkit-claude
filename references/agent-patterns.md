# Sub-Agent Patterns

## Core Principle

Don't do research and implementation in the same context. Keep implementation context clean.

## When to Use Sub-Agents

| Situation | Action |
|-----------|--------|
| Need to understand how something works | Spawn `Explore` agent |
| Need current documentation | Spawn `documentation-researcher` |
| Complex implementation with unknowns | Research first, then implement |
| Simple/clear task | Just do it inline |
| Multiple unknowns | Spawn parallel research agents |

## Pattern 1: Research First

1. User asks to implement feature X
2. Spawn sub-agent(s) to research
3. Receive clean summary back
4. Implement with distilled knowledge

**Why:** Sub-agents handle messy exploration. Main context stays focused.

## Pattern 2: Parallel Research

For complex topics, spawn multiple agents simultaneously:

```
/research "topic"
    ↓
Parallel agents gather info:
- Explore: existing patterns in codebase
- doc-researcher: framework docs
- doc-researcher: community practices
    ↓
Synthesize findings
```

## Knowledge Preservation

After deep research, save reusable summaries:

1. Use `/progress` to create knowledge documents
2. Store in `docs/` with naming: `YYYY-MM-DD-NNN-description.md`
3. Reference in future sessions instead of re-exploring

Example output:
```markdown
# Authentication - Quick Reference
- Entry point: `src/auth/AuthController.ts:34`
- Session: `SessionManager.ts` (Redis-backed)
- Gotcha: Always call `validateToken()` before `getUser()`
```

## Available Agents

| Agent | Purpose |
|-------|---------|
| `Explore` | Codebase search and understanding |
| `documentation-researcher` | Official docs lookup |
| `code-reviewer` | Code quality review |
| `debugger` | Error analysis |
| `git-helper` | Git operations |
| `spec-discovery` | Requirements clarification |
| `performance-optimizer` | Performance analysis |
| `refactoring-assistant` | Safe code restructuring |
