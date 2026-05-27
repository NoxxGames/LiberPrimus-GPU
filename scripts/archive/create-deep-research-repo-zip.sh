#!/usr/bin/env sh
set -eu

stage="${1:-stage5bd}"
out_dir="${2:-deep-research-repo-zips/stage5bd}"
mkdir -p "$out_dir"

commit="unavailable"
branch="unavailable"
if command -v git >/dev/null 2>&1; then
  commit="$(git rev-parse HEAD 2>/dev/null || printf unavailable)"
  branch="$(git branch --show-current 2>/dev/null || printf unavailable)"
fi

cat > "$out_dir/ARCHIVE_COMMIT.txt" <<EOF
commit=$commit
branch=$branch
stage=$stage
expected_next_stage=Stage 5BE - Deep Research review of token-block preflight dry-run implementation, archive/evidence hygiene, and execution-gate enforcement
EOF

file_count="$(git ls-files 2>/dev/null | grep -Ev '^(codex-output|human-review-packs|third_party|experiments/results)/' | wc -l | tr -d ' ')"
cat > "$out_dir/ARCHIVE_MANIFEST.json" <<EOF
{
  "repo_name": "NoxxGames/LiberPrimus-GPU",
  "stage": "$stage",
  "commit": "$commit",
  "branch": "$branch",
  "file_count": $file_count,
  "git_directory_included": false,
  "excluded_roots": [".git", "codex-output", "human-review-packs", "third_party", "experiments/results"],
  "instruction": "Use attached repository ZIP as primary evidence."
}
EOF

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$out_dir/ARCHIVE_MANIFEST.json" | awk '{print $1}' > "$out_dir/ARCHIVE_MANIFEST.sha256"
else
  shasum -a 256 "$out_dir/ARCHIVE_MANIFEST.json" | awk '{print $1}' > "$out_dir/ARCHIVE_MANIFEST.sha256"
fi
printf '# Deep Research Repository ZIP\n\nUse attached repository ZIP as primary evidence.\n' > "$out_dir/ARCHIVE_README.md"

if command -v zip >/dev/null 2>&1; then
  zip_path="$out_dir/LiberPrimus-GPU-$stage-review.zip"
  rm -f "$zip_path"
  git ls-files | grep -Ev '^(codex-output|human-review-packs|third_party|experiments/results)/' | zip -q "$zip_path" -@
  zip -q "$zip_path" "$out_dir/ARCHIVE_COMMIT.txt" "$out_dir/ARCHIVE_MANIFEST.json" "$out_dir/ARCHIVE_MANIFEST.sha256" "$out_dir/ARCHIVE_README.md"
  printf 'archive_zip=%s\n' "$zip_path"
else
  printf 'zip_tool_missing=true\n'
fi
printf 'Use attached repository ZIP as primary evidence.\n'
