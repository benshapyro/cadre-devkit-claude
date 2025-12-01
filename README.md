# Cadre DevKit for Claude Code

A comprehensive development toolkit for Claude Code that enforces quality standards, provides security guardrails, and streamlines workflows.

## Installation

```bash
/plugin install github:yourorg/cadre-devkit-claude
```

## Features

### Quality Gates
- **ConfidenceChecker** - Pre-implementation validation (5 criteria, 0.0-1.0 scale)
- **SelfCheck** - Post-implementation verification with evidence

### Security Hooks
- **Dangerous Command Blocker** - Prevents destructive commands (`rm -rf /`, force push, etc.)
- **Sensitive File Guard** - Blocks access to credentials, `.env`, SSH keys

### Workflow Commands
| Command | Purpose |
|---------|---------|
| `/plan [feature]` | Plan before implementing |
| `/review` | Review code changes |
| `/validate` | Run type checks, lint, tests, build |
| `/ship` | Create properly formatted commits |

### Skills (Auto-Activate)
- `api-design-patterns` - REST/GraphQL best practices
- `code-formatter` - Style guidelines
- `documentation-templates` - README, API docs
- `error-handler` - Exception handling patterns
- `test-generator` - Jest/Pytest test creation

### Agents (Auto-Activate)
- `code-reviewer` - Code quality review
- `debugger` - Error analysis
- `spec-discovery` - Requirements clarification
- `git-helper` - Git workflows
- `documentation-researcher` - Latest docs lookup
- `refactoring-assistant` - Safe code restructuring
- `performance-optimizer` - Performance analysis

## Usage

Skills and agents activate automatically based on your prompts. Use the workflow commands for the development lifecycle:

```
/plan add user authentication
[implement feature]
/review
/validate
/ship
```

## Configuration

The plugin uses `skill-rules.json` to determine when to suggest skills and agents based on:
- Keywords in your prompts
- Intent patterns (regex matching)
- File patterns being edited

## License

MIT
