# Codex Assisted Development

## Purpose

Use Codex safely for scoped repository stages.

## Prompt Checklist

- State the current stage and latest commit.
- Include explicit non-goals.
- List raw/generated files that must not be staged.
- Require tests, docs, developer logs, commit, push, and CI verification.
- Require GitHub issue updates when relevant.
- For Discord stages, state that raw logs, generated shards, message bodies, usernames, user IDs, message IDs, and private URLs must not be staged.
- For post-Discord manifests, state whether the stage is queue-only or execution-authorized.
- For Stage 3S/3T-style execution, state the exact manifest ID, candidate or claim cap, generated output paths, and that no other post-Discord manifest may run in the same stage.

## Commands

```powershell
git status --short
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

## What Not To Commit

Raw corpus material, generated outputs, root research reports, `.venv/`, build dirs, and wiki
worktrees. For Stage 3R/3S/3T-style work, also keep generated Discord review bundles, topic shards, promotion audit JSONL, post-Discord candidate JSONL, verification JSONL, summary JSON, and root report copies out of staging unless copied into `docs/` intentionally.

## Troubleshooting

If Codex sees unrelated untracked files, keep them out of staging unless the user explicitly asks
to include them.

If Codex creates disabled experiment manifests, verify `execution_enabled=false`,
`cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and
`page_boundaries_final=false` before committing.

If Codex executes a bounded manifest, verify the command ran only the requested manifest, raw
Discord logs and raw page images were not processed, and generated result files remain ignored.
