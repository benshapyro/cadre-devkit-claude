# Customizing the DevKit

Most people won't need to customize anything - the defaults work well. But if you want to tweak things, here's how.

## What Can Be Customized

| What | Where | Difficulty |
|------|-------|------------|
| When skills/agents activate | `skill-rules.json` | Easy |
| Security blocked commands | `hooks/security/dangerous-command-blocker.py` | Medium |
| Protected files | `hooks/security/sensitive-file-guard.py` | Medium |
| Workflow commands | `commands/*.md` | Medium |

## Customizing Skill Activation

The file `skill-rules.json` controls when skills and agents are suggested.

### Example: Add a Keyword Trigger

Say you want the test-generator to also activate when someone says "coverage":

**Before:**
```json
"test-generator": {
  "promptTriggers": {
    "keywords": ["test", "testing", "jest", "pytest"]
  }
}
```

**After:**
```json
"test-generator": {
  "promptTriggers": {
    "keywords": ["test", "testing", "jest", "pytest", "coverage"]
  }
}
```

### Example: Add a Pattern Trigger

You can also use regex patterns. Say you want debugger to activate on "why isn't this working":

```json
"debugger": {
  "promptTriggers": {
    "keywords": ["debug", "bug", "error"],
    "intentPatterns": ["fix.*bug", "why.*not.*work", "why isn't.*working"]
  }
}
```

## Customizing Blocked Commands

Edit `hooks/security/dangerous-command-blocker.py` to add or remove blocked patterns.

### Example: Block a New Pattern

Add to the `dangerous_patterns` list:

```python
dangerous_patterns = [
    r'rm\s+-rf\s+/',           # Already blocked
    r'chmod\s+777',            # Already blocked
    r'DROP\s+TABLE',           # NEW: Block SQL drops
    r'truncate\s+',            # NEW: Block truncate
]
```

### Example: Allow Something Currently Blocked

Remove or comment out the pattern:

```python
dangerous_patterns = [
    r'rm\s+-rf\s+/',
    # r'chmod\s+777',          # Commented out - now allowed
    r'sudo\s+',
]
```

## Customizing Protected Files

Edit `hooks/security/sensitive-file-guard.py` to change which files are protected.

### Example: Protect Additional Files

```python
sensitive_patterns = [
    '.env',                    # Already protected
    'credentials.json',        # Already protected
    'api_keys.txt',           # NEW
    'database.yml',           # NEW
]
```

### Example: Protect a Directory

```python
sensitive_dirs = [
    '.ssh/',                   # Already protected
    '.aws/',                   # Already protected
    'secrets/',               # NEW
    'config/production/',     # NEW
]
```

## Customizing Commands

Commands are Markdown files in the `commands/` folder. You can edit them to change behavior.

### Command Structure

```markdown
---
description: What this command does
allowed-tools: Bash(git:*), Read, Grep
argument-hint: [optional arguments]
---

# Command Name

Instructions for Claude on what to do when this command runs.

## Steps

1. Do this first
2. Then do this
3. Finally do this
```

### Example: Add a Step to /validate

Edit `commands/validate.md` and add a new section:

```markdown
### 6. Security Scan

**Run security audit:**
!`npm audit 2>&1 || true`
```

## Project-Level Overrides

You can override DevKit settings for a specific project by creating a `.claude/settings.json` in that project:

```json
{
  "plugins": {
    "cadre-devkit-claude": {
      "enabled": true,
      "settings": {
        "skipConfidenceCheck": false,
        "customKeywords": ["myproject-specific-term"]
      }
    }
  }
}
```

## Tips

1. **Test changes locally first** - Make sure your customization works before sharing
2. **Keep it simple** - Small changes are easier to debug
3. **Document why** - Add a comment explaining non-obvious customizations
4. **Share with the team** - If you find a useful customization, consider adding it to the main DevKit

## Need Help?

If you're trying to customize something and it's not working:
1. Check the FAQ (`docs/faq.md`)
2. Ask in the team Slack channel
3. File an issue on the repo
