#!/usr/bin/env python3
"""
Dangerous Command Blocker Hook (PreToolUse)
Blocks dangerous shell commands before execution.

Exit Codes:
  0 = Allow execution
  2 = Block execution (PreToolUse convention)

Debug: Set CLAUDE_HOOK_DEBUG=1 to enable verbose logging
"""
import json
import sys
import re
import os

DEBUG = os.environ.get('CLAUDE_HOOK_DEBUG', '0') == '1'

def debug(msg):
    if DEBUG:
        print(f"[dangerous-command-blocker] {msg}", file=sys.stderr)

# Handle malformed JSON gracefully
try:
    data = json.load(sys.stdin)
    debug(f"Received data: {json.dumps(data)[:200]}...")
except json.JSONDecodeError:
    debug("Malformed JSON input, allowing")
    sys.exit(0)  # Fail open on malformed input

command = data.get('tool_input', {}).get('command', '')
debug(f"Checking command: {command[:100]}...")

dangerous_patterns = [
    # Filesystem destruction
    (r'rm\s+-rf\s+/', "Recursive delete from root"),
    (r'rm\s+-rf\s+~', "Recursive delete from home"),
    (r'rm\s+-rf\s+\*', "Recursive delete wildcard"),

    # Dangerous permissions
    (r'chmod\s+(-R\s+)?777', "World-writable permissions (777)"),
    (r'chmod\s+(-R\s+)?a\+rwx', "World-writable permissions (a+rwx)"),

    # Elevated privileges
    (r'sudo\s+', "Elevated privileges"),

    # Disk/system operations
    (r'dd\s+if=', "Disk operations"),
    (r'mkfs\.', "Format filesystem"),

    # Accidental publishing/pushing
    (r'npm\s+publish', "Accidental package publishing"),
    (r'git\s+push.*--force', "Force push"),
    (r'git\s+push.*-f\b', "Force push (-f)"),

    # System device writes (but ALLOW /dev/null, /dev/zero, /dev/random, /dev/urandom)
    (r'>\s*/dev/(?!null|zero|u?random)', "Write to system device"),
]

for pattern, description in dangerous_patterns:
    if re.search(pattern, command):
        debug(f"MATCHED pattern: {pattern}")
        print(f"BLOCKED: {description}", file=sys.stderr)
        print(f"Pattern: {pattern}", file=sys.stderr)
        print(f"Command: {command}", file=sys.stderr)
        print(f"\nIf intentional, run manually outside Claude Code.", file=sys.stderr)
        sys.exit(2)  # Exit code 2 blocks execution

debug("No dangerous patterns matched, allowing")
sys.exit(0)  # Allow execution
