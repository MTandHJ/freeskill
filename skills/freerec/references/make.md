# Make

Use `freerec make` to convert RecBole-style atomic files into freerec processed datasets with filtering, tokenization, and train/valid/test splitting.

## Usage

```bash
freerec make DATASET [OPTIONS]
```

`DATASET` is the output dataset name.

## Input Layout

```text
data/[DATASET]/
├── [DATASET].inter
├── [DATASET].user
└── [DATASET].item
```

`.inter` is required. `.user` and `.item` are optional feature files.

Default interaction columns:

- `USER`
- `ITEM`
- `RATING`
- `TIMESTAMP`

Column names can be changed with:

- `-uc, --userColname`
- `-ic, --itemColname`
- `-rc, --ratingColname`
- `-tc, --timestampColname`

## Common Options

- `--root ROOT`: data root, default `.`.
- `--filedir FILEDIR`: raw file directory; defaults to `DATASET`.
- `--splitting {ROU,RAU,ROD,LOU,DOU,DOD}`: split strategy.
- `-sp, --star4pos STAR4POS`: keep ratings `>= star4pos`, default `0`.
- `-ku, --kcore4user KCORE4USER`: minimum interactions per user, default `10`.
- `-ki, --kcore4item KCORE4ITEM`: minimum interactions per item, default `10`.
- `-rs, --ratios RATIOS`: train/valid/test ratios, default `8,1,1`.
- `--days DAYS`: days used by time-based splitting, default `7`.

## Splitting Guide

- `ROU`: ratio on each user's history; general default.
- `RAU`: ratio on user while ensuring at least one test item per user.
- `ROD`: global dataset split by ratio.
- `LOU`: leave-one-out per user; last item is test, penultimate item is valid.
- `DOU`: day-based split per user.
- `DOD`: day-based split over the whole dataset.

For sequential recommendation, `LOU` is often a natural first choice. For general matching tasks, `ROU` or `RAU` is a common starting point.

## Output Layout

```text
data/Processed/[DATASET]_[star4pos][kcore4user][kcore4item]_[splitting]/
├── train.txt
├── valid.txt
├── test.txt
├── user.txt
└── item.txt
```

The split files are TSV-like interaction files. `user.txt` and `item.txt` appear when source feature files exist.

## Example

```bash
freerec make Amazon2014Beauty \
  --root ../../data \
  --splitting LOU \
  --kcore4user 5 \
  --kcore4item 5 \
  --star4pos 0
```