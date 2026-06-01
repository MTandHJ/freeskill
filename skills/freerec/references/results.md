# Results

## `results.json`

Path:

```text
logs/[ExperimentName]/core/results.json
```

Typical structure:

```json
{
  "description": "ExperimentName",
  "dataset": "DatasetName",
  "config": {
    "which4best": "NDCG@10"
  },
  "runs": [
    {
      "id": "MMDDHHMMSS",
      "params": {"lr": 0.001},
      "metrics": {
        "valid": {"NDCG@10": 0.39},
        "best": {"NDCG@10": 0.44},
        "test": {"NDCG@10": 0.38}
      }
    }
  ]
}
```

Fields:

- `config.which4best`: metric used for sorting tune results.
- `runs[].id`: run id, usually `MMDDHHMMSS`.
- `runs[].params`: hyperparameters for this run.
- `runs[].metrics.valid`: validation metrics.
- `runs[].metrics.best`: best-checkpoint metrics.
- `runs[].metrics.test`: last-epoch test metrics, when present.

Read with:

```bash
python skills/freerec/scripts/summarize_tune_results.py logs/[ExperimentName]/core/results.json
```

## `best.pkl`

Path:

```text
logs/[ExperimentName]/[dataset]/[id]/data/best.pkl
```

Typical structure:

```python
{
    "train": {"LOSS": 0.12},
    "valid": {"NDCG@10": 0.39},
    "test": {"NDCG@10": 0.38},
    "best": {"NDCG@10": 0.44},
}
```

Read with:

```bash
python skills/freerec/scripts/read_best.py logs/[ExperimentName]/[dataset]/[id]/data/best.pkl
```