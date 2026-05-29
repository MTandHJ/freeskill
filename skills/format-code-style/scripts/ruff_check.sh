#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_ruff_common.sh"

targets=("$@")
if [ "${#targets[@]}" -eq 0 ]; then
    targets=(".")
fi

run_ruff check "${targets[@]}"
