#!/usr/bin/env python
r"""Summarize freerec tune `results.json` as a Markdown table."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


def load_results(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"results.json does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"failed to parse results.json: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("results.json must contain a mapping")
    return data


def which4best(results: Mapping[str, Any]) -> str:
    config = results.get("config", {})
    if not isinstance(config, Mapping):
        raise ValueError("results.json field config must be a mapping")

    metric = config.get("which4best")
    if not metric:
        raise ValueError("results.json must contain config.which4best")
    return str(metric)


def run_metrics(run: Mapping[str, Any], name: str) -> Dict[str, Any]:
    metrics = run.get("metrics", {})
    if not isinstance(metrics, Mapping):
        return {}

    values = metrics.get(name, {})
    if not isinstance(values, dict):
        return {}
    return values


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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
        "| id | metric | valid | best | params |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {id} | {metric} | {valid} | {best} | {params} |".format(
                id=markdown_cell(row["id"]),
                metric=markdown_cell(row["metric"]),
                valid=markdown_cell(row["valid"]),
                best=markdown_cell(row["best"]),
                params=markdown_cell(row["params"]),
            )
        )
    return "\n".join(lines)


def valid_sort_key(row: Mapping[str, Any]) -> tuple[int, float]:
    value = row["valid"]
    if value is None:
        return (1, 0.0)

    try:
        return (0, -float(value))
    except (TypeError, ValueError):
        return (1, 0.0)


def summarize_results(results: Mapping[str, Any]) -> List[Dict[str, Any]]:
    metric = which4best(results)
    runs = results.get("runs")
    if not isinstance(runs, list):
        raise ValueError("results.json must contain a runs list")

    rows: List[Dict[str, Any]] = []
    for index, run in enumerate(runs):
        if not isinstance(run, Mapping):
            continue

        valid = run_metrics(run, "valid")
        best = run_metrics(run, "best")
        params = run.get("params", {})
        rows.append(
            {
                "id": run.get("id", index),
                "metric": metric,
                "valid": valid.get(metric),
                "best": best.get(metric),
                "params": compact_json(params),
            }
        )

    if not rows:
        raise ValueError("results.json contains no usable runs")
    if all(row["valid"] is None for row in rows):
        raise ValueError(f"metric {metric!r} not found in runs[].metrics.valid")

    rows.sort(key=valid_sort_key)
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize freerec tune results.")
    parser.add_argument("results", type=Path, help="Path to logs/[ExperimentName]/core/results.json.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Run the freerec results summarizer."""

    parser = build_parser()
    namespace = parser.parse_args(argv)

    try:
        rows = summarize_results(load_results(namespace.results))
    except ValueError as exc:
        print(f"summarize_tune_results.py: {exc}", file=sys.stderr)
        return 1

    print(markdown_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
