---
description: Start a new feature with proper planning
argument-hint: [feature description]
---

# Plan Command

Plan a new feature or task with proper structure before implementation.

## Validation

If no feature description provided, ask for one.

## Planning Steps

### 1. Gather Context

Before planning, understand the codebase:
- Read relevant CLAUDE.md files
- Identify existing patterns and conventions
- Understand related code and dependencies

### 2. Requirements Clarification

Ask clarifying questions if needed:
- What is the expected behavior?
- What are the edge cases?
- What are the acceptance criteria?
- Are there performance requirements?

### 3. Create Plan

Structure the implementation:

**Output Format:**
```
## Feature: [description]

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Technical Approach
1. Step 1 - [description]
2. Step 2 - [description]

### Files to Modify/Create
- `path/to/file.ts` - [changes]

### Dependencies
- [list any new dependencies]

### Testing Strategy
- Unit tests: [approach]
- Integration tests: [approach]

### Risks
- [potential issues and mitigations]

### Estimate
- Complexity: [low/medium/high]
```

### 4. Confidence Check

Run Pre-Implementation Confidence Check before proceeding.

### 5. Await Approval

Present plan and wait for user approval before implementation.

## Next Steps

After approval:
- Start implementation with `/review` for code review
- Use `/validate` to verify before completion
- Use `/ship` when ready to commit
