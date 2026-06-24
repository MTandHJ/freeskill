---
name: align
description: Use this skill when the user invokes /align or wants to align requirements before implementation planning.
---

# Align

Use this skill to align requirements and write `spec.md`.

## Prerequisites

None. Start from the user's request and available conversation context.

## Scope

Clarify what should be built, why it matters, and how completion will be judged. Do not design the implementation, validation plan, or task list.

## Workflow

1. Read the user's request and identify missing or ambiguous requirement-level information.
2. Actively ask targeted clarification questions before drafting when missing details affect scope, constraints, acceptance criteria, or user scenarios.
3. After the requirement gaps are resolved or explicitly accepted as assumptions, summarize the aligned requirements.
4. Write or update `spec.md` only after the user confirms the aligned requirements.

## Output

Write or update `spec.md` after the user confirms the aligned requirements.

Use this structure:

```md
# Spec

## Goal

## Scope

## Non-goals

## User Scenarios

## Inputs / Outputs

## Constraints

## Acceptance Criteria

## Assumptions

## Open Questions
```

## Rules

- Cover goals, scope, non-goals, user scenarios, inputs and outputs, constraints, acceptance criteria, assumptions, and open questions.
- Prefer asking about uncertain requirements before drafting `spec.md`.
- If a missing detail changes scope or acceptance, ask before treating it as an assumption.
- Keep implementation details out of `spec.md`; leave them for `/refine`.
- Keep validation methods out of `spec.md`; leave them for `/eval`.
- Keep task sequencing out of `spec.md`; leave it for `/todo`.
- If a detail is unknown but not blocking, record it under `Open Questions`.
- Do not proceed to implementation planning or implementation unless the user asks.
