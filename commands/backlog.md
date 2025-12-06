---
description: Document bugs and improvements to project backlog (interactive loop)
argument-hint: [optional: bug|enh|ux] [optional: brief description]
allowed-tools: Read, Grep, Glob, Task, Write, Edit, mcp__sequential-thinking__sequentialthinking, mcp__exa__exa_search, mcp__Ref__ref_search_documentation, mcp__Ref__ref_read_url, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_click, mcp__playwright__browser_close
---

# Backlog Mode

You are in **Backlog Mode** - documenting bugs and improvements WITHOUT implementing them.

**Reference skills based on issue domain:**
- API issues: Read `.claude/skills/api-design-patterns/SKILL.md`
- Frontend components: Read `.claude/skills/react-patterns/SKILL.md`
- Error handling: Read `.claude/skills/error-handler/SKILL.md`
- UX improvements: Read `.claude/skills/frontend-design/SKILL.md`

## Available Tools & When to Use Them

### Codebase Exploration
Use **Task tool with Explore subagent** for:
- Finding root causes of bugs
- Understanding current implementation
- Locating affected files and components
```
Task(subagent_type="Explore", prompt="Very thorough: find all code related to [X]")
```

### External Research
Use **Exa search** (`mcp__exa__exa_search`) for:
- Checking if others encountered the same bug
- Finding known fixes or workarounds
- Researching UI/UX best practices for similar features
```
mcp__exa__exa_search(query="[framework] [issue description] fix")
```

Use **Ref documentation** (`mcp__Ref__*`) for:
- Checking official framework/library docs
- Verifying correct API usage
- Finding recommended patterns
```
mcp__Ref__ref_search_documentation(query="[library] [feature] documentation")
```

### UI/UX Verification
Use **Playwright** (`mcp__playwright__*`) for UX issues:
- Navigate to the affected page
- Take screenshot of current state (for BACKLOG entry)
- Verify the issue exists as user described
- Document "before" state
```
mcp__playwright__browser_navigate(url="http://localhost:3000/path")
mcp__playwright__browser_take_screenshot(filename="backlog-ux-xxx-before.png")
```

### Complex Analysis
Use **Sequential thinking** (`mcp__sequential-thinking__sequentialthinking`) for:
- Multi-step root cause analysis
- Weighing multiple potential causes
- Structuring complex investigations

---

## Parallel Execution Strategy

You CAN run multiple subagents AND tools in parallel by making multiple tool calls in a single message. Use this for efficiency when tasks are **independent**.

### Multiple Subagents in Parallel

**When to use:**
- Bug/feature spans frontend + backend (separate concerns)
- Investigation touches multiple packages
- Need both code exploration AND documentation research
- Complex issue benefits from divide-and-conquer

**Example - Bug spanning layers:**
```
[Single message, multiple Task calls - all run simultaneously:]

Task(subagent_type="Explore", prompt="Very thorough: find tRPC handlers for [feature]")
Task(subagent_type="Explore", prompt="Very thorough: find React components rendering [feature]")
Task(subagent_type="documentation-researcher", prompt="Research [framework] best practices for [pattern]")
```

**Example - Multi-package investigation:**
```
Task(subagent_type="Explore", prompt="Search packages/trpc for [issue]")
Task(subagent_type="Explore", prompt="Search packages/features for [issue]")
Task(subagent_type="Explore", prompt="Search apps/web for [issue]")
```

### Subagents + Tools in Parallel

**Example - UX issue (all at once):**
```
Task(subagent_type="Explore", prompt="Find component code for [element]")
mcp__playwright__browser_navigate(url="http://localhost:3000/path")
mcp__exa__exa_search(query="UX best practices [pattern]")
```

### When to Stay Sequential

- Results from first search inform what to search next
- Need to confirm issue exists before deep diving
- Small codebase where one Explore is sufficient
- Risk of overlapping/duplicated search areas

**Example - Sequential dependency:**
```
1. First: Explore → discovers it's a Prisma schema issue
2. Then: Ref search → "Prisma relations documentation"
   (wouldn't know to search Prisma without step 1)
```

### Rule of Thumb
| Situation | Approach |
|-----------|----------|
| Know what to search for | **Parallel** - maximize speed |
| Need to discover what to search | **Sequential** - learn first |
| Large codebase, clear separation | **Parallel subagents** - divide and conquer |
| Small codebase or focused issue | **Single subagent** - avoid overhead |

---

## Initial Setup

1. **Check for arguments**: If user passed `$ARGUMENTS`, use it as the first item description
2. **Locate BACKLOG.md** by searching:
   - `docs/*/BACKLOG.md`
   - `docs/BACKLOG.md`
   - `BACKLOG.md`
3. **If not found**: Create `docs/BACKLOG.md` with this template:
   ```markdown
   # Project Backlog

   Issues and improvements tracked for this project.

   ---

   ## Bugs

   (No bugs reported yet)

   ---

   ## Enhancements

   (No enhancements reported yet)

   ---

   ## UX Improvements

   (No UX improvements reported yet)

   ---

   ## Completed

   Items moved here after being fixed/implemented.

   ---

   ## Statistics
   - **Total Open**: 0
   - **Bugs**: 0
   - **Enhancements**: 0
   - **UX**: 0
   - **Last Updated**: YYYY-MM-DD
   ```

---

## Workflow Loop

For each item, execute these steps IN ORDER:

### Step 1: Receive
- Accept ONE item at a time
- If user provides multiple, say: "Let's start with the first one. What is it?"
- If `$ARGUMENTS` provided, use that as the item

### Step 2: Classify
Determine type based on description:
| Type | Criteria |
|------|----------|
| **BUG** | Something broken, error, unexpected behavior |
| **ENH** | New feature, capability, or functional improvement |
| **UX** | Visual, usability, or interface improvement |

State your classification: "This sounds like a **[TYPE]**."

### Step 3: Check Duplicates
- Read BACKLOG.md
- Search for similar existing entries
- If potential duplicate found: "This might be related to [ID]. Is this the same issue or different?"

### Step 4: Investigate (Use Appropriate Tools)

**For ALL types:**
- Use **Explore subagent** to find relevant code

**For BUGs additionally:**
- Use **Exa** to search if others hit this issue
- Check for known fixes or workarounds

**For ENH additionally:**
- Use **Ref** to check official docs for best practices
- Use **Exa** to research how others implement similar features

**For UX additionally:**
- Use **Playwright** to navigate to the page and take a screenshot
- Verify the issue exists as described
- Save screenshot as `backlog-ux-XXX-current.png` for documentation

### Step 5: Analyze
Use sequential thinking if complex. Summarize:
- What you found in codebase
- What external research revealed (if any)
- Root cause (BUG) or approach (ENH/UX)
- All affected files with full paths
- Suggested priority (P1/P2/P3)

### Step 6: Preview Entry
Show the complete BACKLOG entry to user:
```
Here's the proposed entry:

### [TYPE-XXX] Title
- **Reported**: date
- **Status**: Open
...

Does this look accurate? Any changes?
```

### Step 7: Document
After user confirms (or says "looks good", "yes", "ok"):
- Add entry to appropriate section in BACKLOG.md
- Update Statistics section
- Confirm: "Added as **[TYPE-XXX]** to BACKLOG.md"

### Step 8: Next Item
Ask: "Next item? (or 'done' to exit backlog mode)"
- If user provides another item → Go to Step 1
- If user says "done", "exit", "that's all" → End with summary of items added

---

## Critical Rules

1. **NO IMPLEMENTATION** - Only analyze and document
2. **NO CODE CHANGES** - Only read/explore, write only to BACKLOG.md
3. **ALWAYS PREVIEW** - Never add without user confirmation
4. **ONE AT A TIME** - Don't batch multiple items
5. **USE SUBAGENTS** - For thorough codebase exploration
6. **RESEARCH WHEN RELEVANT** - Use Exa/Ref for external context
7. **SCREENSHOT UX ISSUES** - Visual documentation helps
8. **INCREMENT IDs** - Check highest existing ID, add 1

---

## Priority Guidelines

| Priority | Use When |
|----------|----------|
| **P1 (Critical)** | Blocks core functionality, security risk, data loss, affects all users |
| **P2 (Medium)** | Significant but has workaround, important feature request |
| **P3 (Low)** | Minor issue, cosmetic, nice-to-have |

---

## Templates

### BUG-XXX
```markdown
### [BUG-XXX] Title
- **Reported**: YYYY-MM-DD
- **Status**: Open
- **Priority**: P1/P2/P3
- **Description**: What's broken
- **Steps to Reproduce**:
  1. First step
  2. Second step
- **Expected**: What should happen
- **Actual**: What happens instead
- **Root Cause Analysis**:
  - Finding from exploration
  - Why this occurs
- **External Research**: (if relevant - similar issues found, known fixes)
- **Affected Files**:
  - `path/to/file.ts:lineNum` - description
- **Proposed Fix**: High-level approach (NOT code)
```

### ENH-XXX
```markdown
### [ENH-XXX] Title
- **Reported**: YYYY-MM-DD
- **Status**: Open
- **Priority**: P1/P2/P3
- **Description**: What to add/improve
- **User Impact**: Who benefits, how
- **Current State**: How it works now
- **Proposed Solution**: High-level approach
- **Best Practices**: (from docs/research if relevant)
- **Scope**: Small (hours) / Medium (day) / Large (days+)
- **Affected Files**:
  - `path/to/file.ts` - what changes needed
- **Dependencies**: Blockers or prerequisites
```

### UX-XXX
```markdown
### [UX-XXX] Title
- **Reported**: YYYY-MM-DD
- **Status**: Open
- **Priority**: P1/P2/P3
- **Description**: UX issue or improvement
- **Current Behavior**: How it looks/works now
- **Proposed Behavior**: How it should look/work
- **Screenshot**: `.playwright-mcp/backlog-ux-XXX-current.png` (if captured)
- **UX Best Practices**: (from research if relevant)
- **Affected Components**:
  - `path/to/Component.tsx` - changes needed
- **Implementation Notes**: Technical considerations
```

---

## On Exit

When user says "done", provide summary:
```
Backlog session complete. Added X items:
- BUG-XXX: title
- ENH-XXX: title
- UX-XXX: title

Run /backlog again to add more items.
```

Close any open Playwright browser: `mcp__playwright__browser_close`

---

**Backlog mode active.** Describe a bug or improvement to document.
