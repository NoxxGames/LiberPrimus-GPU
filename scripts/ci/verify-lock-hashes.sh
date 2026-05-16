#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"

line_count="$("$python_bin" - <<'PY'
from pathlib import Path
print(len(Path(".gitattributes").read_text(encoding="utf-8").splitlines()))
PY
)"
if [[ "$line_count" -le 10 ]]; then
  echo ".gitattributes must have more than 10 physical lines." >&2
  exit 1
fi

if grep -Fq "* text=auto .gitattributes" .gitattributes; then
  echo ".gitattributes appears to be flattened onto one line." >&2
  exit 1
fi

for required in "*.json text eol=lf" "*.sha256 text eol=lf" "*.yml text eol=lf" "*.sh text eol=lf"; do
  if ! grep -Fxq "$required" .gitattributes; then
    echo ".gitattributes is missing required rule: $required" >&2
    exit 1
  fi
done

echo "Validating canonical JSON locks"
"$python_bin" scripts/ci/repair-canonical-json-locks.py --check
echo "Lock hash validation OK"
