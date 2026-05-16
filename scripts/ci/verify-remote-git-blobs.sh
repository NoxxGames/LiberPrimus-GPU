#!/usr/bin/env bash
set -euo pipefail

remote="origin"
branch="main"
minimum_workflow_lines="25"
minimum_gitattributes_lines="10"
check_raw_url="0"
check_github_api="0"
repo_owner="NoxxGames"
repo_name="LiberPrimus-GPU"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote)
      remote="$2"
      shift 2
      ;;
    --branch)
      branch="$2"
      shift 2
      ;;
    --minimum-workflow-lines)
      minimum_workflow_lines="$2"
      shift 2
      ;;
    --minimum-gitattributes-lines)
      minimum_gitattributes_lines="$2"
      shift 2
      ;;
    --check-raw-url)
      check_raw_url="1"
      shift
      ;;
    --check-github-api)
      check_github_api="1"
      shift
      ;;
    --repo-owner)
      repo_owner="$2"
      shift 2
      ;;
    --repo-name)
      repo_name="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

python_bin="${PYTHON:-python}"

"$python_bin" - \
  "$remote" \
  "$branch" \
  "$minimum_workflow_lines" \
  "$minimum_gitattributes_lines" \
  "$check_raw_url" \
  "$check_github_api" \
  "$repo_owner" \
  "$repo_name" <<'PY'
from __future__ import annotations

import base64
import json
import subprocess
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen


(
    remote,
    branch,
    minimum_workflow_lines_raw,
    minimum_gitattributes_lines_raw,
    check_raw_url_raw,
    check_github_api_raw,
    repo_owner,
    repo_name,
) = sys.argv[1:9]
minimum_workflow_lines = int(minimum_workflow_lines_raw)
minimum_gitattributes_lines = int(minimum_gitattributes_lines_raw)
check_raw_url = check_raw_url_raw == "1"
check_github_api = check_github_api_raw == "1"


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True)


def line_report(content: str) -> tuple[int, str]:
    lines = content.replace("\r\n", "\n").split("\n")
    line_count = len(lines) - 1 if lines and lines[-1] == "" else len(lines)
    first_line = lines[0] if line_count else ""
    return line_count, first_line


def remote_blob(path: str) -> str:
    # Authoritative remote verification uses git show against the fetched remote blob.
    return run_git(["show", f"{remote}/{branch}:{path}"])


def require_contains(content: str, snippet: str, label: str) -> None:
    if snippet not in content:
        raise SystemExit(f"{label} is missing required snippet: {snippet}")


def fetch_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": "liberprimus-remote-blob-verifier"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def warn_mismatch(label: str, blob_lines: int, observed_lines: int) -> None:
    if blob_lines != observed_lines:
        print(
            f"WARNING: {label} line count differs from git blob "
            f"({observed_lines} vs {blob_lines}). Raw/API mismatch warning only; "
            "git blob remains authoritative.",
            file=sys.stderr,
        )


subprocess.check_call(["git", "fetch", remote])

workflow = remote_blob(".github/workflows/ci.yml")
attributes = remote_blob(".gitattributes")
workflow_lines, workflow_first = line_report(workflow)
attributes_lines, attributes_first = line_report(attributes)

if workflow_lines <= minimum_workflow_lines:
    raise SystemExit(
        f"Remote git blob workflow line count {workflow_lines} is not greater than "
        f"{minimum_workflow_lines}."
    )
if attributes_lines <= minimum_gitattributes_lines:
    raise SystemExit(
        f"Remote git blob .gitattributes line count {attributes_lines} is not greater than "
        f"{minimum_gitattributes_lines}."
    )
if "name: CI on:" in workflow_first:
    raise SystemExit("Remote git blob workflow appears flattened.")
if "* text=auto .gitattributes" in attributes_first:
    raise SystemExit("Remote git blob .gitattributes appears flattened.")

for snippet in [
    "python-ci:",
    "cmake-cpu-smoke:",
    'python-version: "3.12"',
    "ruff check",
    "pytest -q",
    "transform-registry validate",
    "solved-baseline validate-manifest",
    "result-store validate-manifest",
]:
    require_contains(workflow, snippet, "workflow")

for snippet in [
    "*.json text eol=lf",
    "*.yml text eol=lf",
    "*.sh text eol=lf",
    "*.sha256 text eol=lf",
]:
    require_contains(attributes, snippet, ".gitattributes")

if check_raw_url:
    for path, blob_lines in [
        (".github/workflows/ci.yml", workflow_lines),
        (".gitattributes", attributes_lines),
    ]:
        raw_path = path.lstrip("/").replace("\\", "/")
        url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{raw_path}"
        content = fetch_url(url)
        observed_lines, _ = line_report(content)
        warn_mismatch(f"raw URL {path}", blob_lines, observed_lines)
        print(f"raw_url_{path}_line_count={observed_lines}")

if check_github_api:
    for path, blob_lines in [
        (".github/workflows/ci.yml", workflow_lines),
        (".gitattributes", attributes_lines),
    ]:
        api_path = path.lstrip("/").replace("\\", "/")
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{api_path}?ref={branch}"
        try:
            payload = json.loads(fetch_url(url))
            content = base64.b64decode("".join(payload["content"].split())).decode("utf-8")
        except (KeyError, URLError, ValueError) as exc:
            print(f"WARNING: GitHub API check skipped for {path}: {exc}", file=sys.stderr)
            continue
        observed_lines, _ = line_report(content)
        warn_mismatch(f"GitHub API {path}", blob_lines, observed_lines)
        print(f"github_api_{path}_line_count={observed_lines}")

print("Remote git blob validation OK")
print(f"git_blob_workflow_line_count={workflow_lines}")
print(f"git_blob_gitattributes_line_count={attributes_lines}")
PY
