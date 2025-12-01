#!/bin/bash
# Cadre DevKit for Claude Code - Installation Script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing Cadre DevKit for Claude Code..."
echo ""

# Create directories
echo "Creating directories..."
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/hooks/security"

# Copy components
echo "Copying skills..."
cp -r "$SCRIPT_DIR/skills/"* "$CLAUDE_DIR/skills/" 2>/dev/null || echo "  No skills to copy"

echo "Copying commands..."
cp -r "$SCRIPT_DIR/commands/"* "$CLAUDE_DIR/commands/" 2>/dev/null || echo "  No commands to copy"

echo "Copying agents..."
cp -r "$SCRIPT_DIR/agents/"* "$CLAUDE_DIR/agents/" 2>/dev/null || echo "  No agents to copy"

echo "Copying hooks..."
cp -r "$SCRIPT_DIR/hooks/security/"* "$CLAUDE_DIR/hooks/security/" 2>/dev/null || echo "  No hooks to copy"
chmod +x "$CLAUDE_DIR/hooks/security/"*.py 2>/dev/null || true
chmod +x "$CLAUDE_DIR/hooks/security/"*.sh 2>/dev/null || true

# Handle settings.json
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
echo ""
echo "Configuring hooks..."

if [ -f "$SETTINGS_FILE" ]; then
    echo "  Found existing settings.json"
    echo ""
    echo "  ⚠️  MANUAL STEP REQUIRED:"
    echo "  Add the following to your $SETTINGS_FILE:"
    echo ""
else
    echo "  Creating new settings.json..."
    echo '{}' > "$SETTINGS_FILE"
fi

cat << 'HOOKS_CONFIG'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security/dangerous-command-blocker.py"
          }
        ]
      },
      {
        "matcher": "Edit|Write|Read",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security/sensitive-file-guard.py"
          }
        ]
      }
    ]
  }
}
HOOKS_CONFIG

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Add the hooks configuration above to ~/.claude/settings.json"
echo "  2. Copy CLAUDE.md to your project root"
echo "  3. Restart Claude Code"
echo "  4. Try: /plan test feature"
echo ""
echo "For help, see: docs/getting-started.md"
