#!/usr/bin/env bash
set -euo pipefail

stage="stage5ea"
profile="stage-fast"
workers=8
pytest_workers=8

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage) stage="$2"; shift 2 ;;
    --profile) profile="$2"; shift 2 ;;
    --workers) workers="$2"; shift 2 ;;
    --pytest-workers) pytest_workers="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"
parallel_results_root="experiments"/"results"/"ci"/"parallel-validation"
stage_id="$(printf '%s' "$stage" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')"
if [[ -z "$stage_id" ]]; then
  echo "Stage identifier is empty" >&2
  exit 2
fi
if [[ "$stage_id" != stage* ]]; then
  stage_id="stage$stage_id"
fi
stage_display="$(echo "$stage_id" | tr '[:lower:]' '[:upper:]' | sed 's/STAGE/Stage /')"
stage_results_dir="$parallel_results_root"/"$stage_id"

if [[ "$workers" -gt 8 || "$pytest_workers" -gt 8 ]]; then
  echo "Stage validation policy caps local workers at 8" >&2
  exit 2
fi

if [[ "$stage_id" != "stage5dy" && "$stage_id" != "stage5dz" && "$stage_id" != "stage5ea" ]]; then
  echo "run-stage-validation currently supports Stage 5DY, Stage 5DZ, and Stage 5EA" >&2
  exit 2
fi

mapfile -t stage_tests < <(find tests/python -maxdepth 1 -name "test_${stage_id}_*.py" | sort)
validate_command="validate-$stage_id"
summary_command="$stage_id-summary"
stage_module="python/libreprimus/token_block/$stage_id.py"

run_stage_fast() {
  "$python_bin" -m libreprimus.cli token-block "$validate_command"
  "$python_bin" -m libreprimus.cli token-block "$summary_command"
  "$python_bin" -m libreprimus.cli source-browser validate-index
  if [[ "${#stage_tests[@]}" -gt 0 ]]; then
    "$python_bin" -m pytest -q "${stage_tests[@]}"
    "$python_bin" -m ruff check "$stage_module" "${stage_tests[@]}"
  fi
}

case "$profile" in
  focused)
    "$python_bin" -m libreprimus.cli token-block "$validate_command"
    if [[ "${#stage_tests[@]}" -gt 0 ]]; then
      "$python_bin" -m pytest -q "${stage_tests[@]}"
    fi
    ;;
  stage-fast)
    run_stage_fast
    ;;
  local-fast)
    run_stage_fast
    "$python_bin" -m libreprimus.cli consistency check-state-drift
    scripts/ci/run-consistency-checks.sh --profile stage-fast
    ;;
  full-parallel)
    scripts/ci/run-parallel-validation.sh \
      --workers "$workers" \
      --pytest-workers "$pytest_workers" \
      --pytest-mode auto \
      --results-dir "$stage_results_dir"
    ;;
  full-serial-rare)
    echo "Full serial pytest is a rare fallback. Running only because the profile was explicitly requested."
    "$python_bin" -m pytest -q tests/python
    ;;
  ci)
    "$0" --stage "$stage" --profile local-fast --workers "$workers" --pytest-workers "$pytest_workers"
    "$0" --stage "$stage" --profile full-parallel --workers "$workers" --pytest-workers "$pytest_workers"
    ;;
  *)
    echo "Unknown profile: $profile" >&2
    exit 2
    ;;
esac
