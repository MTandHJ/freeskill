#!/usr/bin/env python
r"""Create a freerec tune YAML from a reusable template."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import yaml


def parse_key_value(text: str) -> Tuple[str, Any]:
    if "=" not in text:
        raise ValueError(f"expected key=value, got: {text}")

    key, value = text.split("=", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"empty key in argument: {text}")

    try:
        parsed = yaml.safe_load(value)
    except yaml.YAMLError as exc:
        raise ValueError(f"failed to parse YAML value for {key}: {exc}") from exc

    return key, parsed


def parse_repeated_key_values(values: Optional[Sequence[str]]) -> Dict[str, Any]:
    parsed: Dict[str, Any] = {}
    for item in values or []:
        key, value = parse_key_value(item)
        parsed[key] = value
    return parsed


def normalize_params(params: Dict[str, Any]) -> Dict[str, List[Any]]:
    normalized: Dict[str, List[Any]] = {}
    for key, value in params.items():
        if isinstance(value, list):
            if not value:
                raise ValueError(f"params.{key} must not be an empty list")
            normalized[key] = value
        else:
            normalized[key] = [value]
    return normalized


def replace_dataset_name(value: Any, dataset: Optional[str]) -> Any:
    if dataset is None:
        return value
    if isinstance(value, str):
        return value.replace("DATASET_NAME", dataset)
    if isinstance(value, list):
        return [replace_dataset_name(item, dataset) for item in value]
    if isinstance(value, dict):
        return {key: replace_dataset_name(item, dataset) for key, item in value.items()}
    return value


def count_grid_trials(params: Dict[str, Sequence[Any]]) -> int:
    if not params:
        return 1

    trial_count = 1
    for key, values in params.items():
        if not values:
            raise ValueError(f"params.{key} must contain at least one value")
        trial_count *= len(values)
    return trial_count


def run_nvidia_smi(args: Sequence[str]) -> List[str]:
    process = subprocess.run(
        ["nvidia-smi", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in process.stdout.splitlines() if line.strip()]


def detect_gpu_loads() -> List[Tuple[str, int]]:
    r"""Return `(gpu_index, compute_process_count)` from nvidia-smi when available."""

    try:
        gpu_lines = run_nvidia_smi(["--query-gpu=index,uuid", "--format=csv,noheader,nounits"])
    except (OSError, subprocess.CalledProcessError):
        return []

    gpu_uuids: Dict[str, str] = {}
    for line in gpu_lines:
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 2:
            index, uuid = parts[0], parts[1]
            gpu_uuids[uuid] = index

    if not gpu_uuids:
        return []

    process_counts = {index: 0 for index in gpu_uuids.values()}
    try:
        process_lines = run_nvidia_smi(["--query-compute-apps=gpu_uuid", "--format=csv,noheader,nounits"])
    except (OSError, subprocess.CalledProcessError):
        return sorted(process_counts.items(), key=lambda item: int(item[0]))

    for uuid in process_lines:
        index = gpu_uuids.get(uuid)
        if index is not None:
            process_counts[index] += 1

    return sorted(process_counts.items(), key=lambda item: int(item[0]))


def allocate_devices(trial_count: int, gpu_loads: Sequence[Tuple[str, int]], max_workers_per_device: int) -> List[str]:
    if trial_count <= 0:
        raise ValueError("trial_count must be positive")
    if max_workers_per_device <= 0:
        raise ValueError("--max-workers-per-device must be positive")
    if not gpu_loads:
        return ["cpu"]

    assignments = {index: 0 for index, _ in gpu_loads}
    existing = {index: max(0, load) for index, load in gpu_loads}
    devices: List[str] = []

    while len(devices) < trial_count:
        candidates = []
        for index, load in existing.items():
            total = load + assignments[index]
            if total < max_workers_per_device:
                candidates.append((total, load, int(index), index))

        if not candidates:
            break

        _, _, _, index = min(candidates)
        assignments[index] += 1
        devices.append(index)

    return devices or ["cpu"]


def auto_device_string(params: Dict[str, Sequence[Any]], max_workers_per_device: int) -> str:
    trial_count = count_grid_trials(params)
    devices = allocate_devices(trial_count, detect_gpu_loads(), max_workers_per_device)
    return ",".join(devices)


def load_template(path: Path) -> Dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"template does not exist: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"failed to parse template YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("template must be a YAML mapping")
    return data


def build_config(namespace: argparse.Namespace) -> Dict[str, Any]:
    config = replace_dataset_name(load_template(namespace.template), namespace.dataset)

    envs = config.setdefault("envs", {})
    params = config.setdefault("params", {})
    defaults = config.setdefault("defaults", {})
    if not isinstance(envs, dict) or not isinstance(params, dict) or not isinstance(defaults, dict):
        raise ValueError("template fields envs, params, and defaults must be mappings")

    if namespace.command is not None:
        config["command"] = namespace.command
    if namespace.root is not None:
        envs["root"] = namespace.root
    if namespace.dataset is not None:
        envs["dataset"] = namespace.dataset
    if namespace.config is not None:
        defaults["config"] = namespace.config

    envs.update(parse_repeated_key_values(namespace.env))
    defaults.update(parse_repeated_key_values(namespace.default))
    params.update(normalize_params(parse_repeated_key_values(namespace.param)))

    if namespace.device is not None:
        envs["device"] = namespace.device
    elif envs.get("device") == "auto":
        envs["device"] = auto_device_string(params, namespace.max_workers_per_device)

    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a freerec tune YAML.")
    skill_dir = Path(__file__).resolve().parents[1]
    parser.add_argument("--output", type=Path, required=True, help="Output tune YAML path.")
    parser.add_argument("--template", type=Path, default=skill_dir / "assets" / "template.yaml")
    parser.add_argument("--command", help="Override the training command.")
    parser.add_argument("--root", help="Override envs.root.")
    parser.add_argument("--dataset", help="Override envs.dataset and replace DATASET_NAME.")
    parser.add_argument("--config", help="Override defaults.config.")
    parser.add_argument("--device", help="Override envs.device and skip automatic device assignment.")
    parser.add_argument("--max-workers-per-device", type=int, default=2)
    parser.add_argument("--param", action="append", help="Add a params key=value entry.")
    parser.add_argument("--default", action="append", help="Add a defaults key=value entry.")
    parser.add_argument("--env", action="append", help="Add an envs key=value entry.")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it exists.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Run the tune config generator."""

    parser = build_parser()
    namespace = parser.parse_args(argv)

    try:
        if namespace.output.exists() and not namespace.force:
            raise ValueError(f"output already exists: {namespace.output}")

        config = build_config(namespace)
        namespace.output.parent.mkdir(parents=True, exist_ok=True)
        namespace.output.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    except ValueError as exc:
        print(f"create_tune_config.py: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {namespace.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
