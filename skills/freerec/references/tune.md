# Tune

`freerec tune` runs grid search. Each parameter combination is one independent trial.

## Command

```bash
freerec tune ExperimentName ConfigFile
```

## ConfigFile

```yaml
command: python main.py # one-trial command
envs:
  root: ../../data # dataset root
  dataset: Amazon2014Beauty_550_LOU
  device: "0,0,1,1,2,2" # concurrent trial slots
params: # search space; Cartesian product
  lr: [1.e-4, 5.e-4, 1.e-3]
  batch_size: [256, 512]
defaults: # optional fixed arguments; does not expand trial count
  config: configs/Amazon2014Beauty_550_LOU.yaml
  early_stop_patience: 3
```

`device: "0,0,1,1,2,2"` means six concurrent trial slots: two on GPU 0, two on GPU 1, and two on GPU 2. Repeated GPU IDs indicate that multiple independent trials would be assigned to the same GPU.

**Goal:** maximize end-to-end tuning throughput. Keep all GPUs busy; use multiple trials per GPU when one trial is lightweight.

Recommended steps:

1. Check visible GPUs and load.

```bash
if [ -n "${CUDA_VISIBLE_DEVICES:-}" ]; then
  printf '%s\n' "$CUDA_VISIBLE_DEVICES" | awk -F',' '{print NF}'
else
  nvidia-smi --query-gpu=index --format=csv,noheader,nounits | wc -l
fi
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv
```

2. Estimate one trial's GPU load.
3. Choose a balanced string: `"0,1,2,3"` for one slot per GPU, `"0,0,1,1,2,2,3,3"` for two slots per GPU.

## `freerec tune` Output

```text
logs/[ExperimentName]/
├── core/
│   ├── log.txt              # Coordinator log
│   ├── config.json          # Tune config snapshot
│   └── results.json         # Aggregated results
└── [dataset]/[id]/          # id = MMDDHHMMSS, one per hyperparam combo
    ├── config.json, log.txt, model.pt, best.pt
    ├── summary/{SUMMARY.md,*.png}
    └── data/{monitors.pkl, best.pkl}
```

## Tuning Summary

For multi-round tuning, maintain one project-level summary:

```text
tuning/[TaskName].md
```

Use a task name that identifies the model, dataset, or goal. Update the summary before and after each round:

```md
# [TaskName]

## Goal

- Dataset:
- Model:
- Target metric:
- Base config:
- Experiments:

## Search Process

### Round 1: [ExperimentName]

- Search space:
- Rationale:
- Result:

| Rank | Params | Valid | Best | Notes |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

- Finding:


### Round 2: [ExperimentName]

...

## Final Choice

| Field | Value |
| --- | --- |
| Best params |  |
| Best valid |  |
| Final best |  |

- Recommended config:

## Findings

- Sensitive parameters:
- Failed or ignored settings:
- Resource notes:
- Next tuning direction:
```

Prefer tables for comparable results, especially top runs and final choices. `Result` must come from `results.json`. Use `valid` to explain tuning decisions and `best` for final metric reporting.
