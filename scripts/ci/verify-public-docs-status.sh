#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"

echo "Validating public documentation status"
"$python_bin" -m pytest -q tests/python/test_stage2c_public_docs_status.py
