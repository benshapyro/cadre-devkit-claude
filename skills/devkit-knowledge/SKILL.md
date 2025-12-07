---
name: devkit-knowledge
description: Knowledge base for the Cadre DevKit. Use when answering questions about the devkit structure, commands, skills, hooks, agents, or workflows.
---

# Cadre DevKit Knowledge Base

This skill helps you find information in the devkit. **Read the actual files** - they are the source of truth.

## Where to Find Things

Resources are path-agnostic - the skill and command systems handle location automatically.

| Topic | How to Access |
|-------|---------------|
| Commands | Use `/command-name` or find with Glob `**/commands/*.md` |
| Skills | Reference by name (e.g., "Use api-design-patterns skill") |
| Hooks | See Hooks section below for full documentation |
| References | Use `@references/filename.md` syntax |
| Agents | Use `Task` tool with `subagent_type` |

**Install Locations** (for reference only):
- **Marketplace:** `~/.claude/plugins/marketplaces/{marketplace-name}/`
- **Manual:** `~/.claude/`
- **Project:** `./.claude/` (takes precedence)

## Quick Answers

### How do I add a command?

**For plugin development:** Create `commands/my-command.md` in your plugin root
**For personal use:** Create `~/.claude/commands/my-command.md`

```markdown
---
description: What this command does
argument-hint: [optional args]
---

# My Command

Instructions for Claude...
```

### How do I add a skill?

**For plugin development:** Create `skills/my-skill/SKILL.md` in your plugin root
**For personal use:** Create `~/.claude/skills/my-skill/SKILL.md`

```yaml
---
name: my-skill-name
description: What it does and when to use it.
---

# My Skill

Instructions and examples...
```

### Skills vs Agents?

- **Skills** = Knowledge (methodology, templates, best practices)
- **Agents** = Workers (spawned via Task tool to do tasks independently)

Skills inform *how* to do something. Agents actually *do* things.

### Debug hooks not running?

1. Enable debug mode: `CLAUDE_HOOK_DEBUG=1`
2. Check `settings.json` has hook registered
3. Verify file is executable (`chmod +x`)

### Skill not activating?

1. Check YAML frontmatter is valid (name + description)
2. Ensure description has trigger keywords
3. Try explicit reference: "Use the X skill"

### Command workflow?

**New Project:**
```
/greenfield → SPEC.md + DESIGN.md + PLAN.md → /plan [feature] → implement → /review → /validate → /ship
```

**Existing Project:**
```
/plan [feature] → implement → /slop (optional) → /review → /validate → /ship
```

**Research:**
```
/research [topic] → findings → /progress (save as docs)
```

## Install Types & Precedence

| Install Type | Location | Scope |
|--------------|----------|-------|
| Project-local | `./.claude/` | This project only (highest priority) |
| Manual/Global | `~/.claude/` | All projects (personal) |
| Marketplace Plugin | `~/.claude/plugins/marketplaces/*/` | All projects (managed) |

**Precedence:** Project-local > Manual > Plugin

The skill and command systems automatically resolve paths based on this hierarchy.

## Hooks

Hooks are scripts that run automatically before or after tool use, enabling security guards and automation.

### Available Hooks

#### Security Hooks (PreToolUse)

**1. Dangerous Command Blocker**
- **Triggers:** Before any Bash command
- **Purpose:** Blocks destructive commands
- **Blocks:**
  - `rm -rf /` and variants
  - `chmod 777` and variants
  - `git push --force` to main/master
  - `:(){:|:&};:` (fork bomb)
  - Chained destructive commands
- **File:** `hooks/security/dangerous-command-blocker.py`

**2. Sensitive File Guard**
- **Triggers:** Before Read, Write, or Edit operations
- **Purpose:** Prevents accidental exposure of secrets
- **Blocks:**
  - `.env` (allows `.env.example`)
  - `credentials.json`
  - SSH keys (`.ssh/id_*`)
  - API keys, tokens, certificates
- **File:** `hooks/security/sensitive-file-guard.py`

#### Automation Hooks (PostToolUse)

**3. Auto-Format**
- **Triggers:** After Edit or Write operations
- **Purpose:** Automatically formats code
- **Formats:**
  - JavaScript/TypeScript → Prettier (if available)
  - Python → Black (if available)
  - Falls back gracefully if formatters not installed
- **File:** `hooks/formatting/auto-format.py`

**4. Test-On-Change**
- **Triggers:** After source file changes
- **Purpose:** Runs related tests automatically
- **Behavior:**
  - Detects test files matching changed source files
  - Runs tests in background
  - Reports pass/fail status
  - Skips if no related tests found
- **File:** `hooks/testing/test-on-change.py`

### Hook Configuration

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "path/to/hook.py"}]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "path/to/hook.py"}]
      }
    ]
  }
}
```

**For marketplace installs:** Hook paths are automatically configured during plugin installation.

### Debugging Hooks

Enable debug mode:
```bash
export CLAUDE_HOOK_DEBUG=1
claude
```

This shows:
- Which hooks are triggered
- Hook execution output
- Allow/block decisions

## For Everything Else

Read the actual files. This skill points you where to look - don't rely on this skill having the latest info.

---

## Version
- v3.0.0 (2025-12-06): Plugin-native refactor - path-agnostic resource resolution, comprehensive hooks documentation
- v2.0.0 (2025-12-05): Refactored to reference actual files instead of duplicating content
- v1.0.0 (2025-11-15): Initial version
