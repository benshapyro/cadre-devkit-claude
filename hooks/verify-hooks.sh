#!/bin/bash
# Hook Verification Script
# Tests that all hooks are properly configured and functional

HOOKS_DIR="$HOME/.claude/hooks"
PASS=0
FAIL=0

echo "=== Hook Verification ==="
echo ""

# Test 1: Check files exist and are executable
echo "1. Checking hook files..."
for hook in \
    "$HOOKS_DIR/security/dangerous-command-blocker.py" \
    "$HOOKS_DIR/security/sensitive-file-guard.py" \
    "$HOOKS_DIR/formatting/auto-format.py" \
    "$HOOKS_DIR/testing/test-on-change.py" \
    "$HOOKS_DIR/skill-activation-prompt.sh"; do
    if [ -x "$hook" ]; then
        echo "   ✓ $(basename $hook)"
        ((PASS++))
    else
        echo "   ✗ $(basename $hook) - missing or not executable"
        ((FAIL++))
    fi
done

# Test 2: dangerous-command-blocker blocks rm -rf /
echo ""
echo "2. Testing dangerous-command-blocker..."
echo '{"tool_input":{"command":"rm -rf /"}}' | python3 "$HOOKS_DIR/security/dangerous-command-blocker.py" > /dev/null 2>&1
if [ $? -eq 2 ]; then
    echo "   ✓ Blocks 'rm -rf /'"
    ((PASS++))
else
    echo "   ✗ Failed to block 'rm -rf /'"
    ((FAIL++))
fi

echo '{"tool_input":{"command":"ls -la"}}' | python3 "$HOOKS_DIR/security/dangerous-command-blocker.py" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Allows safe commands"
    ((PASS++))
else
    echo "   ✗ Incorrectly blocked safe command"
    ((FAIL++))
fi

# Test 3: sensitive-file-guard blocks .env
echo ""
echo "3. Testing sensitive-file-guard..."
echo '{"tool_input":{"file_path":"/home/user/.env"}}' | python3 "$HOOKS_DIR/security/sensitive-file-guard.py" > /dev/null 2>&1
if [ $? -eq 2 ]; then
    echo "   ✓ Blocks .env files"
    ((PASS++))
else
    echo "   ✗ Failed to block .env"
    ((FAIL++))
fi

echo '{"tool_input":{"file_path":"/home/user/.env.example"}}' | python3 "$HOOKS_DIR/security/sensitive-file-guard.py" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Allows .env.example"
    ((PASS++))
else
    echo "   ✗ Incorrectly blocked .env.example"
    ((FAIL++))
fi

# Test 4: settings.json is valid
echo ""
echo "4. Validating settings.json..."
if jq . "$HOME/.claude/settings.json" > /dev/null 2>&1; then
    echo "   ✓ settings.json is valid JSON"
    ((PASS++))
else
    echo "   ✗ settings.json has JSON errors"
    ((FAIL++))
fi

# Summary
echo ""
echo "=== Results ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"

if [ $FAIL -eq 0 ]; then
    echo ""
    echo "All hooks verified successfully!"
    exit 0
else
    echo ""
    echo "Some tests failed. Check hook configuration."
    exit 1
fi
