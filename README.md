# Cadre DevKit for Claude Code

**Turn Claude Code from a helpful intern into a reliable senior engineer.**

---

## What is Claude Code?

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is Anthropic's official CLI for AI-assisted coding. You run it in your terminal, and Claude can read your files, write code, run commands, and help you build software.

It's powerful. It's also... unpredictable.

## The Problem

AI coding assistants have a reliability problem:

| Issue | What Happens |
|-------|--------------|
| **Hallucination** | "Tests pass!" (they don't) |
| **Over-engineering** | 50 lines of defensive code for a 3-line function |
| **AI slop** | Comments everywhere, `any` casts, unnecessary try/catch |
| **Context loss** | Re-explores the same code every session |
| **Dangerous commands** | `rm -rf /` is just a typo away |
| **No planning** | Jumps straight to code without understanding |
| **Inconsistent quality** | Great on Monday, chaos on Tuesday |

You end up babysitting the AI instead of shipping code.

## The Solution

This devkit adds a **quality and safety layer** to Claude Code:

- **Hooks** that actually block dangerous commands (not just warnings)
- **Structured workflow** from idea to shipping
- **Evidence-based verification** (no more "it should work")
- **Research-first pattern** (understand before implementing)
- **Knowledge preservation** (learnings persist across sessions)
- **Anti-slop tooling** (removes AI code smell)
- **Interactive learning** (teach yourself about Claude Code)

It's not a collection of prompts. It's an integrated system.

---

## Installation

### Option 1: Claude Code Marketplace (Recommended)

```bash
claude plugins install cadre-devkit-claude
```

This installs the devkit directly into your Claude Code environment.

### Option 2: Git Clone

```bash
git clone https://github.com/benshapyro/cadre-devkit-claude.git
cd cadre-devkit-claude
./install.sh
```

### Option 3: Manual Installation

```bash
# Clone
git clone https://github.com/benshapyro/cadre-devkit-claude.git

# Copy components
cp -r cadre-devkit-claude/commands/* ~/.claude/commands/
cp -r cadre-devkit-claude/skills/* ~/.claude/skills/
cp -r cadre-devkit-claude/agents/* ~/.claude/agents/
cp -r cadre-devkit-claude/hooks/* ~/.claude/hooks/

# Make hooks executable
chmod +x ~/.claude/hooks/**/*.py
chmod +x ~/.claude/hooks/**/*.sh
```

### Configure Hooks

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/security/dangerous-command-blocker.py" }]
      },
      {
        "matcher": "Edit|Write|Read",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/security/sensitive-file-guard.py" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/formatting/auto-format.py" },
          { "type": "command", "command": "~/.claude/hooks/testing/test-on-change.py" }
        ]
      }
    ]
  }
}
```

### Verify Installation

```bash
claude
> /learn                    # Should show welcome message
> /plan test feature        # Should work
> Can you run rm -rf /      # Should be blocked by hook
```

---

## The Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  NEW PROJECT:                                                               │
│  /greenfield ──→ SPEC.md + DESIGN.md + PLAN.md                              │
│       │                                                                     │
│       └──→ /plan [first feature] ──→ ...                                    │
│                                                                             │
│  EXISTING PROJECT:                                                          │
│  /research ──→ /plan ──→ implement ──→ /slop ──→ /review ──→ /validate ──→ /ship
│      │          │                        │         │          │        │    │
│   Parallel    Read files              Remove    Qualitative  Tests,   Commit│
│   sub-agents  first,                  AI cruft  feedback     types,         │
│   gather      --tdd for                         on design    lint,          │
│   context     test-first                                     build          │
│                                                                             │
│                                          /progress ◄────────────────────────┘
│                                          Save learnings for next time       │
│                                                                             │
│  ISSUES:                                                                    │
│  /backlog ──→ Document bugs/enhancements without implementing               │
│                                                                             │
│  HELP:                                                                      │
│  /learn ──→ Interactive help about Claude Code and the devkit               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Typical flows:

- **Quick fix:** implement → `/validate` → `/ship`
- **New feature:** `/plan` → implement → `/review` → `/validate` → `/ship`
- **Complex feature:** `/research` → `/plan --tdd` → implement → `/slop` → `/review` → `/validate` → `/progress` → `/ship`
- **New project:** `/greenfield` → `/plan [first feature]` → implement → ship

---

## Commands

### `/greenfield [idea]`

**Start a new project from scratch.**

Don't jump into code. Discover what you're actually building first.

```
> /greenfield I want to build a tool that helps developers track learning progress
```

What happens:
1. Interactive discovery through 6 phases (vision, problem, users, technical, validation, scoping)
2. Uses Socratic questioning to uncover requirements you haven't thought of
3. Creates three documents in `docs/`:
   - `SPEC.md` - What to build (requirements, users, success criteria)
   - `DESIGN.md` - How to build it (architecture, technology choices)
   - `PLAN.md` - Implementation roadmap (phases, tasks)
4. Suggests first feature to implement with `/plan`

Why it matters: Most projects fail from unclear requirements, not bad code. This forces clarity before you write a single line.

---

### `/learn [question]`

**Interactive help about Claude Code and the devkit.**

```
> /learn
> /learn how do hooks work?
> /learn what's the difference between /plan and /greenfield?
> /learn what skills are available?
```

What happens:
- No question: Shows welcome message with topic list
- Devkit question: Reads actual files and explains
- Claude Code question: Routes to official documentation

Why it matters: Self-service onboarding. Learn the system without reading all the docs.

---

### `/research [topic]`

**Deep research before you build.**

Don't let Claude guess. Have it actually investigate first.

```
> /research how should we implement caching in this project
```

What happens:
1. Claude analyzes your question + project context
2. Proposes a research plan (e.g., "I'll check existing patterns, framework docs, and community best practices")
3. You approve or adjust
4. Spawns multiple sub-agents **in parallel** to gather info
5. Synthesizes findings into actionable summary

Why it matters: Sub-agents do the messy exploration. Your main conversation stays clean with just the distilled knowledge.

---

### `/plan [--tdd] [feature]`

**Plan before you build. No assumptions.**

```
> /plan add rate limiting to the API
> /plan --tdd add rate limiting to the API   # Test-driven mode
```

What happens:
1. Claude **reads the actual files** that will be modified (required, not optional)
2. Asks clarifying questions if needed
3. Creates a detailed plan with:
   - Files to modify (with line numbers for complex changes)
   - Code snippets showing what will change
   - Why this approach (and alternatives considered)
   - Testing strategy
4. Waits for your approval before implementing

With `--tdd`:
- Converts requirements to test cases first
- Plans test file creation before implementation
- Follows red → green → refactor cycle

---

### `/backlog [bug|enh|ux] [description]`

**Document issues without implementing them.**

```
> /backlog bug the login form doesn't validate email format
> /backlog enh add dark mode support
> /backlog ux the submit button is hard to find
```

What happens:
1. Classifies as BUG, ENH (enhancement), or UX improvement
2. Investigates codebase to find root cause / affected files
3. Researches best practices (for enhancements)
4. Takes screenshots (for UX issues, if Playwright available)
5. Creates detailed entry in `BACKLOG.md`
6. Asks for next item (interactive loop)

Why it matters: Capture issues when you notice them. Implement later when you have time.

---

### `/review`

**Qualitative code review.**

```
> /review
```

Focuses on:
- Design patterns and architecture
- Code readability and maintainability
- Potential bugs or edge cases
- Consistency with existing codebase

This is the "does this code make sense?" check.

---

### `/slop`

**Remove AI-generated code smell.**

```
> /slop
```

Checks the diff against `main` and removes:
- **Over-commenting** (`// Get the user` before `getUser()`)
- **Defensive overkill** (null checks when TypeScript already enforces it)
- **Type escapes** (`as any`, `as unknown as X`)
- **Inconsistent style** (JSDoc in a file that doesn't use it)
- **Unnecessary try/catch** (wrapping code that doesn't throw)
- **Verbose logging** (logging every step)

Outputs a 1-3 sentence summary of what was cleaned.

Why it matters: AI code has tells. This removes them so your code looks like a human wrote it.

---

### `/validate`

**Quantitative checks.**

```
> /validate
```

Runs:
- TypeScript type checking (`tsc --noEmit`)
- Linting (`eslint`, `ruff`)
- Tests (`jest`, `pytest`)
- Build verification

This is the "does this code work?" check.

---

### `/progress [topic]`

**Save learnings for next time.**

```
> /progress
> /progress authentication system
```

After a research or exploration session, saves findings to `docs/YYYY-MM-DD-NNN-description.md`.

Example output:
```markdown
# Authentication System - Quick Reference

**Date:** 2025-12-04
**Context:** Researched how to add OAuth

**Key Files:**
- `src/auth/AuthController.ts:34` - Main entry point
- `src/auth/SessionManager.ts` - Redis-backed sessions

**Gotchas:**
- Always call `validateToken()` before `getUser()`
```

Why it matters: Next time you work on auth, Claude reads this instead of re-exploring from scratch.

---

### `/ship [commit message]`

**Commit with proper formatting.**

```
> /ship
> /ship feat: add rate limiting to API
```

What happens:
1. Runs `git status` and `git diff`
2. Analyzes changes
3. Creates a commit message following conventional format (`type(scope): message`)
4. Commits (doesn't push unless you ask)

---

## What's Running Behind the Scenes

The devkit isn't just commands. There's a lot happening automatically.

### Hooks (The Safety Net)

Hooks are Python scripts that run before/after Claude uses tools. They can **block execution**.

| Hook | When | What It Does |
|------|------|--------------|
| **Dangerous Command Blocker** | Before Bash | Blocks `rm -rf /`, `chmod 777`, force push, `sudo`, etc. |
| **Sensitive File Guard** | Before Read/Write | Blocks access to `.env`, credentials, SSH keys, `.kube/`, `.docker/` |
| **Auto-Format** | After Edit/Write | Runs Prettier (JS/TS) or Black (Python) |
| **Test-On-Change** | After Edit | Runs related tests when source files change |

These aren't warnings. Exit code 2 = execution blocked.

**Debug mode:** Set `CLAUDE_HOOK_DEBUG=1` to see what hooks are doing.

### Skills (Context-Aware Guidance)

Skills are specialized knowledge that auto-activates based on what you're working on.

| Skill | Activates When | Provides |
|-------|---------------|----------|
| `devkit-knowledge` | Using `/learn`, asking "how" questions | Architecture, commands, workflows |
| `product-discovery` | Using `/greenfield`, starting new projects | MVP scoping, requirements discovery |
| `api-design-patterns` | Working in `/api/`, `/routes/` | REST conventions, GraphQL patterns, error formats |
| `react-patterns` | Working with `.tsx`, `/components/` | Component patterns, hooks, state management |
| `tailwind-conventions` | Working with Tailwind | Class organization, layout patterns |
| `test-generator` | Working in `/tests/`, `*.test.*` | Jest/Pytest patterns, async testing |
| `error-handler` | Implementing error handling | Try/catch patterns, error boundaries |
| `code-formatter` | Any code file | Style guidelines, naming conventions |
| `documentation-templates` | Creating docs | README structure, API docs format |
| `frontend-design` | Working on pages/layouts | Hero sections, cards, dashboards |

### Agents (Specialized Workers)

Agents are sub-processes Claude can spawn for specific tasks.

| Agent | Purpose | When It's Used |
|-------|---------|----------------|
| `Explore` | Search and understand codebase | `/research`, understanding existing patterns |
| `documentation-researcher` | Find official docs | `/research`, checking library APIs |
| `code-reviewer` | Review code quality | `/review` |
| `debugger` | Analyze errors and stack traces | When errors occur |
| `git-helper` | Git operations | `/ship`, branch management |
| `spec-discovery` | Clarify requirements | When requirements are vague |
| `performance-optimizer` | Find performance issues | When optimizing code |
| `refactoring-assistant` | Safe code restructuring | When refactoring |

### Quality Gates

Two automated checks enforce quality:

**ConfidenceChecker** (before implementation):
- Scores confidence 0.0-1.0 across: requirements clarity, technical feasibility, dependencies, test strategy, risk
- Green (≥0.90): proceed
- Yellow (0.70-0.89): investigate gaps
- Red (<0.70): stop and clarify

**SelfCheck** (after implementation):
- Requires evidence for claims
- "Tests pass" must show actual test output
- Blocks phrases like "should work" or "probably fine"

### Reference Guides (Progressive Disclosure)

The devkit uses a **hub-and-spoke architecture**. The main `CLAUDE.md` is a lean navigation hub (~140 lines) that links to detailed reference guides:

| Reference | Content |
|-----------|---------|
| `style-guide.md` | Naming conventions, lint rules, TypeScript/Python specifics |
| `testing-guide.md` | Jest/Pytest patterns, directory structure, mocking |
| `environment.md` | Node.js, Python, Postgres setup |
| `commands-reference.md` | Common dev commands |
| `git-workflow.md` | Branching, commits, merge strategy |
| `agent-patterns.md` | When to spawn sub-agents, parallel research |

This keeps token usage low while providing deep knowledge on demand.

---

## FAQ

### Do I need all of this?

No. The components are modular:
- Just want safety? Install only the hooks
- Just want workflow? Install only the commands
- Want everything? Install it all

### Does this slow Claude down?

Hooks add a few milliseconds per tool use. You won't notice.

### Can I customize the blocked commands?

Yes. Edit `~/.claude/hooks/security/dangerous-command-blocker.py` and modify the `dangerous_patterns` list.

### What if a hook blocks something I actually want to do?

Run the command manually in your terminal, outside of Claude Code. The hooks only affect Claude's actions.

### Does this work with other AI coding tools?

There's a separate [Cursor version](https://github.com/benshapyro/cadre-devkit-cursor) with the same patterns adapted for Cursor's rule system.

### How do I debug hooks?

```bash
export CLAUDE_HOOK_DEBUG=1
claude
# Now hooks print debug info to stderr
```

### Can I add my own commands?

Yes. Create a `.md` file in `~/.claude/commands/` with this format:

```markdown
---
description: What this command does
argument-hint: [optional args]
---

# Command Name

Instructions for Claude when this command is invoked...
```

### Can I add my own skills?

Yes. Create a directory in `~/.claude/skills/my-skill/` with a `SKILL.md` file:

```markdown
---
name: my-skill
description: What this skill provides
---

# My Skill

Knowledge and patterns for Claude to use...
```

Then add activation triggers to `skill-rules.json`.

### Where are knowledge docs saved?

`/progress` saves to `docs/YYYY-MM-DD-NNN-description.md` in your project directory.

### How do I get help?

Run `/learn` for interactive help about the devkit and Claude Code.

---

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Commands** | 10 | `/greenfield`, `/plan`, `/research`, `/backlog`, `/review`, `/slop`, `/validate`, `/progress`, `/ship`, `/learn` |
| **Skills** | 10 | Product discovery, devkit knowledge, API design, React, Tailwind, testing, errors, formatting, docs, frontend |
| **Agents** | 7 | Code review, debugging, research, git, refactoring, performance, specs |
| **Hooks** | 4 | Dangerous command blocker, sensitive file guard, auto-format, test runner |
| **References** | 6 | Style guide, testing, environment, commands, git workflow, agent patterns |

---

## Documentation

| Doc | What's In It |
|-----|--------------|
| [Getting Started](docs/getting-started.md) | Extended tutorial with examples |
| [Components](docs/components.md) | Deep dive into every component |
| [Customization](docs/customization.md) | How to modify and extend |
| [Hook Development](docs/hook-development.md) | Creating custom hooks |
| [FAQ](docs/faq.md) | Common questions |

Or just run `/learn` for interactive help.

---

## Contributing

Found a bug? Want to add a feature? PRs welcome.

1. Fork the repo
2. Create a branch (`git checkout -b feat/my-feature`)
3. Make changes
4. Test locally by copying to `~/.claude/`
5. Submit a PR

---

## License

MIT
