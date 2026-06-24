---
name: eval
description: Use this skill when the user invokes /eval or wants to design validation before or during implementation.
---

# Eval

Use this skill to write `validation.md`, explaining how to prove the implementation is correct.

## Prerequisites

Requires `plan.md`; use `spec.md` when available. If `plan.md` is missing, ask whether to run `/refine` first unless the user explicitly wants a standalone validation checklist.

## Scope

Translate acceptance criteria and implementation risks into validation methods. Do not implement the feature or split execution tasks.

## Output

Write or update `validation.md` after the user confirms the validation design.

Use this structure:

```md
# Validation

## Scope

## Acceptance Checks

## Test Cases

## Edge Cases

## Failure Cases

## Manual Checks

## Open Questions
```

## Rules

- Map `Acceptance Checks` to `spec.md` acceptance criteria when available.
- Use `Test Cases` for checks that can be automated.
- Use `Manual Checks` for important behavior that is not suitable for automation.
- Cover edge cases, failure cases, compatibility constraints, and regression risks when relevant.
- Do not weaken, remove, or bypass accepted validation criteria for implementation convenience.
- If acceptance criteria are not verifiable, record the issue under `Open Questions` and return to `/align` when needed.
- If the implementation plan is not verifiable, record the issue under `Open Questions` and return to `/refine` when needed.
