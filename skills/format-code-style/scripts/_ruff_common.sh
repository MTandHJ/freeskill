#!/usr/bin/env bash

if ! command -v ruff >/dev/null 2>&1; then
    echo "ruff is not installed or not on PATH." >&2
    exit 127
fi

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fallback_config="${skill_root}/assets/ruff.toml"

if [ ! -f "${fallback_config}" ]; then
    echo "fallback Ruff config is missing: ${fallback_config}" >&2
    exit 1
fi

find_project_ruff_config() {
    local dir
    dir="${PWD}"

    while true; do
        if [ -f "${dir}/ruff.toml" ] || [ -f "${dir}/.ruff.toml" ]; then
            return 0
        fi

        if [ -f "${dir}/pyproject.toml" ] && grep -Eq '^[[:space:]]*\[tool\.ruff(\.|\])' "${dir}/pyproject.toml"; then
            return 0
        fi

        if [ "${dir}" = "/" ]; then
            return 1
        fi

        dir="$(dirname "${dir}")"
    done
}

use_fallback_config=0
if ! find_project_ruff_config; then
    use_fallback_config=1
fi

run_ruff() {
    local command
    command="$1"
    shift

    if [ "${use_fallback_config}" = "1" ]; then
        ruff "${command}" --config "${fallback_config}" "$@"
    else
        ruff "${command}" "$@"
    fi
}
