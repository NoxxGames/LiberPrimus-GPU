#!/usr/bin/env bash
set -euo pipefail

repo_owner="NoxxGames"
repo_name="LiberPrimus-GPU"
branch="main"
workflow_path=".github/workflows/ci.yml"
minimum_line_count="25"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-owner)
      repo_owner="$2"
      shift 2
      ;;
    --repo-name)
      repo_name="$2"
      shift 2
      ;;
    --branch)
      branch="$2"
      shift 2
      ;;
    --workflow-path)
      workflow_path="$2"
      shift 2
      ;;
    --minimum-line-count)
      minimum_line_count="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

python_bin="${PYTHON:-python}"

"$python_bin" - "$repo_owner" "$repo_name" "$branch" "$workflow_path" "$minimum_line_count" <<'PY'
from __future__ import annotations

import sys
from urllib.request import urlopen


repo_owner, repo_name, branch, workflow_path, minimum_line_count_raw = sys.argv[1:6]
minimum_line_count = int(minimum_line_count_raw)
raw_path = workflow_path.lstrip("/").replace("\\", "/")
url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{raw_path}"

print(f"Fetching remote workflow: {url}")
with urlopen(url, timeout=30) as response:
    content = response.read().decode("utf-8")

lines = content.replace("\r\n", "\n").split("\n")
if lines and lines[-1] == "":
    line_count = len(lines) - 1
else:
    line_count = len(lines)

first_line = lines[0] if line_count else ""
if line_count <= minimum_line_count:
    raise SystemExit(
        f"Remote workflow line count {line_count} is not greater than {minimum_line_count}."
    )
if "name: CI on:" in first_line:
    raise SystemExit("Remote workflow appears flattened: first line contains multiple top-level keys.")

required_snippets = [
    "python-ci:",
    "cmake-cpu-smoke:",
    'python-version: "3.12"',
    "ruff check",
    "pytest -q",
    "transform-registry validate",
    "solved-baseline validate-manifest",
    "result-store validate-manifest",
]
for snippet in required_snippets:
    if snippet not in content:
        raise SystemExit(f"Remote workflow is missing required snippet: {snippet}")

forbidden_snippets = [
    "secrets.",
    "upload-artifact",
    "data/" + "raw",
    "experiments/" + "results",
    "LPGPU_ENABLE_CUDA=ON",
]
for snippet in forbidden_snippets:
    if snippet in content:
        raise SystemExit(f"Remote workflow contains forbidden snippet: {snippet}")

print("Remote workflow validation OK")
print(f"line_count={line_count}")
print(f"first_line={first_line}")
PY
