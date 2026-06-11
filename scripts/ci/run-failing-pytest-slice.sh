#!/usr/bin/env bash
set -euo pipefail

results_dir=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --results-dir) results_dir="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$results_dir" ]]; then
  echo "Usage: run-failing-pytest-slice.sh --results-dir path" >&2
  exit 2
fi

summary="$(find "$results_dir" \( -name '*run-summary*.yaml' -o -name '*run-summary*.yml' -o -name '*run-summary*.json' \) -type f | sort | tail -n 1)"
if [[ -z "$summary" ]]; then
  echo "No parallel-validation run summary found under $results_dir" >&2
  exit 2
fi
echo "Inspect run summary for failure_rerun_commands: $summary"
if [[ "$summary" == *.json ]]; then
  python - "$summary" <<'PY'
import json
import sys
from pathlib import Path

record = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
pytest_result = record.get("pytest_result") or {}
for command in pytest_result.get("failure_rerun_commands") or []:
    print(command)
for shard in pytest_result.get("shard_results") or []:
    if not shard.get("passed") and shard.get("rerun_command"):
        print(shard["rerun_command"])
PY
else
  grep -n -A3 -E 'rerun_command|failure_rerun_commands|rerun_guidance' "$summary" || true
fi
