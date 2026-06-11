#!/usr/bin/env bash
set -euo pipefail

shard=""
plan=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --shard) shard="$2"; shift 2 ;;
    --plan) plan="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$shard" || -z "$plan" ]]; then
  echo "Usage: run-pytest-shard.sh --shard N --plan path/to/plan.json" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
python_bin="${PYTHON:-python}"

mapfile -t files < <("$python_bin" - "$plan" "$shard" <<'PY'
import sys
from pathlib import Path
import yaml

payload = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8")) or {}
shard_id = f"pytest-shard-{int(sys.argv[2]):02d}"
for shard in payload.get("shards", []):
    if shard.get("shard_id") == shard_id:
        print("\n".join(shard.get("test_files", [])))
        break
else:
    raise SystemExit(f"Pytest shard not found in plan: {shard_id}")
PY
)
"$python_bin" -m pytest -q "${files[@]}"
