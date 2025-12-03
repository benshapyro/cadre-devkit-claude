#!/bin/bash

# Skill Auto-Activation Hook
# Triggers skill suggestions based on user prompts and file context

# Get the project directory (defaults to current directory)
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Path to skill rules configuration
SKILL_RULES="$HOME/.claude/skill-rules.json"

# Check if skill-rules.json exists
if [ ! -f "$SKILL_RULES" ]; then
    exit 0
fi

# Read input from stdin (JSON with session_id, hook_type, etc.)
INPUT=$(cat)

# Extract user prompt from the input
USER_PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""')

# If no prompt, exit
if [ -z "$USER_PROMPT" ] || [ "$USER_PROMPT" = "null" ]; then
    exit 0
fi

# Convert prompt to lowercase for matching
USER_PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

# Match prompt against configured keyword patterns
MATCHED_SKILLS=$(jq -r --arg prompt "$USER_PROMPT_LOWER" '
  .skills | to_entries[] |
  select(
    (.value.promptTriggers.keywords // [] |
     any(. as $keyword | $prompt | contains($keyword | ascii_downcase)))
  ) |
  "\(.key):\(.value.priority // "medium")"
' "$SKILL_RULES" 2>/dev/null)

# Also match against intent patterns (regex)
INTENT_MATCHED=$(jq -r --arg prompt "$USER_PROMPT_LOWER" '
  .skills | to_entries[] |
  select(
    (.value.promptTriggers.intentPatterns // [] |
     any(. as $pattern | $prompt | test($pattern; "i")))
  ) |
  "\(.key):\(.value.priority // "medium")"
' "$SKILL_RULES" 2>/dev/null)

# Combine matches and sort by priority (high first), then deduplicate by skill name
# Format is "skillname:priority" - sort by priority field, keep first occurrence of each skill
ALL_MATCHED=$(echo -e "$MATCHED_SKILLS\n$INTENT_MATCHED" | grep -v '^$' | \
    awk -F: '{
        priority_order = ($2 == "high" ? 1 : ($2 == "medium" ? 2 : 3));
        print priority_order ":" $0
    }' | sort -t: -k1,1n | cut -d: -f2- | \
    awk -F: '!seen[$1]++')

# If we have matches, output skill suggestions
if [ -n "$ALL_MATCHED" ]; then
    # Extract just skill names for the message (already in priority order)
    SKILL_NAMES=$(echo "$ALL_MATCHED" | cut -d':' -f1 | tr '\n' ', ' | sed 's/,$//')

    # Output JSON with skill suggestions
    cat << EOF
{
  "additionalContext": "Relevant skills detected for this task: $SKILL_NAMES. Consider using the Skill tool to load these for best practices and patterns."
}
EOF
fi

exit 0
