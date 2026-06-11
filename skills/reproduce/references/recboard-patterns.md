# RecBoard Patterns

Use the closest RecBoard baseline as the primary template. The generic patterns below are fallback structure, not a replacement for local examples.

## Contents

- [RecBoard Patterns](#recboard-patterns)
  - [Contents](#contents)
  - [Directory](#directory)
  - [main.py Shape](#mainpy-shape)
  - [Config](#config)
  - [README](#readme)
  - [Local Pattern Extraction](#local-pattern-extraction)

## Directory

```text
[ModelName]/
├── main.py
├── configs/
│   └── [dataset].yaml
├── README.md
├── modules.py        # optional, for substantial model components
├── utils.py          # optional, for small helpers or adapters
└── other files       # only when required by the method
```

Keep optional files only when they carry real method logic. Avoid copying source-framework scaffolding.

## main.py Shape

Replace placeholder text such as `<...>` with model-specific content. Do not copy placeholder text into the migrated code.

```python
from typing import Dict

import freerec
import torch
import torch.nn as nn

freerec.declare(version="1.0.1")

cfg = freerec.parser.Parser()
cfg.add_argument("--embedding-dim", type=int, default=64)
cfg.set_defaults(
    description="ModelName",
    root="../../data",
    dataset="DatasetName",
    epochs=300,
    batch_size=512,
    optimizer="adam",
    lr=1e-3,
    weight_decay=0.0,
    seed=1,
)
cfg.compile()


class ModelName(freerec.models.SeqRecArch):
    r"""<short model responsibility and data flow>

    Add a short top-to-bottom workflow only when the model logic is complex.
    """

    def __init__(self, dataset: freerec.data.datasets.RecDataSet) -> None:
        super().__init__(dataset)
        ...

    def reset_parameters(self) -> None:
        # initialize key modules
        ...

    def sure_trainpipe(self, batch_size: int):
        return (...)

    def fit(
        self, data: Dict[freerec.data.fields.Field, torch.Tensor]
    ) -> Dict[str, torch.Tensor]:
        # return {"loss_name": loss}
        ...

    def recommend_from_full(self, data: Dict[freerec.data.fields.Field, torch.Tensor]):
        ...

    def recommend_from_pool(self, data: Dict[freerec.data.fields.Field, torch.Tensor]):
        ...


class CoachForModelName(freerec.launcher.Coach):

    def set_other(self) -> None:
        # optional hook called before coach.fit
        ...

    def train_per_epoch(self, epoch: int):
        ...


def main() -> None:
    try:
        dataset = getattr(freerec.data.datasets, cfg.dataset)(root=cfg.root)
    except AttributeError:
        dataset = freerec.data.datasets.RecDataSet(
            cfg.root, cfg.dataset, tasktag=cfg.tasktag
        )

    model = ModelName(dataset)
    trainpipe = model.sure_trainpipe(cfg.batch_size)
    validpipe = model.sure_validpipe(cfg.ranking)
    testpipe = model.sure_testpipe(cfg.ranking)

    coach = CoachForModelName(
        dataset=dataset,
        trainpipe=trainpipe,
        validpipe=validpipe,
        testpipe=testpipe,
        model=model,
        cfg=cfg,
    )
    coach.fit()


if __name__ == "__main__":
    main()
```

Adapt the architecture base class, datapipe, loss dict, coach hooks, and ranking methods to the closest RecBoard baseline.

## Config

```yaml
# Data
root: ../../data
dataset: DatasetName
tasktag: NEXTITEM

# Model
embedding_dim: 64

# Training
epochs: 300
batch_size: 512
optimizer: adam
lr: 1.e-3
weight_decay: 0.

# Evaluation
monitors: [LOSS, HitRate@10, NDCG@10]
which4best: NDCG@10
```

Every config field should be used by code or freerec. Do not keep unused source-repo options.

## README

```markdown
# ModelName

[[official-code](...)] [[paper](...)]

## Usage

    python main.py --config=configs/[dataset].yaml --ranking=full
    python main.py --config=configs/[dataset].yaml --ranking=pool

## Hyperparameters

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| --embedding-dim | int | 64 | Embedding dimension |

## Configuration Example

[paste a representative config]
```

## Local Pattern Extraction

When a close baseline is provided, inspect its `main.py`, `configs/`, and `README.md` first. Match its:

- Architecture base class and field names.
- Train, valid, and test datapipes.
- Coach methods and optimizer setup.
- Full/pool ranking output shapes.
- Config grouping, metric names, and README style.
