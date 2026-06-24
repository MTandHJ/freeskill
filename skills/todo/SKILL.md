---
name: todo
description: Use this skill when the user invokes /todo or wants to split aligned work into executable implementation tasks.
---

# Todo

Use this skill to turn aligned work into `task.md`.

## Prerequisites

Requires at least `spec.md`. Use `plan.md` and `validation.md` when available, but do not require `/eval` for simple tasks. If `spec.md` is missing, ask whether to run `/align` first or confirm that conversation context is enough.

## Scope

Split the work into executable tasks and maintain task status during implementation. Do not redesign requirements, implementation, or validation criteria.

## Output

Write or update `task.md` after the user confirms the task breakdown.

Use this structure:

```md
# Tasks

## TODO

- [ ] 1. <task>
  - Depends on:
  - Validate:

## Blockers

## Notes
```

## Rules

- Each task should be concrete, ordered, and small enough to execute clearly.
- Preserve dependencies between tasks.
- Attach a concise validation point to each task when useful.
- Use `validation.md` when it exists, but do not duplicate the full validation plan.
- Update checkboxes as work progresses.
- If the task breakdown exposes a requirement conflict, return to `/align`.
- If it exposes an implementation conflict, return to `/refine`.
- If it exposes a validation gap, return to `/eval`.
