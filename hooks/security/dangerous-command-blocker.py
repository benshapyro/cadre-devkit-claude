#!/usr/bin/env python3
"""
Dangerous Command Blocker Hook
Blocks dangerous shell commands before execution.
"""
import json
import sys
import re

data = json.load(sys.stdin)
command = data.get('tool_input', {}).get('command', '')

dangerous_patterns = [
    r'rm\s+-rf\s+/',           # Recursive delete from root
    r'chmod\s+777',            # Overly permissive permissions
    r'sudo\s+',                # Elevated privileges
    r'dd\s+if=',               # Disk operations
    r'mkfs\.',                 # Format filesystem
    r'npm\s+publish',          # Accidental package publishing
    r'git\s+push.*--force',    # Force push
    r'mv\s+.*\s+/',            # Move to root
    r'>\s*/dev/',              # Write to system devices
]

for pattern in dangerous_patterns:
    if re.search(pattern, command):
        print(f"BLOCKED: Dangerous command pattern detected: {pattern}", file=sys.stderr)
        print(f"Command attempted: {command}", file=sys.stderr)
        print(f"\nIf this is intentional, run manually outside Claude Code.", file=sys.stderr)
        sys.exit(2)  # Exit code 2 blocks execution

sys.exit(0)  # Allow execution
