# Hook Development Guide

A guide to creating custom hooks for Claude Code.

## Overview

Hooks allow you to run custom scripts before or after Claude Code tool executions. They enable:
- **Security guards** - Block dangerous operations
- **Automation** - Auto-format code, run tests
- **Validation** - Check inputs before execution
- **Logging** - Track tool usage

## Hook Types

### PreToolUse
Runs **before** a tool executes. Can block execution.

**Use cases:**
- Security validation (block dangerous commands)
- Permission checks (prevent sensitive file access)
- Input validation

**Exit codes:**
- `0` = Allow execution
- `2` = Block execution (tool will not run)

### PostToolUse
Runs **after** a tool executes. Cannot block, only react.

**Use cases:**
- Auto-formatting edited files
- Running tests after changes
- Logging/notifications

**Exit codes:**
- `0` = Success
- `1` = Warning/error (informational, non-blocking)

## Configuration

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security/my-hook.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/my-hook.py"
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns
- Single tool: `"Bash"`
- Multiple tools: `"Edit|Write|Read"`
- All tools: `"*"` (use with caution)

## Hook Input

Hooks receive JSON on stdin with tool execution context:

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  },
  "session_id": "...",
  "hook_type": "PreToolUse"
}
```

### Common Fields by Tool

**Bash:**
```json
{ "tool_input": { "command": "npm test" } }
```

**Edit/Write/Read:**
```json
{ "tool_input": { "file_path": "/path/to/file" } }
```

## Hook Template (Python)

```python
#!/usr/bin/env python3
"""
My Custom Hook (PreToolUse|PostToolUse)
Description of what this hook does.

Exit Codes:
  0 = Allow/Success
  2 = Block (PreToolUse only)
  1 = Warning (PostToolUse only)

Debug: Set CLAUDE_HOOK_DEBUG=1 to enable verbose logging
"""
import json
import sys
import os

# Debug mode support
DEBUG = os.environ.get('CLAUDE_HOOK_DEBUG', '0') == '1'

def debug(msg):
    if DEBUG:
        print(f"[my-hook] {msg}", file=sys.stderr)

# Parse input
try:
    data = json.load(sys.stdin)
    debug(f"Received: {json.dumps(data)[:200]}")
except json.JSONDecodeError:
    debug("Malformed JSON input")
    sys.exit(0)  # Fail open

# Extract relevant data
tool_input = data.get('tool_input', {})
# file_path = tool_input.get('file_path', '')
# command = tool_input.get('command', '')

# Your logic here
# ...

# Exit appropriately
debug("Check passed")
sys.exit(0)
```

## Best Practices

### 1. Fail Open
If input is malformed or unexpected, allow execution rather than blocking:
```python
except json.JSONDecodeError:
    sys.exit(0)  # Don't block on bad input
```

### 2. Add Debug Mode
Support `CLAUDE_HOOK_DEBUG=1` environment variable:
```python
DEBUG = os.environ.get('CLAUDE_HOOK_DEBUG', '0') == '1'
```

### 3. Document Exit Codes
Always document what each exit code means in the docstring.

### 4. Keep Hooks Fast
Hooks run on every matching tool call. Keep execution time < 1 second.

### 5. Use Specific Matchers
Don't use `"*"` matcher unless necessary. Target specific tools.

### 6. Handle Edge Cases
- Empty file paths
- Missing keys in tool_input
- Unusual characters in paths

## Debugging

Enable debug mode:
```bash
export CLAUDE_HOOK_DEBUG=1
```

Test hook directly:
```bash
echo '{"tool_input": {"command": "rm -rf /"}}' | python3 ~/.claude/hooks/security/my-hook.py
echo $?  # Check exit code
```

## Directory Structure

```
~/.claude/
├── hooks/
│   ├── security/
│   │   ├── dangerous-command-blocker.py
│   │   └── sensitive-file-guard.py
│   ├── formatting/
│   │   └── auto-format.py
│   └── testing/
│       └── test-on-change.py
├── settings.json  # Hook configuration
└── docs/
    └── hook-development.md  # This guide
```

## Common Patterns

### Block Dangerous Commands
```python
dangerous_patterns = [
    (r'rm\s+-rf\s+/', "Delete from root"),
    (r'sudo\s+', "Elevated privileges"),
]

for pattern, description in dangerous_patterns:
    if re.search(pattern, command):
        print(f"BLOCKED: {description}", file=sys.stderr)
        sys.exit(2)
```

### Protect Sensitive Files
```python
sensitive_files = ['.env', 'credentials.json', 'id_rsa']
file_name = os.path.basename(file_path).lower()

if file_name in sensitive_files:
    print(f"BLOCKED: Sensitive file", file=sys.stderr)
    sys.exit(2)
```

### Auto-Format on Edit
```python
formatters = {
    '.ts': ['npx', 'prettier', '--write'],
    '.py': ['black'],
}

ext = os.path.splitext(file_path)[1]
if ext in formatters:
    subprocess.run(formatters[ext] + [file_path])
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not running | Check matcher pattern in settings.json |
| Hook blocking unexpectedly | Enable debug mode, check patterns |
| Hook output not visible | Output goes to stderr, not stdout |
| Permission denied | Check file permissions: `chmod +x hook.py` |
| JSON parse error | Ensure hook reads from stdin correctly |

## Resources

- [Claude Code Hooks Documentation](https://docs.anthropic.com/claude-code/hooks)
- [Hook Configuration Reference](https://docs.anthropic.com/claude-code/settings#hooks)
