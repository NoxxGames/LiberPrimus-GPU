#!/usr/bin/env bash
set -euo pipefail

stage="stage5dy"
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
stage5dy_results_dir="experiments"/"results"/"ci"/"parallel-validation"/"stage5dy"

if [[ "$workers" -gt 8 || "$pytest_workers" -gt 8 ]]; then
  echo "Stage 5DY validation policy caps local workers at 8" >&2
  exit 2
fi

if [[ "$stage" != "stage5dy" && "$stage" != "stage-5dy" ]]; then
  echo "run-stage-validation currently supports Stage 5DY only" >&2
  exit 2
fi

mapfile -t stage_tests < <(find tests/python -maxdepth 1 -name 'test_stage5dy_*.py' | sort)

run_stage_fast() {
  "$python_bin" -m libreprimus.cli token-block validate-stage5dy
  "$python_bin" -m libreprimus.cli token-block stage5dy-summary
  "$python_bin" -m libreprimus.cli source-browser validate-index
  if [[ "${#stage_tests[@]}" -gt 0 ]]; then
    "$python_bin" -m pytest -q "${stage_tests[@]}"
    "$python_bin" -m ruff check python/libreprimus/token_block/stage5dy.py "${stage_tests[@]}"
  fi
}

case "$profile" in
  focused)
    "$python_bin" -m libreprimus.cli token-block validate-stage5dy
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
      --results-dir "$stage5dy_results_dir"
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
