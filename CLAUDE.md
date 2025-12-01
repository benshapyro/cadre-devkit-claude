# Ben's Claude Code Optimization Plugin

This plugin provides a comprehensive productivity and quality system for Claude Code.

## Features

### Pre-Implementation Confidence Check
Before starting any non-trivial implementation, Claude assesses confidence across 5 criteria:
- Requirements Clarity (25%)
- Technical Feasibility (25%)
- Dependency Verification (20%)
- Test Strategy (15%)
- Risk Assessment (15%)

**Decision Matrix:**
- GREEN (≥0.90): Proceed
- YELLOW (0.70-0.89): Investigate/clarify
- RED (<0.70): STOP and ask questions

### Post-Implementation SelfCheck
After completing work, Claude validates:
1. Are tests passing? (with evidence)
2. Are all requirements met?
3. No unverified assumptions?
4. Is there evidence of success?

### Security Hooks
- **Dangerous Command Blocker**: Prevents `rm -rf /`, `chmod 777`, force push, etc.
- **Sensitive File Guard**: Blocks access to `.env`, credentials, SSH keys

### Workflow Commands
- `/plan [feature]` - Plan before implementing
- `/review` - Review code changes
- `/validate` - Run all checks (types, lint, tests, build)
- `/ship` - Commit with proper formatting

### Skills
- **api-design-patterns** - REST/GraphQL best practices
- **code-formatter** - Style guidelines
- **documentation-templates** - README, API docs
- **error-handler** - Exception handling patterns
- **test-generator** - Jest/Pytest test creation

### Agents
- **code-reviewer** - Code quality review
- **debugger** - Error analysis
- **spec-discovery** - Requirements clarification
- **git-helper** - Git workflows
- **documentation-researcher** - Latest docs lookup
- **refactoring-assistant** - Safe code restructuring
- **performance-optimizer** - Performance analysis

## Usage

Skills and agents auto-activate based on your prompts. Use workflow commands for the development lifecycle:

```
/plan add user authentication
[implement feature]
/review
/validate
/ship
```
