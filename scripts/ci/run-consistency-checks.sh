#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

echo "Running full consistency suite"
"$python_bin" -m libreprimus.cli consistency check-all --allow-warnings

echo "Running result-store consistency suite"
"$python_bin" -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings

echo "Exporting consistency summary to temp"
"$python_bin" -m libreprimus.cli consistency check-all --out "$tmp_dir/consistency_summary.json" --allow-warnings

echo "Validating Stage 2E exploratory manifests"
"$python_bin" -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml
"$python_bin" -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-affine-preview-dry-run.yaml

echo "Dry-running Stage 2E Caesar preview to temp"
"$python_bin" -m libreprimus.cli experiment dry-run --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml --out-dir "$tmp_dir/stage2e-dry-run" --allow-warnings
