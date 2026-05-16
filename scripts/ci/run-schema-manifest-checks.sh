#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"

echo "Validating lock hashes"
bash scripts/ci/verify-lock-hashes.sh

echo "Validating profile summaries"
"$python_bin" -m libreprimus.cli profile summary

echo "Validating transform registry"
"$python_bin" -m libreprimus.cli transform-registry validate --registry data/transform-registry/cpu-reference-transforms-v0.json

solved_manifests=(
  "experiments/manifests/solved-baselines/direct-translation-v0.yaml"
  "experiments/manifests/solved-baselines/atbash-family-v0.yaml"
  "experiments/manifests/solved-baselines/vigenere-v0.yaml"
  "experiments/manifests/solved-baselines/prime-stream-v0.yaml"
  "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml"
)

for manifest in "${solved_manifests[@]}"; do
  echo "Validating solved-baseline manifest $manifest"
  "$python_bin" -m libreprimus.cli solved-baseline validate-manifest --manifest "$manifest"
done

echo "Validating result-store manifest"
"$python_bin" -m libreprimus.cli result-store validate-manifest --manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml

echo "Running consistency checks"
"$python_bin" -m libreprimus.cli consistency check-all --allow-warnings
