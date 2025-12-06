---
description: Discover and specify a new software project from scratch
argument-hint: [project idea or problem]
---

# Greenfield Command

Transform a new idea into actionable specifications through structured discovery.

**Before starting:** Read `.claude/skills/product-discovery/SKILL.md` for methodology and templates.

## When to Use

- Starting a new project from scratch
- Exploring a vague idea that needs definition
- Defining MVP scope before implementation

**Not for:** Adding features to existing projects (use `/plan` instead)

## Output

Creates three documents in `docs/`:
- `docs/SPEC.md` - What to build (requirements, users, success criteria)
- `docs/DESIGN.md` - How to build it (architecture, technology choices)
- `docs/PLAN.md` - Implementation roadmap (phases, tasks, go/no-go)

## Discovery Process

### Phase 1: Vision (2-3 questions)
Understand the core idea and motivation.
- What problem are you solving?
- Who has this problem?
- What does success look like?

### Phase 2: Core Problem (2-3 questions)
Identify the essential problem to solve first.
- What's the ONE thing that must work?
- What's the smallest valuable solution?

### Phase 3: Users (2-3 questions)
Define specific user types and their needs.
- Who is the primary user?
- What triggers their need?

### Phase 4: Technical (2-3 questions)
Explore constraints and technology options.
- What can be simplified for MVP?
- What existing tools can be leveraged?

### Phase 5: Validation (2-3 questions)
Define success metrics and failure conditions.
- How will you know it's working?
- What would make you pivot?

### Phase 6: Scoping
Define MVP boundaries using effort-based framing:

| Scope | Definition |
|-------|------------|
| **Core MVP** | ONE problem, ONE user type |
| **Expanded MVP** | Multiple features, single user focus |
| **Full Vision** | All features, all users |

## Workflow

```
1. User provides idea/problem
2. Interactive discovery (phases 1-6)
3. After each phase: Update relevant doc sections
4. Review complete specs with user
5. Finalize and save to docs/
6. Suggest next step: /plan [first feature]
```

## Key Behaviors

**Ask, don't assume:**
- Probe deeper with "Why?" and "Can you give an example?"
- Challenge scope with "If you could only have one..."
- Clarify vague terms with "What does X specifically mean?"

**Progressive documentation:**
- Update SPEC.md as requirements emerge
- Update DESIGN.md as technical decisions are made
- Update PLAN.md as scope crystallizes

**Scope control:**
- Default to smallest viable scope
- Move "nice to haves" to Full Vision section
- Resist feature creep with "Let's validate the core first"

## Example Session

```
User: /greenfield I want to build a tool that helps developers track their learning progress

Claude: Great idea! Let's explore this together and create specifications.

**Phase 1: Vision**

What moment made you think "someone should build this"? What were you trying to do when you had this idea?

[... interactive discovery continues ...]

After exploring your idea, I've created three documents:

- `docs/SPEC.md` - Your learning tracker specification
- `docs/DESIGN.md` - Technical architecture decisions
- `docs/PLAN.md` - Implementation roadmap

**MVP Scope:** Personal progress dashboard with manual entry
**Full Vision:** Social features, spaced repetition, integrations

Ready to start building? Run:
`/plan Implement basic progress tracking with manual entry`
```

## Completion

After discovery is complete:

1. Present summary of all three docs
2. Highlight MVP scope vs full vision
3. Suggest first feature for `/plan`

**Next Steps:**
- `/plan [first MVP feature]` - Start implementation
- `/research [technical topic]` - Deep dive on unknowns
