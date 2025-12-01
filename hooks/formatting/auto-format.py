#!/usr/bin/env python3
"""
PostToolUse hook: Auto-format files after Edit/Write operations.
Runs formatters based on file extension.
"""
import json
import sys
import subprocess
import os

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

if not file_path or not os.path.exists(file_path):
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
    try:
        subprocess.run(
            formatters[ext] + [file_path],
            capture_output=True,
            timeout=10,
            check=True
        )
        print(f"✓ Formatted {file_path}")
    except FileNotFoundError:
        print(f"Formatter not available", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"Formatter timeout", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)

sys.exit(0)
