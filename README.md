# Cadre DevKit for Claude Code

A comprehensive development toolkit for Claude Code that enforces quality standards, provides security guardrails, and streamlines workflows.

**New to the DevKit?** Start with the [Getting Started Guide](docs/getting-started.md).

## Installation

### Option 1: Plugin Install (Recommended)

In Claude Code, run:

```
/plugin marketplace add benshapyro/cadre-devkit-claude
/plugin install cadre-devkit-claude
```

Then restart Claude Code to activate the plugin.

### Option 2: Manual Setup

If plugins aren't working, install manually:

```bash
# Clone the devkit
git clone https://github.com/benshapyro/cadre-devkit-claude.git
cd cadre-devkit-claude

# Run the install script
./install.sh
```

The script copies components to `~/.claude/` and shows you how to configure hooks.

### Configure Hooks (Required for Security Features)

After installation, add hooks to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security/dangerous-command-blocker.py"
          }
        ]
      },
      {
        "matcher": "Edit|Write|Read",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security/sensitive-file-guard.py"
          }
        ]
      }
    ]
  }
}
```

**Note:** Plugin install may configure hooks automatically. Check your settings after install.

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Commands** | 7 | `/plan`, `/research`, `/review`, `/slop`, `/validate`, `/progress`, `/ship` |
| **Skills** | 8 | API design, formatting, docs, errors, testing, React, Tailwind, frontend |
| **Agents** | 7 | Code review, debugging, refactoring, and more |
| **Hooks** | 5 | Security guards, auto-format, test runner, skill activation |

## Quick Start

```
/research how to add authentication  # Research first (optional)
/plan --tdd add user authentication  # Plan the feature (--tdd for test-driven)
[implement with Claude's help]       # Build it
/slop                                # Remove AI code slop
/review                              # Review your code
/validate                            # Run all checks
/progress                            # Save learnings (optional)
/ship                                # Commit with proper format
```

## Documentation

| Doc | What's In It |
|-----|--------------|
| [Getting Started](docs/getting-started.md) | Plain English intro - what this is, why use it, how it works |
| [Components](docs/components.md) | Detailed explanation of every command, skill, agent, and hook |
| [Customization](docs/customization.md) | How to tweak settings, add keywords, modify blocked commands |
| [FAQ](docs/faq.md) | Common questions and troubleshooting |
| [Changelog](CHANGELOG.md) | Version history and what's changed |

## Features at a Glance

### Quality Gates
- **ConfidenceChecker** - Pauses before complex work to verify understanding
- **SelfCheck** - Validates completed work with evidence

### Hooks

**Security (PreToolUse)**
- **Dangerous Command Blocker** - Prevents `rm -rf /`, force push, etc.
- **Sensitive File Guard** - Blocks access to `.env`, credentials, SSH keys (allows `.example` files)

**Automation (PostToolUse)**
- **Auto-Format** - Runs Prettier/Black after Edit/Write operations
- **Test-On-Change** - Runs related tests after source file changes

### Workflow Commands
| Command | Purpose |
|---------|---------|
| `/plan [--tdd] [feature]` | Plan before implementing (--tdd for test-driven) |
| `/research [topic]` | Deep research with parallel sub-agents |
| `/review` | Qualitative code review |
| `/slop` | Remove AI-generated code slop |
| `/validate` | Run type checks, lint, tests, build |
| `/progress` | Save research findings as knowledge docs |
| `/ship` | Create properly formatted commits |

### Skills (Auto-Activate)
- `api-design-patterns` - REST/GraphQL best practices
- `code-formatter` - Cadre style guidelines
- `documentation-templates` - README, API docs
- `error-handler` - Exception handling patterns
- `test-generator` - Jest/Pytest test creation

### Agents (Auto-Activate)
- `code-reviewer` - Code quality review
- `debugger` - Error analysis and root cause identification
- `spec-discovery` - Requirements clarification
- `git-helper` - Git workflow assistance
- `documentation-researcher` - Latest docs lookup
- `refactoring-assistant` - Safe code restructuring
- `performance-optimizer` - Performance analysis

## Need Help?

1. Check the [FAQ](docs/faq.md)
2. Read the [Getting Started Guide](docs/getting-started.md)
3. Ask in the team Slack channel

## License

MIT - See [LICENSE](LICENSE) for details.
