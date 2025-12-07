---
description: Learn about Claude Code, the devkit, commands, skills, and workflows
argument-hint: [question or topic]
---

# Learn Command

Interactive help and teaching for Claude Code and the devkit.

**Before answering:** Use the devkit-knowledge skill for devkit architecture.

## Question Routing

Route the user's question to the appropriate source:

| Question Type | Action |
|---------------|--------|
| Claude Code features | Use `claude-code-guide` subagent |
| Devkit structure | Use devkit-knowledge skill |
| Specific command | Use Glob to find and read `**/commands/{command}.md` |
| Specific skill | Activate the {skill} skill by name |
| Workflows | Use devkit-knowledge skill |
| Hooks | Use devkit-knowledge skill (includes all hook documentation) |
| Troubleshooting | Combine sources as needed |

## Response Style

- **Concise first** - Give the direct answer
- **Then explain** - Add context if helpful
- **Show examples** - Concrete usage examples
- **Link to sources** - Point to files they can read

## Example Interactions

### "How do hooks work?"
1. Read devkit-knowledge skill for overview
2. Explain PreToolUse vs PostToolUse
3. Show example hook structure
4. Mention debug mode (`CLAUDE_HOOK_DEBUG=1`)

### "What's the difference between /plan and /greenfield?"
1. `/greenfield` = new project from scratch, creates SPEC/DESIGN/PLAN docs
2. `/plan` = specific feature in existing project
3. Use greenfield first, then plan for each feature

### "Show me all available commands"
1. List commands from devkit-knowledge
2. Brief description of each
3. Show the standard workflow

### "How do I add a custom skill?"
1. Create `skills/my-skill/SKILL.md` in your plugin or `~/.claude/skills/my-skill/SKILL.md` for personal use
2. Add to `skill-rules.json` with triggers
3. Reference from commands by skill name (skill system handles paths)
4. Show example structure

### "What can Claude Code do?"
1. Use `claude-code-guide` subagent for accurate info
2. Summarize key capabilities
3. Point to official documentation

## Dynamic Discovery

For questions about current setup:

```
"What commands are available?"
→ Use Glob to find `**/commands/*.md` and list them

"What skills do I have?"
→ List all registered skills from skill-rules.json knowledge

"Show me the hooks"
→ Use devkit-knowledge skill (includes hook documentation)
```

## Teaching Mode

If user says "teach me about X" or "explain X":
1. Start with the big picture
2. Break down into components
3. Give practical examples
4. Suggest hands-on exercises

Example exercise suggestions:
- "Try running `/plan --tdd add a hello endpoint` to see TDD mode"
- "Run `/research [topic]` to see parallel sub-agents in action"
- "Ask about hooks to learn how security blocking works"

## No Question Provided

If user just runs `/learn` without a question:

```
Welcome to the Cadre DevKit!

I can help you learn about:
- **Commands** - /greenfield, /plan, /review, /validate, /ship, etc.
- **Skills** - api-design, react-patterns, testing, and more
- **Hooks** - Security guards and automation
- **Agents** - Specialized helpers for debugging, reviewing, etc.
- **Workflows** - How everything fits together

What would you like to learn about?

Quick starts:
- "How do I start a new project?"
- "What's the workflow for shipping code?"
- "How do hooks protect me?"
- "What skills are available?"
```

## Claude Code Questions

For questions specifically about Claude Code (not the devkit):

Use Task tool with `claude-code-guide` subagent:
```
Task(
  subagent_type="claude-code-guide",
  prompt="User question: {question}"
)
```

This ensures accurate, up-to-date information from official docs.

## Devkit-Specific Questions

For devkit questions, combine:
1. devkit-knowledge skill (architecture overview)
2. Actual file reads (current state)
3. Examples from the skill files

Always ground answers in the actual files when possible.
