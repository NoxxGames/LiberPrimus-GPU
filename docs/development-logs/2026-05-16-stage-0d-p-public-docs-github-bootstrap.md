# 2026-05-16 Stage 0D-P Public Docs And GitHub Bootstrap

## Task Summary

Added public tutorials, GitHub issue/wiki bootstrap files, GitHub helper scripts, and push workflow policy.

## Starting State

- Branch: `main`
- Starting commit: `5c66ad59cdc5482b761317235cd9e2b4405db690`
- Starting status: `.gitignore` had a pre-existing unstaged change for `LiberPrimus-Research-Report.md`; `LiberPrimus-Research-Report.md` was untracked.
- `gh` was found at `C:\Program Files\GitHub CLI\gh.exe`.
- Authenticated GitHub user: `NoxxGames`.
- Target repo: `NoxxGames/LiberPrimus-GPU`.
- `origin`: `https://github.com/NoxxGames/LiberPrimusSolver.git`, which GitHub resolves to `NoxxGames/LiberPrimus-GPU`.

## Remote And Push Policy

`origin` was treated as verified because GitHub resolves the old remote URL to the target repository. The remote URL was not changed.

AGENTS.md now requires pushing after successful commits when the remote is verified and validation passes.

## Tutorials

Added top-level `tutorials/` with setup, data, CLI, alignment, hardware, GitHub, and Codex-assisted development guides.

## GitHub Issue Infrastructure

Added issue templates, label definitions, ten local issue seed files, and idempotent scripts for label and issue creation.

## GitHub Wiki Infrastructure

Added wiki source pages under `docs/github/wiki-pages/` and a publish script that uses an ignored `.wiki-worktree/`.

## Dry Runs

GitHub verification passed for `NoxxGames/LiberPrimus-GPU`.

Dry-run results:

- `verify-github-remote.ps1`: passed.
- `create-issues.ps1 -DryRun`: passed; 10 issues would be created, 0 exact-title duplicates found.
- `publish-wiki.ps1 -DryRun`: passed; 16 wiki source pages found.
- `gh repo edit --enable-issues --enable-wiki`: completed; issues and wiki remain enabled.

## Validation

Before first commit:

- Python tests: `55 passed`.
- C++ tests: skipped because this is a docs/GitHub/tutorials stage only.
- Tutorials, issue seeds, wiki source pages, and GitHub scripts exist.
- `.wiki-worktree/` is ignored.

## Git Safety

Raw data, generated outputs, `.venv`, build outputs, `.wiki-worktree/`, and `LiberPrimus-Research-Report.md` must remain unstaged.

Before first commit validation confirmed raw files, generated outputs, `.wiki-worktree/`, `.venv`, build outputs, and `LiberPrimus-Research-Report.md` were not staged.

## First Commit And Push

- Commit: `1d2500a40c0c3abf30e334cfc0e20a70d7cbb6cf`
- Push: succeeded to `origin/main`.
- GitHub reported that the old origin URL moved to `https://github.com/NoxxGames/LiberPrimus-GPU.git`; the remote was not rewritten.

## GitHub Labels And Issues

- Labels created or updated: `17`
- Issues created: `10`
- Issues skipped as existing: `0`
- Bootstrap report: `docs/github/issue-bootstrap-report.md`

Issue URLs:

- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/1`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/2`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/3`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/4`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/5`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/6`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/7`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/8`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/9`
- `https://github.com/NoxxGames/LiberPrimus-GPU/issues/10`

## GitHub Wiki Publish

Wiki source pages were prepared under `docs/github/wiki-pages/`.

Publish was attempted, but the wiki git endpoint returned `Repository not found` for `https://github.com/NoxxGames/LiberPrimus-GPU.wiki.git` even though `gh repo view` reports `hasWikiEnabled=true`. No force-push or destructive retry was attempted. The local `.wiki-worktree/` remains ignored and was not staged.

## Known Limitations

The tutorials are introductory and must evolve with the workbench. Stage 0D-followup alignment work remains unresolved.

## Next Recommended Stage

Stage 0D-followup - resolve transcript-alignment gaps, audit overconfident page-boundary candidates, improve bounded alignment passes, and preserve non-canonical confidence labels before any corpus freeze.
