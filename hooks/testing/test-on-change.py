#!/usr/bin/env python3
"""
Test-On-Change Hook (PostToolUse)
Runs tests after source file edits. Skips test files to avoid infinite loops.

Exit Codes:
  0 = Success (or no action needed)
  1 = Tests failed (non-blocking warning)

Debug: Set CLAUDE_HOOK_DEBUG=1 to enable verbose logging
"""
import json
import sys
import subprocess
import os

DEBUG = os.environ.get('CLAUDE_HOOK_DEBUG', '0') == '1'

def debug(msg):
    if DEBUG:
        print(f"[test-on-change] {msg}", file=sys.stderr)

# Handle malformed JSON gracefully
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    debug("Malformed JSON input")
    sys.exit(0)

file_path = data.get('tool_input', {}).get('file_path', '')
debug(f"Checking file: {file_path}")

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

# Skip .claude directory (config/hook files) - check path components properly
path_parts = file_path.split(os.sep)
if '.claude' in path_parts:
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
