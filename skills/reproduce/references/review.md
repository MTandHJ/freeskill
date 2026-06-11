# Review

Use this checklist to review an existing RecBoard migration. If the source implementation is missing, request it before making semantic-correctness claims.

## Structure

- Directory contains `main.py`, `configs/`, and `README.md`.
- `modules.py`, `utils.py`, and other files are present only when needed.
- No copied source-framework scaffolding remains without purpose.

## Config

- README config example matches real config files.
- Config fields are used by code or freerec.
- Dataset, task tag, monitors, and `which4best` match the target task.
- Defaults in `main.py` do not conflict with YAML examples without reason.

## Source Semantics

Compare against the source implementation:

- Data fields, sequence construction, feature usage, and candidate sets.
- Positive/negative sampling behavior.
- Initialization of embeddings and key modules.
- Forward path and tensor shapes.
- Loss terms, reductions, weights, masks, and regularization.
- Optimizer, scheduler, and update order when method-relevant.
- Inference score definition for full and pool ranking.
- Metric meaning and best-checkpoint selection.

## RecBoard Interface

- Parser, dataset loading, model construction, datapipe construction, and coach construction are connected.
- `fit` returns loss dicts expected by the coach.
- `recommend_from_full` returns `(B, N)` scores.
- `recommend_from_pool` returns `(B, K)` scores.
- `reset_ranking_buffers` is used when full ranking benefits from cached embeddings.

## Cleanliness

- No dead branches for unused source tasks.
- No unused config fields, imports, files, or classes.
- No defensive branches that only compensate for ignored type annotations.
- Code follows `format-code-style` and local RecBoard style.

## Verification Record

Record what was run:

- Import or config parse.
- One batch or short epoch.
- Full ranking shape.
- Pool ranking shape.
- Ruff check.

Record any skipped checks with the reason.
