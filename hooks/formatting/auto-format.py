#!/usr/bin/env python3
"""
Auto-Format Hook (PostToolUse)
Runs formatters after Edit/Write operations based on file extension.

Exit Codes:
  0 = Success (or no action needed)
  1 = Formatter error (non-blocking, informational)

Debug: Set CLAUDE_HOOK_DEBUG=1 to enable verbose logging
"""
import json
import sys
import subprocess
import os

DEBUG = os.environ.get('CLAUDE_HOOK_DEBUG', '0') == '1'

def debug(msg):
    if DEBUG:
        print(f"[auto-format] {msg}", file=sys.stderr)

# Handle malformed JSON gracefully
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    debug("Malformed JSON input")
    sys.exit(0)

file_path = data.get('tool_input', {}).get('file_path', '')
debug(f"Checking file: {file_path}")

if not file_path or not os.path.exists(file_path):
    debug("File path empty or doesn't exist")
    sys.exit(0)

formatters = {
    '.ts': ['npx', 'prettier', '--write'],
    '.tsx': ['npx', 'prettier', '--write'],
    '.js': ['npx', 'prettier', '--write'],
    '.jsx': ['npx', 'prettier', '--write'],
    '.py': ['black', '--line-length', '100'],
}

ext = os.path.splitext(file_path)[1]
if ext in formatters:
    debug(f"Found formatter for extension: {ext}")
    try:
        result = subprocess.run(
            formatters[ext] + [file_path],
            capture_output=True,
            timeout=10,
            text=True
        )
        if result.returncode != 0:
            debug(f"Formatter returned non-zero: {result.returncode}")
            print(f"Formatter failed for {file_path}", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            sys.exit(1)
        print(f"✓ Formatted {file_path}")
    except FileNotFoundError:
        debug("Formatter not installed")
        pass
    except subprocess.TimeoutExpired:
        debug("Formatter timed out")
        print(f"Formatter timeout for {file_path}", file=sys.stderr)
else:
    debug(f"No formatter configured for extension: {ext}")

sys.exit(0)
