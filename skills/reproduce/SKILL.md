---
name: reproduce
description: Use this skill when migrating external recommender-system baselines into RecBoard/freerec or reviewing an existing RecBoard migration for semantic correctness, cleanliness, runnable configuration, source-code fidelity, and valid full/pool ranking behavior.
---

# Reproduce

Use this skill for RecBoard baseline migration and migration review.

## Required Context

Before implementation or review, identify:

- Source repository or key source files.
- Target model name and target RecBoard directory.
- Closest RecBoard baseline to use as the local pattern.

If the closest RecBoard baseline is missing, ask for one. If the user cannot provide one, inspect RecBoard and state which baseline is closest and why.

## Routing

- New migration: read `references/migration.md` and `references/recboard-patterns.md`.
- Migration review: read `references/review.md`; also read `references/recboard-patterns.md` when checking local structure.
- RecBoard templates or local conventions: read `references/recboard-patterns.md`.

## Ground Rules

- Use `format-code-style` when writing, editing, or reviewing code.
- Analyze the source implementation before writing RecBoard code.
- Preserve method semantics, not source-file shape.
- Remove unrelated framework branches, dead code, and task variants that the target migration will not execute.
- Do not claim semantic correctness without source implementation access.
- Finish with explicit verification results and any unverified items.
