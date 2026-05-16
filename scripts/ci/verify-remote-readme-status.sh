#!/usr/bin/env bash
set -euo pipefail

remote="origin"
branch="main"
repo_owner="NoxxGames"
repo_name="LiberPrimus-GPU"
check_raw_url=0
check_github_api=0

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
    --repo-owner)
      repo_owner="$2"
      shift 2
      ;;
    --repo-name)
      repo_name="$2"
      shift 2
      ;;
    --check-raw-url)
      check_raw_url=1
      shift
      ;;
    --check-github-api)
      check_github_api=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

echo "Fetching $remote"
git fetch "$remote"

blob_text="$(git show "$remote/$branch:README.md")"

python - "$repo_owner" "$repo_name" "$branch" "$check_raw_url" "$check_github_api" "$blob_text" <<'PY'
from __future__ import annotations

import base64
import json
import sys
import urllib.request

owner, repo, branch, check_raw, check_api, blob = sys.argv[1:7]


def has_heading(text: str, heading: str) -> bool:
    return heading in text.splitlines()


def assert_readme(text: str, source: str) -> None:
    if has_heading(text, "## Non-goals"):
        raise SystemExit(f"{source} README contains forbidden top-level heading: ## Non-goals")
    if has_heading(text, "## Non-goals for Stage 0A"):
        raise SystemExit(f"{source} README contains forbidden top-level heading: ## Non-goals for Stage 0A")
    required = [
        "## Current boundaries and deferred work",
        "### Permanent safety rules",
        "### Current boundaries",
        "### Deferred future work",
        "### Already implemented since Stage 0A",
        "These are not permanent project exclusions",
        "Canonical corpus: inactive.",
        "No Liber Primus page is claimed solved",
        "Search/scoring/CUDA campaigns: not started",
        "Stage 2D: CI-gated schema/docs consistency and manifest/result-store hardening complete.",
        "Stage 2E CPU exploratory experiment manifest scaffold and dry-run planner",
    ]
    for item in required:
        if item not in text:
            raise SystemExit(f"{source} README is missing required text: {item}")


assert_readme(blob, "git_blob")
print(f"git_blob_readme_line_count={len(blob.splitlines())}")

if check_api == "1":
    try:
        with urllib.request.urlopen(
            f"https://api.github.com/repos/{owner}/{repo}/contents/README.md?ref={branch}",
            timeout=20,
        ) as response:
            payload = json.loads(response.read().decode("utf-8"))
        api_text = base64.b64decode(payload["content"]).decode("utf-8")
        assert_readme(api_text, "github_api")
        print(f"github_api_readme_line_count={len(api_text.splitlines())}")
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: GitHub API README check failed: {exc}", file=sys.stderr)

if check_raw == "1":
    try:
        with urllib.request.urlopen(
            f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md",
            timeout=20,
        ) as response:
            raw_text = response.read().decode("utf-8")
        try:
            assert_readme(raw_text, "raw_url")
        except SystemExit as exc:
            print(f"WARNING: Raw README status differs from git blob/API: {exc}", file=sys.stderr)
        print(f"raw_url_readme_line_count={len(raw_text.splitlines())}")
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: Raw README fetch failed: {exc}", file=sys.stderr)

print("Remote README status validation OK")
PY
