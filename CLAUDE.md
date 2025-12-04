# Cadre DevKit for Claude Code

This plugin provides a comprehensive productivity and quality system for Claude Code.

## Features

### Pre-Implementation Confidence Check

Before starting ANY non-trivial implementation, assess confidence across 5 criteria (0.0-1.0 scale):

## Assessment Criteria

| Criterion | Weight | Key Questions |
|-----------|--------|---------------|
| **Requirements Clarity** | 25% | Are requirements explicit? Acceptance criteria defined? Edge cases identified? |
| **Technical Feasibility** | 25% | Is approach verified? APIs available? Stack compatible? |
| **Dependency Verification** | 20% | Dependencies accessible? Versions compatible? Infrastructure ready? |
| **Test Strategy** | 15% | How will this be tested? Tools available? Test cases defined? |
| **Risk Assessment** | 15% | Failure modes known? Mitigation defined? Rollback possible? |

## Decision Matrix

| Overall Score | Status | Action |
|---------------|--------|--------|
| **≥0.90** | GREEN | Proceed with implementation |
| **0.70-0.89** | YELLOW | Investigate alternatives, clarify ambiguity, document assumptions |
| **<0.70** | RED | STOP - Ask clarifying questions, research unknowns, then re-assess |

## Enforcement

**NEVER proceed with confidence <0.90 without explicit user approval.**

If confidence is below 0.90:
1. State current confidence score with breakdown
2. Identify weak areas (any criterion <0.80)
3. Ask specific questions OR conduct research
4. Recalculate after new information
5. Only proceed when ≥0.90 or user explicitly approves lower confidence

## When to Skip

Skip confidence check for:
- Simple edits (typos, formatting, comments)
- Direct user instructions with clear scope
- Tasks where requirements are already verified in conversation

### Post-Implementation SelfCheck

After completing ANY non-trivial implementation, answer these 4 questions with evidence:

## Q1: Are tests passing?
- Provide actual test output (not "tests pass" without proof)
- Show test command executed and pass/fail counts

## Q2: Are all requirements met?
- Map each requirement to implementation (file:line references)
- Confirm nothing was missed or assumed

## Q3: No unverified assumptions?
- External APIs/libraries verified with documentation
- Avoid "should work" or "typically..." language

## Q4: Is there evidence?
- Include test results, validation output, or build success
- Avoid "probably works" or "should be fine"

## Red Flags (Avoid)
- Claiming success without output
- "Everything works" without evidence
- Ignoring warnings or errors
- Speculation instead of verification

## When to Skip

Skip SelfCheck for:
- Simple edits (typos, formatting, config)
- Exploratory/research tasks
- When user explicitly confirms completion


### Red Flags (NEVER Use These)

These indicate hallucination - immediate failure:
1. "Tests passing" without actual output shown
2. "Everything works" without specific evidence
3. Implementation complete with failing tests
4. Skipped error messages or warnings
5. "Probably works" or "should work" language
6. "Likely..." or "typically..." speculation
7. Claims without concrete proof

**Detection Rate:** 94% hallucination prevention

## Components

### Hooks

#### Security (PreToolUse)
- **Dangerous Command Blocker**: Prevents `rm -rf /`, `chmod 777`, force push, etc.
- **Sensitive File Guard**: Blocks access to `.env`, credentials, SSH keys (allows .example files)

#### Automation (PostToolUse)
- **Auto-Format**: Runs Prettier/Black after Edit/Write operations
- **Test-On-Change**: Runs related tests after source file changes

### Workflow Commands
- `/plan [--tdd] [feature]` - Plan before implementing (--tdd for test-driven)
- `/research [topic]` - Deep research with parallel sub-agents
- `/review` - Qualitative code review
- `/validate` - Quantitative checks (types, lint, tests, build)
- `/progress` - Save research findings as knowledge docs
- `/ship` - Commit with proper formatting

### Skills
- **api-design-patterns** - REST/GraphQL best practices
- **code-formatter** - Style guidelines
- **documentation-templates** - README, API docs
- **error-handler** - Exception handling patterns
- **test-generator** - Jest/Pytest test creation

### Agents
- **code-reviewer** - Code quality review
- **debugger** - Error analysis
- **spec-discovery** - Requirements clarification
- **git-helper** - Git workflows
- **documentation-researcher** - Latest docs lookup

### References (Progressive Disclosure)
Load detailed content on-demand with `@references/filename.md`:
- `style-guide.md` - Naming conventions, lint rules
- `testing-guide.md` - Test frameworks, coverage guidelines
- `environment.md` - Node, Python, Postgres setup
- `commands-reference.md` - Common dev commands

## Usage

Skills and agents auto-activate based on your prompts. Use workflow commands for the development lifecycle:

```
/plan add user authentication
[implement feature]
/review
/validate
/ship
```
