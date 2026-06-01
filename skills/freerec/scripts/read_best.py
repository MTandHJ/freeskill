#!/usr/bin/env python
r"""Read a freerec run's `best.pkl` and print valid/best metrics."""

from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


def load_best(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"best.pkl file does not exist: {path}")

    try:
        from freerec.utils import import_pickle
    except Exception:
        with path.open("rb") as file:
            data = pickle.load(file)
    else:
        data = import_pickle(str(path))

    if not isinstance(data, dict):
        raise ValueError("best.pkl must contain a mapping")
    return data


def metric_mapping(data: Mapping[str, Any], name: str) -> Dict[str, Any]:
    values = data.get(name, {})
    if not isinstance(values, dict):
        raise ValueError(f"best.pkl field {name!r} must be a mapping")
    return values


def format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def markdown_cell(value: Any) -> str:
    return format_value(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: Sequence[Dict[str, Any]]) -> str:
    lines = [
        "| metric | valid | best |",
        "| --- | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {metric} | {valid} | {best} |".format(
                metric=markdown_cell(row["metric"]),
                valid=markdown_cell(row["valid"]),
                best=markdown_cell(row["best"]),
            )
        )
    return "\n".join(lines)


def summarize_best(data: Mapping[str, Any]) -> List[Dict[str, Any]]:
    valid = metric_mapping(data, "valid")
    best = metric_mapping(data, "best")
    metrics = sorted(set(valid) | set(best))
    return [{"metric": name, "valid": valid.get(name), "best": best.get(name)} for name in metrics]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read freerec data/best.pkl metrics.")
    parser.add_argument("path", type=Path, help="Path to data/best.pkl.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Run the best.pkl reader."""

    parser = build_parser()
    namespace = parser.parse_args(argv)

    try:
        rows = summarize_best(load_best(namespace.path))
    except Exception as exc:
        print(f"read_best.py: {exc}", file=sys.stderr)
        return 1

    print(markdown_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
