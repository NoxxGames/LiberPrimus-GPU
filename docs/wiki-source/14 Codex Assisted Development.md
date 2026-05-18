> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

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
- For Stage 3S/3T/3U-style execution, state the exact manifest ID, candidate or claim cap, generated output paths, and that no other post-Discord manifest may run in the same stage.
- For Stage 3V-style stego work, state whether missing OutGuess tools/assets should skip, list the exact manifest, and prohibit broad image scans.
- For Stage 3W-style consolidation, state that no experiments should run and require source-of-truth docs plus anti-drift checks to stay synchronized.
- For Stage 3X-style CLI modularisation, state that command names, options, help behavior, output shape, and exit semantics must be preserved and that command-surface tests must be added or updated.

## Commands

```powershell
git status --short
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

## What Not To Commit

Raw corpus material, generated outputs, root research reports, `.venv/`, build dirs, and wiki
worktrees. For Stage 3R/3S/3T/3U/3V-style work, also keep generated Discord review bundles, topic shards, promotion audit JSONL, post-Discord candidate JSONL, verification JSONL, hash candidate JSONL, OutGuess extraction JSONL, extracted payloads, summary JSON, and root report copies out of staging unless copied into `docs/` intentionally.

Keep `deep-research-reports/**` out of staging; it is local review material only.

## Troubleshooting

If Codex sees unrelated untracked files, keep them out of staging unless the user explicitly asks
to include them.

If Codex creates disabled experiment manifests, verify `execution_enabled=false`,
`cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and
`page_boundaries_final=false` before committing.

If Codex executes a bounded manifest, verify the command ran only the requested manifest, raw
Discord logs and raw page images were not processed, and generated result files remain ignored.

If Codex runs OutGuess regression, verify missing tools/assets are recorded as skips when allowed,
raw historical artefacts remain ignored, and non-empty payloads are not interpreted without expected
hash validation.

If Codex updates stage state, verify `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` are
synchronized and run `libreprimus consistency check-state-drift` before staging.

If Codex changes CLI registration, verify `python -m libreprimus.cli --help`, selected group
`--help` commands, and the Stage 3X command-surface tests before staging. Do not create
`python/libreprimus/cli/` while `python/libreprimus/cli.py` remains the public entrypoint.
