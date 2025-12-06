---
description: Learn about Claude Code, the devkit, commands, skills, and workflows
argument-hint: [question or topic]
---

# Learn Command

Interactive help and teaching for Claude Code and the devkit.

**Before answering:** Read `.claude/skills/devkit-knowledge/SKILL.md` for devkit architecture.

## Question Routing

Route the user's question to the appropriate source:

| Question Type | Action |
|---------------|--------|
| Claude Code features | Use `claude-code-guide` subagent |
| Devkit structure | Reference devkit-knowledge skill |
| Specific command | Read `.claude/commands/{command}.md` |
| Specific skill | Read `.claude/skills/{skill}/SKILL.md` |
| Workflows | Reference devkit-knowledge skill |
| Hooks | Read `.claude/hooks/` + devkit-knowledge |
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
1. Create `.claude/skills/my-skill/SKILL.md`
2. Add to `skill-rules.json` with triggers
3. Reference from commands with explicit path
4. Show example structure

### "What can Claude Code do?"
1. Use `claude-code-guide` subagent for accurate info
2. Summarize key capabilities
3. Point to official documentation

## Dynamic Discovery

For questions about current setup, actually read the files:

```
"What commands are available?"
→ Read files in .claude/commands/ and list them

"What skills do I have?"
→ Read directories in .claude/skills/ and summarize

"Show me the hooks"
→ Read .claude/hooks/ structure and explain each
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
- "Check `.claude/hooks/security/` to see how blocking works"

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
