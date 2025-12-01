#!/usr/bin/env python3
"""
PostToolUse hook: Run tests after source file edits.
Skips test files themselves to avoid infinite loops.
"""
import json
import sys
import subprocess
import os

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

if not file_path:
    sys.exit(0)

# Only run tests for source files
test_extensions = ['.ts', '.tsx', '.js', '.jsx', '.py']
ext = os.path.splitext(file_path)[1]

if ext not in test_extensions:
    sys.exit(0)

# Skip test files themselves
if 'test' in file_path.lower() or '__tests__' in file_path:
    sys.exit(0)

# Skip config/hook files
if '.claude' in file_path:
    sys.exit(0)

# Determine test command
if ext == '.py':
    test_cmd = ['pytest', '-x', '-q', '--tb=short']
else:
    test_cmd = ['npm', 'test', '--', '--bail', '--findRelatedTests', file_path]

try:
    result = subprocess.run(
        test_cmd,
        capture_output=True,
        timeout=60,
        cwd=os.getcwd()
    )
    if result.returncode != 0:
        print(f"⚠️ Tests failed after editing {file_path}", file=sys.stderr)
        sys.exit(1)
    print(f"✓ Tests passing for {file_path}")
except FileNotFoundError:
    # Test runner not available - not an error
    pass
except subprocess.TimeoutExpired:
    print(f"Test timeout for {file_path}", file=sys.stderr)
except Exception as e:
    print(f"Could not run tests: {e}", file=sys.stderr)

sys.exit(0)
