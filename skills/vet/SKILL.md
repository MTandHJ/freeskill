---
name: vet
description: Use this skill when the user invokes /vet or wants an independent review of a workflow artifact before moving to the next phase.
---

# Vet

Use this skill to review a workflow artifact and write `vet.md`.

## Prerequisites

None. Review the stage or files named by the user. If no target is named, infer the latest relevant artifact among `spec.md`, `plan.md`, `validation.md`, and `task.md`.

## Scope

Review the target artifact for completeness, consistency, phase boundaries, and readiness for the next step. Do not modify the target artifact.

## Output

Prefer using a subagent for the review. If subagents are unavailable, perform the review directly and mention that fallback.

Write or update `vet.md` with this structure:

```md
# Vet

## Target

- Stage:
- Files reviewed:

## Verdict

- Status: Pass | Revise
- Return to: none | align | refine | eval | todo

## Findings

## Required Fixes

## Suggestions
```

## Rules

- Subagents, when used, should review only and should not modify files.
- Judge whether the artifact is clear, complete, internally consistent, and ready for the next phase.
- Check that `spec.md` states what should be built and how completion is judged.
- Check that `plan.md` states how to build it without turning into TODOs or validation design.
- Check that `validation.md` explains how to prove correctness without weakening accepted criteria.
- Check that `task.md` is executable and grounded in the previous artifacts.
- If `Required Fixes` is non-empty, set `Status: Revise` and name the phase to return to.
- Put non-blocking improvements under `Suggestions`.
