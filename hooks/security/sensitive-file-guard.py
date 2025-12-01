#!/usr/bin/env python3
"""
Sensitive File Guard Hook
Prevents access to sensitive files containing credentials or secrets.
"""
import json
import sys
import os

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)  # Fail open on malformed input

file_path = data.get('tool_input', {}).get('file_path', '')
file_name = os.path.basename(file_path).lower()
file_path_lower = file_path.lower()

# ALLOW example/sample/template files - these don't contain real secrets
safe_suffixes = ['.example', '.sample', '.template', '.dist']
for suffix in safe_suffixes:
    if file_name.endswith(suffix):
        sys.exit(0)  # Allow these files

# Exact filename matches (most restrictive)
sensitive_filenames = [
    '.env', '.env.local', '.env.production', '.env.development',
    '.env.staging', '.env.test',
    'credentials.json', 'secrets.yaml', 'secrets.json',
    'id_rsa', 'id_ed25519', 'id_dsa', 'id_ecdsa',
    '.netrc', '.npmrc', '.pypirc',
]

# Extension matches (files ending with these - private keys only)
sensitive_extensions = [
    '.key', '.pem', '.p12', '.pfx',  # Note: .crt/.cer are public certs, not sensitive
]

# Path segment matches (these in any directory component)
sensitive_path_segments = [
    '.git/config',
    '.aws/credentials',
    '.ssh/config',
    '.ssh/known_hosts',
]

# Block exact filename matches
if file_name in sensitive_filenames:
    print(f"BLOCKED: Sensitive file: {file_path}", file=sys.stderr)
    print(f"Matched filename: {file_name}", file=sys.stderr)
    print(f"\nTo edit sensitive files, use your editor directly.", file=sys.stderr)
    sys.exit(2)

# Block any .env* files (catches .env.custom, .env.myapp, etc.)
if file_name.startswith('.env'):
    print(f"BLOCKED: Environment file: {file_path}", file=sys.stderr)
    print(f"\nTo edit .env files, use your editor directly.", file=sys.stderr)
    sys.exit(2)

# Block sensitive extensions
for ext in sensitive_extensions:
    if file_name.endswith(ext):
        print(f"BLOCKED: Sensitive file type: {file_path}", file=sys.stderr)
        print(f"Matched extension: {ext}", file=sys.stderr)
        print(f"\nTo edit sensitive files, use your editor directly.", file=sys.stderr)
        sys.exit(2)

# Block sensitive path segments
for segment in sensitive_path_segments:
    if segment in file_path_lower:
        print(f"BLOCKED: Sensitive path: {file_path}", file=sys.stderr)
        print(f"Matched segment: {segment}", file=sys.stderr)
        sys.exit(2)

# Block sensitive directories
sensitive_dirs = ['.ssh/', '.aws/', '.gnupg/']
for dir_pattern in sensitive_dirs:
    if dir_pattern in file_path_lower:
        print(f"BLOCKED: File in sensitive directory: {file_path}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
