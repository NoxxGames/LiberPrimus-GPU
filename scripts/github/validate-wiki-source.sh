#!/usr/bin/env bash
set -euo pipefail

TUTORIAL_DIR="${1:-tutorials}"
WIKI_SOURCE_DIR="${2:-docs/wiki-source}"

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
[[ -d "$WIKI_SOURCE_DIR" ]] || { echo "wiki_source_dir_missing=$WIKI_SOURCE_DIR" >&2; exit 1; }
[[ -f "$WIKI_SOURCE_DIR/Home.md" ]] || { echo "missing_home=$WIKI_SOURCE_DIR/Home.md" >&2; exit 1; }
[[ -f "$WIKI_SOURCE_DIR/_Sidebar.md" ]] || { echo "missing_sidebar=$WIKI_SOURCE_DIR/_Sidebar.md" >&2; exit 1; }

count=0
while IFS= read -r -d '' tutorial; do
  file="$(basename "$tutorial")"
  page="$(page_name "$file")"
  path="$WIKI_SOURCE_DIR/$page"
  [[ -f "$path" ]] || { echo "missing_wiki_page=$page" >&2; exit 1; }
  grep -q "repository tutorial file is the source of truth" "$path" || {
    echo "missing_source_of_truth_notice=$page" >&2
    exit 1
  }
  if grep -Eq 'third_party[/\\]LiberPrimusDiscordChats[/\\].+\.html' "$path"; then
    echo "raw_discord_html_path_in_wiki_page=$page" >&2
    exit 1
  fi
  count=$((count + 1))
done < <(find "$TUTORIAL_DIR" -maxdepth 1 -type f -name '*.md' -print0 | sort -z)

echo "wiki_source_valid=true"
echo "tutorial_count=$count"
echo "wiki_page_count=$(find "$WIKI_SOURCE_DIR" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
