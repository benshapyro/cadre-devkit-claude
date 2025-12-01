# Frequently Asked Questions

## Installation & Setup

### How do I install the DevKit?

```
/plugin install github:benshapyro/cadre-devkit-claude
```

That's it - one command.

### How do I know it's working?

Try running `/plan test feature`. If Claude responds with a structured planning approach and asks clarifying questions, the DevKit is active.

You can also try typing "write a test" - you should see a note about relevant skills being detected.

### How do I update to the latest version?

```
/plugin update cadre-devkit-claude
```

### How do I uninstall it?

```
/plugin uninstall cadre-devkit-claude
```

---

## Using the DevKit

### Do I have to use the commands?

No. The DevKit works in the background even if you never use `/plan`, `/review`, etc. The security hooks and skill activation happen automatically.

But the commands are there to help - they encode best practices into a simple workflow.

### What's the difference between skills and agents?

**Skills** are knowledge bases - collections of best practices and patterns that Claude can reference.

**Agents** are specialized personas with defined approaches to problems.

Think of it like this:
- A **skill** is like a reference book on your desk
- An **agent** is like calling in a specialist consultant

### Why does Claude sometimes pause and ask about confidence?

That's the ConfidenceChecker. Before complex tasks, Claude assesses whether it has enough information to do a good job. If confidence is below 90%, it will:
1. Tell you which areas are uncertain
2. Ask specific questions to fill gaps
3. Only proceed when confident (or when you say "go ahead anyway")

This prevents Claude from charging ahead and building the wrong thing.

### Can I skip the confidence check?

Yes, just tell Claude to proceed:
- "Go ahead anyway"
- "I understand, please continue"
- "Skip the confidence check"

But consider whether you should - the check exists to prevent rework.

---

## Security

### Why was my command blocked?

The DevKit blocks commands that could be dangerous:
- Deleting system files (`rm -rf /`)
- Insecure permissions (`chmod 777`)
- Force pushing to main
- Accessing credentials

If you see "BLOCKED", it's protecting you from a potentially destructive action.

### I need to run a blocked command. What do I do?

Run it manually in your terminal, outside of Claude Code. The blocks only apply within Claude Code sessions.

If you think a command is being blocked incorrectly, check `docs/customization.md` for how to adjust the rules.

### Can Claude see my .env files?

No. The sensitive file guard blocks access to:
- `.env` and variants
- Credential files
- SSH keys
- AWS credentials

This is intentional - Claude shouldn't need access to secrets.

---

## Commands

### What does /plan do exactly?

1. Takes your feature description
2. Asks clarifying questions (scope, edge cases, requirements)
3. Creates a structured plan with:
   - Requirements checklist
   - Technical approach
   - Files to modify
   - Testing strategy
   - Risks and mitigations

### What does /review check?

- **Code quality**: Readability, duplication, complexity
- **Style**: Naming conventions, formatting, imports
- **Security**: Hardcoded secrets, injection risks, input validation
- **Error handling**: Try/catch, edge cases
- **Testing**: Coverage, meaningful tests

### What does /validate run?

1. Type checking (TypeScript: `tsc --noEmit`)
2. Linting (`npm run lint` or `ruff check`)
3. Tests (`npm test` or `pytest`)
4. Build (`npm run build`)

### Can I customize what /validate runs?

Yes - edit `commands/validate.md`. See `docs/customization.md` for details.

---

## Troubleshooting

### Skills aren't being suggested

Check that:
1. The plugin is installed (`/plugin list`)
2. Your prompt contains relevant keywords
3. The skill-rules.json file exists and is valid JSON

### A command isn't working

Make sure you're typing it correctly:
- `/plan` not `\plan` or `/Plan`
- Include a space before arguments: `/plan my feature`

### Claude seems to ignore the DevKit settings

Try starting a fresh session. Some settings only take effect at session start.

### The security hook is blocking something it shouldn't

You can customize the blocked patterns - see `docs/customization.md`. Or run the command manually outside Claude Code.

---

## General

### Does this slow Claude down?

Minimally. The hooks add a few milliseconds of processing. You won't notice it.

### Does this use more tokens/cost more?

The CLAUDE.md file adds some context, but it's small (~100 lines). The impact on token usage is minimal.

### Can I use this on personal projects?

Yes! The DevKit works anywhere you use Claude Code. It's not restricted to Cadre repos.

### Who maintains this?

The Cadre engineering team. If you find bugs or have suggestions, let us know in Slack or file an issue on the repo.

### How do I contribute improvements?

1. Make your changes locally
2. Test them
3. Submit a PR to the repo
4. Tag the team for review

---

## Still Have Questions?

- Check the other docs in this folder
- Ask in the team Slack channel
- File an issue on GitHub
