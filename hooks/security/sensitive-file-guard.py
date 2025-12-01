#!/usr/bin/env python3
"""
Sensitive File Guard Hook
Prevents access to sensitive files containing credentials or secrets.
"""
import json
import sys

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

sensitive_patterns = [
    '.env', '.env.local', '.env.production', '.env.development',
    '.key', '.pem', '.p12', '.pfx',
    'credentials.json', 'secrets.yaml', 'secrets.json',
    '.git/config', 'id_rsa', 'id_ed25519', 'id_dsa',
    '.aws/credentials', '.ssh/config', 'password', 'secret',
]

for pattern in sensitive_patterns:
    if pattern in file_path.lower():
        print(f"BLOCKED: Sensitive file access detected: {file_path}", file=sys.stderr)
        print(f"Pattern matched: {pattern}", file=sys.stderr)
        print(f"\nTo edit sensitive files, use your editor directly.", file=sys.stderr)
        sys.exit(2)

sensitive_dirs = ['.ssh/', '.aws/', '.gnupg/', 'secrets/', 'private/']
for dir_pattern in sensitive_dirs:
    if dir_pattern in file_path:
        print(f"BLOCKED: File in sensitive directory: {file_path}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
