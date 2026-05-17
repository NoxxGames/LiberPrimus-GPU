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

echo "Validating Stage 2F CPU execution manifests"
"$python_bin" -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml
"$python_bin" -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-solved-baseline-replay.yaml

echo "Running Stage 2F synthetic direct execution"
"$python_bin" -m libreprimus.cli execution run --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml --out-dir experiments/results/cpu-execution/stage2f --allow-warnings

echo "Validating Stage 2G proposals and approval gates"
"$python_bin" -m libreprimus.cli proposal validate --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml
"$python_bin" -m libreprimus.cli proposal check-approval --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --approval experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml

echo "Generating Stage 2G review packet to temp"
"$python_bin" -m libreprimus.cli proposal review-packet --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --out-dir "$tmp_dir/stage2g-review" --allow-warnings

echo "Validating Stage 2H approval-gated requests"
"$python_bin" -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml
"$python_bin" -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-noop-real-request.yaml

echo "Running Stage 2H approved synthetic request to temp"
"$python_bin" -m libreprimus.cli approval-execution run --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml --out-dir "$tmp_dir/stage2h-approval-execution" --allow-warnings

echo "Validating Stage 2I approval-readiness proposal"
"$python_bin" -m libreprimus.cli approval-readiness validate --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml

echo "Generating Stage 2I readiness packet to temp"
"$python_bin" -m libreprimus.cli approval-readiness packet --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml --out-dir "$tmp_dir/stage2i-readiness" --allow-warnings
