#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

max_workers="${LIBERPRIMUS_MAX_VALIDATION_WORKERS:-10}"
workers="${LIBERPRIMUS_VALIDATION_WORKERS:-10}"
pytest_workers="${LIBERPRIMUS_PYTEST_WORKERS:-10}"
pytest_mode="${LIBERPRIMUS_PYTEST_MODE:-auto}"
results_dir="${LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR:-"experiments"/"results/ci/parallel-validation/stage5ax"}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-workers) max_workers="$2"; shift 2 ;;
    --workers) workers="$2"; shift 2 ;;
    --pytest-workers) pytest_workers="$2"; shift 2 ;;
    --pytest-mode) pytest_mode="$2"; shift 2 ;;
    --results-dir) results_dir="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

python_bin="${PYTHON:-python}"
run_state_dir="$results_dir/_stage5ax_state"
mkdir -p "$run_state_dir"

if [[ "$workers" -gt "$max_workers" || "$pytest_workers" -gt "$max_workers" ]]; then
  echo "Validation policy caps local parallel validation at $max_workers workers" >&2
  exit 2
fi

"$python_bin" -m libreprimus.cli parallel-validation build-stage5ax-plan \
  --out-plan "$run_state_dir/stage5ax-parallel-validation-plan.yaml" \
  --out-command-registry "$run_state_dir/stage5ax-parallel-command-registry.yaml" \
  --out-run-policy "$run_state_dir/stage5ax-parallel-run-policy.yaml" \
  --out-safety-audit "$run_state_dir/stage5ax-parallel-validation-safety-audit.yaml" \
  --out-pytest-shard-plan "$run_state_dir/stage5ax-pytest-shard-plan.yaml"

set +e
"$python_bin" -m libreprimus.cli parallel-validation run-stage5ax-parallel-validation \
  --plan "$run_state_dir/stage5ax-parallel-validation-plan.yaml" \
  --workers "$workers" \
  --pytest-workers "$pytest_workers" \
  --pytest-mode "$pytest_mode" \
  --results-dir "$results_dir" \
  --out-run-summary "$run_state_dir/stage5ax-parallel-validation-run-summary.yaml" \
  --out-safety-audit "$run_state_dir/stage5ax-parallel-validation-safety-audit.yaml"
run_status=$?
set -e

"$python_bin" -m libreprimus.cli parallel-validation build-stage5ax-summary \
  --plan "$run_state_dir/stage5ax-parallel-validation-plan.yaml" \
  --command-registry "$run_state_dir/stage5ax-parallel-command-registry.yaml" \
  --run-policy "$run_state_dir/stage5ax-parallel-run-policy.yaml" \
  --run-summary "$run_state_dir/stage5ax-parallel-validation-run-summary.yaml" \
  --safety-audit "$run_state_dir/stage5ax-parallel-validation-safety-audit.yaml" \
  --pytest-shard-plan "$run_state_dir/stage5ax-pytest-shard-plan.yaml" \
  --out-guardrail "$run_state_dir/stage5ax-guardrail.yaml" \
  --out-next-stage "$run_state_dir/stage5ax-next-stage-decision.yaml" \
  --out-summary "$run_state_dir/stage5ax-summary.yaml"

"$python_bin" -m libreprimus.cli parallel-validation validate-stage5ax \
  --plan "$run_state_dir/stage5ax-parallel-validation-plan.yaml" \
  --command-registry "$run_state_dir/stage5ax-parallel-command-registry.yaml" \
  --run-policy "$run_state_dir/stage5ax-parallel-run-policy.yaml" \
  --run-summary "$run_state_dir/stage5ax-parallel-validation-run-summary.yaml" \
  --safety-audit "$run_state_dir/stage5ax-parallel-validation-safety-audit.yaml" \
  --pytest-shard-plan "$run_state_dir/stage5ax-pytest-shard-plan.yaml" \
  --guardrail "$run_state_dir/stage5ax-guardrail.yaml" \
  --next-stage-decision "$run_state_dir/stage5ax-next-stage-decision.yaml" \
  --summary "$run_state_dir/stage5ax-summary.yaml" \
  --results-dir "$results_dir"

exit "$run_status"
