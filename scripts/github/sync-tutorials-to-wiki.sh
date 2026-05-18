#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
PUBLISH=0
REPO="NoxxGames/LiberPrimus-GPU"
WIKI_REMOTE="https://github.com/NoxxGames/LiberPrimus-GPU.wiki.git"
TUTORIAL_DIR="tutorials"
WIKI_SOURCE_DIR="docs/wiki-source"
WIKI_WORKTREE_DIR=".wiki-worktree"
REPORT_PATH="experiments/results/wiki-sync/stage3o/wiki-sync-report.json"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --DryRun|--dry-run) DRY_RUN=1; shift ;;
    --Publish|--publish) PUBLISH=1; shift ;;
    --Repo|--repo) REPO="$2"; shift 2 ;;
    --WikiRemote|--wiki-remote) WIKI_REMOTE="$2"; shift 2 ;;
    --TutorialDir|--tutorial-dir) TUTORIAL_DIR="$2"; shift 2 ;;
    --WikiSourceDir|--wiki-source-dir) WIKI_SOURCE_DIR="$2"; shift 2 ;;
    *) echo "unknown_arg=$1" >&2; exit 2 ;;
  esac
done

if [[ "$DRY_RUN" -eq 0 && "$PUBLISH" -eq 0 ]]; then
  DRY_RUN=1
fi

page_name() {
  local file="$1"
  local stem="${file%.md}"
  local out=""
  IFS='-' read -ra parts <<< "$stem"
  for part in "${parts[@]}"; do
    if [[ -n "$out" ]]; then out+=" "; fi
    if [[ "$part" =~ ^[0-9]+$ ]]; then
      out+="$part"
    else
      out+="$(tr '[:lower:]' '[:upper:]' <<< "${part:0:1}")$(tr '[:upper:]' '[:lower:]' <<< "${part:1}")"
    fi
  done
  printf '%s.md' "$out"
}

[[ -d "$TUTORIAL_DIR" ]] || { echo "tutorial_dir_missing=$TUTORIAL_DIR" >&2; exit 1; }
mkdir -p "$WIKI_SOURCE_DIR"
find "$WIKI_SOURCE_DIR" -maxdepth 1 -type f -name '*.md' -delete

pages=()
while IFS= read -r -d '' tutorial; do
  file="$(basename "$tutorial")"
  page="$(page_name "$file")"
  pages+=("$page")
  {
    echo "> This Wiki page mirrors \`tutorials/$file\`. The repository tutorial file is the source of truth."
    echo
    sed -e :a -e '/^[[:space:]]*$/{$d;N;ba' -e '}' "$tutorial"
  } > "$WIKI_SOURCE_DIR/$page"
done < <(find "$TUTORIAL_DIR" -maxdepth 1 -type f -name '*.md' -print0 | sort -z)

{
  echo "# Liber Primus GPU Wiki Mirror"
  echo
  echo "This Wiki mirrors the repository tutorials. The repository files under \`tutorials/\` are the source of truth."
  echo
  for page in "${pages[@]}"; do
    title="${page%.md}"
    echo "- [[$title]]"
  done
} > "$WIKI_SOURCE_DIR/Home.md"

{
  echo "# Tutorials"
  for page in "${pages[@]}"; do
    title="${page%.md}"
    echo "- [[$title]]"
  done
} > "$WIKI_SOURCE_DIR/_Sidebar.md"

"$(dirname "$0")/validate-wiki-source.sh" "$TUTORIAL_DIR" "$WIKI_SOURCE_DIR"
mkdir -p "$(dirname "$REPORT_PATH")"
cat > "$REPORT_PATH" <<JSON
{
  "repo": "$REPO",
  "wiki_remote": "$WIKI_REMOTE",
  "dry_run": $([[ "$DRY_RUN" -eq 1 ]] && echo true || echo false),
  "publish": $([[ "$PUBLISH" -eq 1 ]] && echo true || echo false),
  "wiki_source_dir": "$WIKI_SOURCE_DIR",
  "tutorial_count": ${#pages[@]},
  "wiki_page_count": $(find "$WIKI_SOURCE_DIR" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' '),
  "publish_attempted": false,
  "publish_succeeded": false,
  "wiki_commit": null,
  "failure_reason": null
}
JSON

if [[ "$DRY_RUN" -eq 1 && "$PUBLISH" -eq 0 ]]; then
  echo "dry_run=true"
  echo "tutorial_pages=${#pages[@]}"
  exit 0
fi

if [[ "$PUBLISH" -eq 1 ]]; then
  if ! git ls-remote "$WIKI_REMOTE" >/dev/null 2>&1; then
    echo "Wiki remote is not accessible: $WIKI_REMOTE" >&2
    exit 1
  fi
  if [[ -d "$WIKI_WORKTREE_DIR/.git" ]]; then
    git -C "$WIKI_WORKTREE_DIR" fetch origin
    git -C "$WIKI_WORKTREE_DIR" checkout master
    git -C "$WIKI_WORKTREE_DIR" pull --ff-only origin master
  else
    git clone "$WIKI_REMOTE" "$WIKI_WORKTREE_DIR"
  fi
  cp "$WIKI_SOURCE_DIR"/*.md "$WIKI_WORKTREE_DIR"/
  git -C "$WIKI_WORKTREE_DIR" add -- '*.md'
  if [[ -n "$(git -C "$WIKI_WORKTREE_DIR" status --short)" ]]; then
    git -C "$WIKI_WORKTREE_DIR" commit -m "Sync tutorials from main repository"
    git -C "$WIKI_WORKTREE_DIR" push origin HEAD
    echo "wiki_commit=$(git -C "$WIKI_WORKTREE_DIR" rev-parse HEAD)"
  else
    echo "wiki_no_changes=true"
  fi
fi
