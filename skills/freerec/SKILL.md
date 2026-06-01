---
name: freerec
description: Use this skill when working with freerec/RecBoard recommendation experiments, including freerec make dataset construction, freerec tune config generation, grid search, results.json summarization, best.pkl reading, and valid/best metric reporting.
---

# FreeRec

Use this skill to run and analyze freerec recommendation experiments from the user side.

## Workflow

1. Identify the task and read the matching reference before acting.
2. Use `freerec` CLI commands for freerec operations.
3. Use bundled scripts for tune config creation and result parsing.
4. Report `valid` as the tuning signal and `best` as the final metric.

## Experiment Loop

```text
prepare data -> freerec make -> create tune config -> freerec tune -> summarize results -> adjust config -> report valid/best
```

## Task Routing

- Dataset construction with `freerec make`: read `references/make.md`.
- Tune YAML and `freerec tune`: read `references/tune.md`.
- Tune `results.json` summaries: read `references/results.md`.

## Common Paths

- Base configs: `configs/[dataset].yaml`.
- Tune summary: `logs/[ExperimentName]/core/results.json`.
- Single run output: `logs/[ExperimentName]/[dataset]/[id]/`.
- Single run best snapshot: `logs/[ExperimentName]/[dataset]/[id]/data/best.pkl`.

## Reporting Rule

- `valid`: validation metric used to choose hyperparameters.
- `best`: test metrics at the best validation checkpoint; use this for final reporting.
- `test`: if present, usually last-epoch test metrics; use mainly for debugging.

## Scripts

- `scripts/create_tune_config.py`: create a freerec tune YAML from `assets/template.yaml`.
- `scripts/summarize_tune_results.py`: summarize `logs/[ExperimentName]/core/results.json` as Markdown.
- `scripts/read_best.py`: read a run's `data/best.pkl` and print `valid` / `best` metrics.
