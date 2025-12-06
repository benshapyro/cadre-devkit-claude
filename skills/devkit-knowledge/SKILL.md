---
name: devkit-knowledge
description: Knowledge base for the Cadre DevKit. Use when answering questions about the devkit structure, commands, skills, hooks, agents, or workflows.
---

# Cadre DevKit Knowledge Base

This skill contains everything needed to teach users about the devkit.

## Architecture Overview

```
.claude/
├── commands/        # Slash commands (/plan, /ship, etc.)
├── skills/          # Domain expertise (api-design, testing, etc.)
├── agents/          # Specialized sub-agents (debugger, reviewer, etc.)
├── hooks/           # Lifecycle hooks (security, formatting, testing)
├── references/      # Progressive disclosure docs
├── config/          # Helper procedures
└── skill-rules.json # Activation triggers
```

## Commands (Workflows)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/greenfield` | Discover & spec new projects | Starting from scratch, new idea |
| `/plan` | Plan feature implementation | Adding to existing project |
| `/research` | Deep parallel research | Need to explore unknowns |
| `/backlog` | Document bugs/enhancements | Track issues without implementing |
| `/review` | Qualitative code review | Before validation |
| `/validate` | Automated checks (types, lint, test) | Before shipping |
| `/ship` | Git commit workflow | Ready to commit |
| `/progress` | Save research as knowledge | After learning something reusable |
| `/slop` | Remove AI code artifacts | Clean up over-commenting, etc. |

### Command Workflow

**New Project:**
```
/greenfield → SPEC.md + DESIGN.md + PLAN.md
    ↓
/plan [first feature]
    ↓
implement → /review → /validate → /ship
```

**Existing Project:**
```
/plan [feature]
    ↓
implement → /slop (optional) → /review → /validate → /ship
```

**Research Flow:**
```
/research [topic] → findings → /progress (save as docs)
```

## Skills (Domain Expertise)

Skills provide specialized knowledge. They activate based on keywords or file patterns.

| Skill | Domain | Activates When |
|-------|--------|----------------|
| `product-discovery` | MVP scoping, requirements | New project, greenfield |
| `api-design-patterns` | REST/GraphQL APIs | Building endpoints |
| `react-patterns` | React components, hooks | Frontend React work |
| `tailwind-conventions` | CSS styling | Tailwind classes |
| `test-generator` | Jest/Pytest testing | Writing tests |
| `code-formatter` | Style guidelines | Formatting, linting |
| `error-handler` | Exception handling | Error patterns |
| `documentation-templates` | README, API docs | Writing docs |
| `frontend-design` | UI/UX principles | Design work |

### Skill Structure

Each skill lives in `.claude/skills/{name}/SKILL.md` and contains:
- Methodology and best practices
- Code examples and templates
- Do's and don'ts
- Quick reference tables

### How Skills Activate

1. **Keyword triggers** - User prompt contains relevant words
2. **File triggers** - User is working on matching file patterns
3. **Command reference** - Command explicitly says "Read .claude/skills/..."

## Agents (Specialized Sub-Agents)

Agents are spawned for specific tasks using the Task tool.

| Agent | Purpose | Tools Available |
|-------|---------|-----------------|
| `code-reviewer` | Code quality review | Read, Grep, Glob |
| `debugger` | Error analysis | Read, Grep, Bash, Glob |
| `spec-discovery` | Requirements clarification | Read, Grep, Glob |
| `documentation-researcher` | External docs lookup | WebSearch, WebFetch, Ref |
| `git-helper` | Git operations | Bash, Read, Grep, Glob |
| `refactoring-assistant` | Safe refactoring | Read, Grep, Glob, Edit |
| `performance-optimizer` | Speed optimization | Read, Grep, Glob, Bash |

### When to Use Agents

- **Complex tasks** - Spawn agent to handle independently
- **Parallel work** - Multiple agents can run simultaneously
- **Research** - Agents explore while keeping main context clean

## Hooks (Lifecycle Events)

Hooks run automatically at specific points.

### PreToolUse Hooks (Can Block)

| Hook | Protects Against |
|------|------------------|
| `dangerous-command-blocker` | `rm -rf /`, `chmod 777`, `sudo`, force push |
| `sensitive-file-guard` | `.env`, SSH keys, credentials, secrets |

**Exit codes:** 0 = allow, 2 = block

### PostToolUse Hooks (Automation)

| Hook | Action |
|------|--------|
| `auto-format` | Runs Prettier (JS/TS) or Black (Python) |
| `test-on-change` | Runs related tests after edits |

**Exit codes:** 0 = success, 1 = warning (non-blocking)

### Debug Mode

Enable with environment variable:
```bash
CLAUDE_HOOK_DEBUG=1  # Claude Code
CURSOR_HOOK_DEBUG=1  # Cursor
```

## References (Progressive Disclosure)

Load detailed content on-demand:

| Reference | Content |
|-----------|---------|
| `style-guide.md` | Naming conventions, lint rules |
| `testing-guide.md` | Test frameworks, patterns |
| `environment.md` | Node, Python, setup |
| `commands-reference.md` | Common dev commands |

**Usage:** Reference with `@.claude/references/style-guide.md`

## Configuration Files

| File | Purpose |
|------|---------|
| `skill-rules.json` | Keyword/pattern triggers for skills & agents |
| `settings.json` | Claude Code settings, hook registration |
| `CLAUDE.md` | Project-level instructions |

## Common Questions

### How do I add a new command?

1. Create `.claude/commands/my-command.md`
2. Add YAML frontmatter with description
3. Write the command instructions

```markdown
---
description: What this command does
argument-hint: [optional args]
---

# My Command

Instructions for Claude...
```

### How do I add a new skill?

1. Create `.claude/skills/my-skill/SKILL.md`
2. Add to `skill-rules.json` with activation triggers
3. Reference from commands with explicit path

### How do I add a hook?

1. Create script in `.claude/hooks/{category}/`
2. Register in `settings.json` under hooks section
3. Return exit code 0 (allow), 1 (warn), or 2 (block)

### What's the difference between skills and agents?

- **Skills** = Knowledge (methodology, templates, best practices)
- **Agents** = Workers (spawned to do specific tasks independently)

Skills inform how to do something. Agents actually do things.

### How do commands reference skills?

Commands include explicit file paths:
```markdown
**Before starting:** Read `.claude/skills/product-discovery/SKILL.md`
```

This tells Claude to load the skill content before proceeding.

## Troubleshooting

### Hook not running?
1. Check `settings.json` has hook registered
2. Verify file is executable (`chmod +x`)
3. Enable debug mode: `CLAUDE_HOOK_DEBUG=1`

### Skill not activating?
1. Check `skill-rules.json` has matching keywords
2. Try explicit reference in prompt
3. Verify skill file exists at expected path

### Command not found?
1. Check file exists in `.claude/commands/`
2. Verify YAML frontmatter is valid
3. Restart Claude Code session

## Devkit vs Global Config

| Location | Scope | Use For |
|----------|-------|---------|
| `~/.claude/` | All projects | Personal preferences, global skills |
| `./.claude/` | This project only | Project-specific config |

Project-level config takes precedence over global.
