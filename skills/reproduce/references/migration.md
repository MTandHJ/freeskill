# Migration

Migrate by understanding the source method first, then mapping it to the closest RecBoard baseline.

## Source Analysis

Read the source repository before editing. Identify:

- Entry point, config system, and run command.
- Dataset format, raw sample fields, and batch fields.
- Positive/negative sampling and sequence/window construction.
- Model initialization, forward path, loss terms, and regularization.
- Training loop, optimizer, scheduler, gradient behavior, and logging.
- Inference path, candidate set, score definition, and metrics.

Summarize the source data flow before writing RecBoard code.

## RecBoard Mapping

Map source concepts to RecBoard/freerec:

- Config values -> `cfg.add_argument`, `cfg.set_defaults`, and `configs/[dataset].yaml`.
- Dataset and fields -> `freerec.data.datasets` and field-indexed batches.
- Training samples -> `sure_trainpipe`.
- Validation/test samples -> `sure_validpipe` and `sure_testpipe`.
- Model logic -> RecBoard model class, optional `modules.py`, optional `utils.py`.
- Training step -> `CoachForModel.train_per_epoch`.
- Full ranking -> score matrix over all candidate items.
- Pool ranking -> score matrix over provided unseen/candidate items.

Use the closest RecBoard baseline to choose the exact datapipe and architecture pattern.

## Clean Migration

Preserve method semantics, not the original framework shape.

Keep:

- Branches required by the target method and target task.
- Initialization, sampling, loss, masking, scoring, and metric semantics.
- Helper modules that carry real method logic.

Remove:

- Source-framework registries, trainer abstractions, and CLI layers that RecBoard replaces.
- Dataset branches, tasks, or modes not used by the target migration.
- Dead code, unused config fields, and unused copied files.

## Implementation Order

1. Create target directory and required files.
2. Port model components and helpers.
3. Implement `main.py` around RecBoard parser, dataset, model, datapipe, and coach.
4. Write one representative config.
5. Write README with source links, usage, hyperparameters, and config example.
6. Verify import/config, one minimal training step, ranking output shape, and Ruff.

## Verification Notes

Do not replace semantic checks with "it runs". If data or runtime is unavailable, report which checks were not run and why.
