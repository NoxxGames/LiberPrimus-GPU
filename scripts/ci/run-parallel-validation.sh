#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

workers="${LIBERPRIMUS_VALIDATION_WORKERS:-16}"
pytest_workers="${LIBERPRIMUS_PYTEST_WORKERS:-16}"
pytest_mode="${LIBERPRIMUS_PYTEST_MODE:-auto}"
results_dir="${LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR:-"experiments"/"results/ci/parallel-validation/stage5ax"}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workers) workers="$2"; shift 2 ;;
    --pytest-workers) pytest_workers="$2"; shift 2 ;;
    --pytest-mode) pytest_mode="$2"; shift 2 ;;
    --results-dir) results_dir="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

python_bin="${PYTHON:-python}"

"$python_bin" -m libreprimus.cli parallel-validation build-stage5ax-plan \
  --out-plan data/ci/stage5ax-parallel-validation-plan.yaml \
  --out-command-registry data/ci/stage5ax-parallel-command-registry.yaml \
  --out-run-policy data/ci/stage5ax-parallel-run-policy.yaml \
  --out-safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml \
  --out-pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml

"$python_bin" -m libreprimus.cli parallel-validation run-stage5ax-parallel-validation \
  --plan data/ci/stage5ax-parallel-validation-plan.yaml \
  --workers "$workers" \
  --pytest-workers "$pytest_workers" \
  --pytest-mode "$pytest_mode" \
  --results-dir "$results_dir" \
  --out-run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml

"$python_bin" -m libreprimus.cli parallel-validation build-stage5ax-summary \
  --plan data/ci/stage5ax-parallel-validation-plan.yaml \
  --command-registry data/ci/stage5ax-parallel-command-registry.yaml \
  --run-policy data/ci/stage5ax-parallel-run-policy.yaml \
  --run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml \
  --safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml \
  --pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml \
  --out-guardrail data/ci/stage5ax-guardrail.yaml \
  --out-next-stage data/project-state/stage5ax-next-stage-decision.yaml \
  --out-summary data/project-state/stage5ax-summary.yaml

"$python_bin" -m libreprimus.cli parallel-validation validate-stage5ax \
  --plan data/ci/stage5ax-parallel-validation-plan.yaml \
  --command-registry data/ci/stage5ax-parallel-command-registry.yaml \
  --run-policy data/ci/stage5ax-parallel-run-policy.yaml \
  --run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml \
  --safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml \
  --pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml \
  --guardrail data/ci/stage5ax-guardrail.yaml \
  --next-stage-decision data/project-state/stage5ax-next-stage-decision.yaml \
  --summary data/project-state/stage5ax-summary.yaml \
  --results-dir "$results_dir"
