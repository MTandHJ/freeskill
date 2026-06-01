# Tune

Use `freerec tune` for grid search over hyperparameters. Each grid combination runs as an independent process.

## Usage

```bash
freerec tune ExperimentName tune.yaml
```

## tune.yaml

```yaml
command: python main.py
envs:
  root: ../../data
  dataset: Amazon2014Beauty_550_LOU
  device: "0,0,1,1"
params:
  lr: [1.e-4, 5.e-4, 1.e-3]
  batch_size: [256, 512]
defaults:
  config: configs/Amazon2014Beauty_550_LOU.yaml
  optimizer: adam
  epochs: 100
```

## Field Boundaries

- `command`: training command for one trial.
- `envs`: environment-level values passed to each trial, such as root, dataset, and device.
- `params`: grid search dimensions. freerec runs the Cartesian product.
- `defaults`: fixed arguments shared by all trials.

## Device

`envs.device` is a comma-separated assignment list. Each entry represents one concurrent trial slot, not multi-GPU training for a single trial.

Examples:

- `device: "0"`: one trial on GPU 0.
- `device: "0,1"`: two concurrent slots, one on GPU 0 and one on GPU 1.
- `device: "0,0,1,1"`: four concurrent slots, two on each GPU.
- `device: cpu`: CPU fallback.

When using `scripts/create_tune_config.py`, `device: auto` in `assets/template.yaml` is resolved to a concrete device string unless `--device` is explicitly passed.

## Config Creation

```bash
python skills/freerec/scripts/create_tune_config.py \
  --output tune.yaml \
  --dataset Amazon2014Beauty_550_LOU \
  --config configs/Amazon2014Beauty_550_LOU.yaml \
  --param "lr=[1.e-4, 5.e-4, 1.e-3]" \
  --param "batch_size=[256, 512]" \
  --default "epochs=100"
```

Pass `--device "0,1"` to override automatic device assignment. Pass `--force` only when overwriting an existing output is intended.

## freerec tune Output

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