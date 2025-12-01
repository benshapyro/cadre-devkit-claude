# Cadre DevKit for Claude Code

A comprehensive development toolkit for Claude Code that enforces quality standards, provides security guardrails, and streamlines workflows.

**New to the DevKit?** Start with the [Getting Started Guide](docs/getting-started.md).

## Installation

```bash
/plugin install github:benshapyro/cadre-devkit-claude
```

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Commands** | 4 | `/plan`, `/review`, `/validate`, `/ship` |
| **Skills** | 5 | API design, formatting, docs, errors, testing |
| **Agents** | 7 | Code review, debugging, refactoring, and more |
| **Hooks** | 3 | Security guards + skill auto-activation |

## Quick Start

```
/plan add user authentication    # Plan the feature
[implement with Claude's help]   # Build it
/review                          # Review your code
/validate                        # Run all checks
/ship                           # Commit with proper format
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

### Security Hooks
- **Dangerous Command Blocker** - Prevents `rm -rf /`, force push, etc.
- **Sensitive File Guard** - Blocks access to `.env`, credentials, SSH keys

### Workflow Commands
| Command | Purpose |
|---------|---------|
| `/plan [feature]` | Plan before implementing |
| `/review` | Review code changes |
| `/validate` | Run type checks, lint, tests, build |
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
