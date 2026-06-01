---
name: freerec
description: Use this skill when working with freerec/RecBoard recommendation experiments, including freerec make dataset construction, parameter tuning, hyperparameter search, grid search, results.json summarization, best.pkl reading, and valid/best metric interpretation.
---

# FreeRec

Use this skill to run and analyze freerec recommendation experiments from the user side.

## Capabilities

- Dataset construction: use `freerec make`; read `references/make.md`.
- Parameter tuning and hyperparameter search: use `freerec tune`; read `references/tune.md`.
- Result summarization: read `references/results.md`; use `scripts/summarize_tune_results.py` or `scripts/read_best.py`.
- Metric interpretation: read `references/results.md` for `valid`, `best`, and `test`.

## Experiment Loop

```text
prepare data -> freerec make -> configure search -> freerec tune -> summarize results -> adjust config -> interpret valid/best
```

## Common Paths

- Dataset-specific configs: `configs/[dataset].yaml`.
- Tune summary: `logs/[ExperimentName]/core/results.json`.
- Single run output: `logs/[ExperimentName]/[dataset]/[id]/`.
- Single run valid/best/test snapshot: `logs/[ExperimentName]/[dataset]/[id]/data/best.pkl`.

## Metric Roles

- `valid`: validation metrics used for hyperparameter selection.
- `best`: test metrics at the best validation checkpoint.
- `test`: last-epoch test metrics, mainly useful for debugging.

## Scripts

- `scripts/summarize_tune_results.py`: summarize `logs/[ExperimentName]/core/results.json` as Markdown.
- `scripts/read_best.py`: read a run's `data/best.pkl` and print `valid` / `best` metrics.
