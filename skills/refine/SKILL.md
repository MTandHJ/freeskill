---
name: refine
description: Use this skill when the user invokes /refine or wants to refine implementation details after requirements are aligned.
---

# Refine

Use this skill to turn `spec.md` into a mature implementation plan in `plan.md`.

## Prerequisites

Requires `spec.md`. If `spec.md` is missing, ask whether to run `/align` first or reconstruct the requirements from conversation context and clearly mention the gap.

## Scope

Discuss implementation details, settle the final approach, and record only the confirmed plan. Do not preserve rejected alternatives in `plan.md`.

## Output

Write or update `plan.md` after the user confirms the refined implementation direction.

Use this structure:

```md
# Plan

## Overview

## Implementation

## Behavior

## Compatibility

## Notes
```

## Rules

- Preserve the goals, non-goals, constraints, and acceptance criteria from `spec.md`.
- Do not duplicate `spec.md`; summarize only what is needed to understand the implementation plan.
- Discuss alternatives with the user when useful, but write only the final agreed approach.
- Cover implementation structure, important files, interfaces, data shape, user-visible behavior, and compatibility concerns when relevant.
- Keep validation design for `/eval` and task sequencing for `/todo`.
- If a requirement conflict appears, pause and return to `/align`.
