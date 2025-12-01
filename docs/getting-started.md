# Getting Started with Cadre DevKit

Welcome! This guide explains what the Cadre DevKit is and how to use it. No technical jargon - just plain English.

## What Is This Thing?

Think of the Cadre DevKit as a **co-pilot upgrade** for Claude Code.

Out of the box, Claude Code is like a smart assistant who can write code. The DevKit turns it into a smart assistant who:
- Knows Cadre's coding standards
- Double-checks before diving into complex work
- Protects you from accidentally running dangerous commands
- Has specialized knowledge for common tasks (testing, debugging, API design, etc.)

**Analogy:** It's like giving a new employee our company handbook, security training, and best practices guide - but for Claude.

## Why Should I Use It?

### Without the DevKit
- Claude might use different coding styles than we do
- No guardrails against accidentally deleting files or exposing secrets
- You have to remember to ask for code reviews, run tests, etc.
- Claude starts coding immediately, even when requirements are unclear

### With the DevKit
- Claude follows Cadre conventions automatically
- Dangerous commands are blocked before they run
- Built-in workflow: plan → review → validate → ship
- Claude pauses to assess confidence before complex work

## Installation (2 minutes)

Open Claude Code and run:

```
/plugin install github:benshapyro/cadre-devkit-claude
```

That's it. The DevKit is now active.

## How to Use It

### The Short Version

Just use Claude Code normally. The DevKit works in the background:
- It suggests relevant tools based on what you're asking
- It blocks dangerous commands automatically
- It enforces quality checks on complex tasks

### The Workflow Commands

These are your main tools. Use them in order:

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/plan add user login` | Starting a new feature | Helps you think through requirements before coding |
| `/review` | After making changes | Reviews your code against Cadre standards |
| `/validate` | Before committing | Runs type checks, linting, tests, and build |
| `/ship` | Ready to commit | Creates a properly formatted commit message |

**Example workflow:**

```
You: /plan add password reset feature

Claude: [Asks clarifying questions about requirements]
Claude: [Creates a structured plan]

You: [Implement the feature with Claude's help]

You: /review

Claude: [Reviews code for quality, security, style]

You: /validate

Claude: [Runs tests, checks types, builds project]
Claude: "All checks pass. Ready to ship."

You: /ship

Claude: [Creates commit with proper message format]
```

### Automatic Help

The DevKit watches what you're asking and offers relevant tools:

| If You Say... | DevKit Suggests... |
|---------------|-------------------|
| "Write tests for the user service" | test-generator skill |
| "This function is throwing an error" | debugger agent |
| "Create a REST API endpoint" | api-design-patterns skill |
| "I need to refactor this class" | refactoring-assistant agent |

You don't have to do anything - suggestions appear automatically.

## The Safety Net

### Commands That Get Blocked

The DevKit prevents accidentally running dangerous commands:

- `rm -rf /` - Would delete everything
- `chmod 777` - Makes files insecure
- `git push --force` to main - Could overwrite team's work
- Any command touching `.env` or credential files

If you try to run something dangerous, you'll see:
```
BLOCKED: Dangerous command pattern detected
If this is intentional, run manually outside Claude Code.
```

### The Confidence Check

Before complex work, Claude will assess its confidence:

```
Confidence Assessment:
- Requirements Clarity: 0.95 ✓
- Technical Feasibility: 0.85 ⚠
- Dependencies: 0.90 ✓
- Test Strategy: 0.80 ⚠
- Risk Assessment: 0.90 ✓

Overall: 0.88 (YELLOW)

I'm not fully confident about the technical approach.
Can you clarify: [specific questions]
```

This prevents Claude from charging ahead when it should be asking questions.

## Quick Reference

### Commands
- `/plan [feature]` - Plan before building
- `/review` - Review your changes
- `/validate` - Run all checks
- `/ship` - Commit your work

### What's Running in the Background
- **ConfidenceChecker** - Pauses on complex tasks to verify understanding
- **SelfCheck** - Verifies work is complete with evidence
- **Security hooks** - Blocks dangerous commands
- **Skill activation** - Suggests relevant tools automatically

## Next Steps

1. **Try it out** - Start a Claude Code session and run `/plan test feature`
2. **Read the FAQ** - See `docs/faq.md` for common questions
3. **Learn the components** - See `docs/components.md` for details on each piece

## Getting Help

- **Something not working?** Check `docs/faq.md`
- **Want to customize?** See `docs/customization.md`
- **Found a bug?** Let the team know in Slack
