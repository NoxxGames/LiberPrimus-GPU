# Stage 2C-followup-5 Remote Blob Consistency

## Initial State

- Branch: `main`
- Local HEAD: `0813b138dc7ede8a0ea3ff96ad3fd4b6e234a66b`
- Origin main: `0813b138dc7ede8a0ea3ff96ad3fd4b6e234a66b`
- Local equals origin/main: `true`
- Git status before changes: clean
- Local workflow line count: `71`
- Origin/main workflow blob line count: `54` via `git show` pipeline; above threshold.
- Raw URL workflow line count: `72`
- Cache-busted raw workflow line count: `72`
- GitHub API workflow line count: `72`
- Local `.gitattributes` line count: `45`
- Origin/main `.gitattributes` blob line count: `39` via `git show` pipeline; above threshold.
- Raw URL `.gitattributes` line count: `46`
- Cache-busted raw `.gitattributes` line count: `46`
- GitHub API `.gitattributes` line count: `46`
- Latest CI status: `success`
- Raw files staged: `0`
- Generated outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`
- Discrepancy classification: `none` for current observable state.

## Decision

The authoritative `origin/main` blobs and GitHub API contents are readable
multi-line files. No workflow or `.gitattributes` rewrite is required. This
stage adds remote blob verification tooling and documents that raw GitHub URLs
are lower-trust diagnostics when they disagree with fetched Git blobs.

## Changes

- Added `scripts/ci/verify-remote-git-blobs.ps1`.
- Added `scripts/ci/verify-remote-git-blobs.sh`.
- Added `tests/python/test_stage2c_remote_blob_verifier.py`.
- Added `docs/ci/remote-blob-verification.md`.
- Updated CI documentation, testing notes, roadmap/status text, and AGENTS rules.

## Corrective Content Changes

- Workflow changed: `false`
- `.gitattributes` changed: `false`
- Reason: local files, `origin/main` blobs, GitHub API contents, and current raw URLs are already readable multi-line files.
- Classification: `none`
- Lock verification after changes: passed.

## Local Validation

- Ruff: passed.
- Pytest: `260 passed in 42.95s`.
- Python smoke: passed.
- Transform registry validation: passed.
- Solved-baseline manifest validation: passed.
- Result-store manifest validation: passed.
- Lock verification: passed.
- Workflow static validation: passed.
- Public docs status validation: passed.
- Raw workflow verifier: passed.
- Remote Git blob verifier: passed with workflow and `.gitattributes` line counts `71/45` for Git blob, raw URL, and API.
- Bash syntax for `verify-remote-git-blobs.sh`: skipped because this Windows host's `bash` delegates to WSL and no WSL distribution is installed.
- Raw files staged: `0`
- Generated outputs staged: `0`
- SQLite outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`

## Git Safety

Only verification scripts, tests, docs, developer log, research log, and status/roadmap/testing/AGENTS updates are intended for staging. Raw data, generated outputs, SQLite databases, virtual environments, build outputs, and `LiberPrimus-Research-Report.md` remain unstaged.
