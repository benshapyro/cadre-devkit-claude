---
description: Deep research on a topic with parallel sub-agents
argument-hint: [topic or question]
---

# Research Command

Orchestrate comprehensive research using multiple parallel sub-agents.

## Validation

If no topic provided, ask for one.

## Research Flow

### 1. Analyze Request

Before proposing a research plan:
- Understand the user's question/topic
- Consider the project context (CLAUDE.md, tech stack, existing patterns)
- Review conversation history for relevant context
- Identify knowledge gaps that need filling

### 2. Propose Research Plan

Suggest a tailored research plan. Dynamically determine which research agents are needed:

**Possible Research Dimensions:**

| Dimension | When to Include |
|-----------|-----------------|
| **Codebase - Existing Patterns** | Feature touches existing code |
| **Codebase - Architecture** | Architectural decision needed |
| **Codebase - Frontend** | UI/UX or frontend changes |
| **Codebase - Backend** | API/database/server changes |
| **Codebase - Infrastructure** | DevOps, deployment, CI/CD |
| **Documentation - Framework** | Using framework features |
| **Documentation - Libraries** | Using external libraries |
| **Documentation - APIs** | Integrating external services |
| **Community - Best Practices** | Common patterns and anti-patterns |
| **Community - Recent Changes** | Library updates, deprecations |

**Output Format:**
```
## Research Plan: [topic]

Based on your question and this project's context, I recommend:

### Proposed Research Agents (N)

1. **[Category] [Specific Focus]**
   - What: [What this agent will investigate]
   - Why: [Why this is relevant to your question]

2. **[Category] [Specific Focus]**
   - What: [description]
   - Why: [relevance]

[...more as needed...]

### Questions Before Proceeding

- [Any clarifying question if the request is ambiguous]

---
Proceed with this plan? (yes / adjust / add more / cancel)
```

### 3. Await Approval

Wait for user to:
- **Approve** ("yes", "proceed", "looks good")
- **Adjust** ("skip the community one", "also check X")
- **Add** ("also research Y")
- **Cancel** ("nevermind")

### 4. Execute Research

Once approved, spawn agents using the Task tool:

```
For EACH approved research dimension:
  - Use Task tool with appropriate subagent_type
  - Prompt should specify exactly what to find
  - Request structured findings in return
```

**Subagent mapping:**
- Codebase searches → `subagent_type: "Explore"`
- Documentation → `subagent_type: "documentation-researcher"`
- Community/best practices → `subagent_type: "documentation-researcher"` with web search

**IMPORTANT:** Spawn all agents in a SINGLE message with multiple Task tool calls for parallel execution.

### 5. Synthesize Findings

After all agents return:

**Output Format:**
```
## Research Findings: [topic]

### Summary
[2-3 sentence executive summary]

### Key Discoveries

#### From Codebase
- [Finding 1 with file:line references]
- [Finding 2]

#### From Documentation
- [Finding 1 with source links]
- [Finding 2]

#### From Community
- [Best practice or pattern]
- [Common pitfall to avoid]

### Recommendations
1. [Actionable recommendation]
2. [Another recommendation]

### Next Steps
- [ ] [Suggested action]
- [ ] [Another action]

---
Save these findings? (`/progress` to create knowledge document)
```

## Example

**User:** `/research "how should we implement caching"`

**Claude Response:**
```
## Research Plan: Implementing Caching

Based on your Next.js + PostgreSQL project, I recommend:

### Proposed Research Agents (4)

1. **Codebase - Existing Patterns**
   - What: Search for any existing caching (Redis, in-memory, HTTP cache headers)
   - Why: Avoid duplicating or conflicting with existing caching

2. **Codebase - Data Access Layer**
   - What: Understand current database queries and ORM patterns
   - Why: Identify cache invalidation points

3. **Documentation - Next.js Caching**
   - What: Next.js 14 caching strategies (ISR, Route Handlers, fetch cache)
   - Why: Use framework-native caching before adding external solutions

4. **Community - Best Practices**
   - What: Redis vs in-memory vs CDN caching patterns for your stack
   - Why: Learn from others' mistakes and successes

---
Proceed with this plan?
```

## Notes

- Prefer fewer, more focused agents over many broad ones
- 3-5 agents is typical; more than 7 is probably too broad
- Each agent should have a clear, specific mission
- Always synthesize findings - don't just dump raw results
