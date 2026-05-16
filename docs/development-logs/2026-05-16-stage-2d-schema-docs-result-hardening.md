# Stage 2D Schema Docs Result Hardening

## Initial State

- Branch: `main`
- Local HEAD: `3d861fd1cc0edd2a5c04c6f13b50b9779c4a892d`
- Origin main: `3d861fd1cc0edd2a5c04c6f13b50b9779c4a892d`
- Local equals origin/main: `true`
- Git status before changes: clean
- Latest CI status: success.
- Remote blob verification: passed.
- Lock-hash verification: passed.
- Public-docs verification: passed.
- Schema dirs present: `true`
- Manifest dirs present: `true`
- Transform registry present: `true`
- Result-store modules present: `true`
- Raw files staged: `0`
- Generated outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`

## Changes

- Added `python/libreprimus/consistency/` with registry, manifest, schema, docs,
  ignored-output, and result-store checks.
- Added `libreprimus consistency` CLI commands.
- Added consistency CI scripts and workflow steps.
- Added ignored consistency output placeholders under `experiments/results/consistency/`.
- Added Stage 2D tests and documentation.

## Validation

- Stage 2D focused tests: `38 passed`.
- Full pytest: `298 passed`.
- Ruff: passed.
- Python smoke: passed.
- Transform registry validation: passed.
- Solved-baseline manifest validation: passed.
- Result-store manifest validation: passed.
- Consistency check-all: `67` pass, `0` fail, `0` warning, `0` skipped.
- Result-store consistency: `7` pass, `0` fail, `0` warning, `0` skipped.
- Lock verification: passed.
- Workflow static validation: passed.
- Public docs status validation: passed.
- Remote Git blob verification: passed.
- Generated consistency summary path is ignored by Git.
- Bash syntax for `run-consistency-checks.sh`: skipped because this Windows host's `bash` delegates to WSL and no WSL distribution is installed.
- C++ tests: skipped; Python/docs/consistency stage only, and C++ files were not changed.
- Raw files staged: `0`
- Generated outputs staged: `0`
- SQLite outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`

## GitHub Issue

- Created issue: `https://github.com/NoxxGames/LiberPrimus-GPU/issues/12`
- Title: `Stage 2D: CI-gated schema/docs consistency and validation hardening`
- Labels requested: `stage-2`, `testing`, `documentation`, `data-provenance`, `needs-human-review`
- Result comment and closure pending commit/push and remote CI verification.
