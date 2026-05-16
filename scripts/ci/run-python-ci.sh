#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"

echo "Running Ruff"
"$python_bin" -m ruff check python/libreprimus tests/python

echo "Running pytest"
"$python_bin" -m pytest -q tests/python

echo "Running Python smoke"
"$python_bin" -m libreprimus.cli smoke
