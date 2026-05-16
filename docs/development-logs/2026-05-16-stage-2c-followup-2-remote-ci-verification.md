# Stage 2C-followup-2 Remote CI Verification

## Initial State

- Branch: `main`
- Local commit: `3decc088754e636995272edf7ab2d52fc000b7e2`
- Remote main commit: `3decc088754e636995272edf7ab2d52fc000b7e2`
- Local equals remote: `true`
- Git status before changes: clean
- Local workflow line count: `70`
- Remote raw workflow line count: `71`
- Local workflow flattened/minified suspected: `false`
- Remote workflow flattened/minified suspected: `false`
- `gh` in PATH: `true`
- Absolute `gh.exe` path found: `C:\Program Files\GitHub CLI\gh.exe`
- `gh` authenticated: `true`
- Raw files staged: `0`
- Generated outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`

## Observations

The public raw workflow fetched during this stage was already readable multi-line YAML. The previous GitHub Actions run was visible through `gh`, but failed during Python tests because Linux checkout line endings caused SHA-256 lock mismatches in committed structured JSON locks. This stage records that as a remote CI run observation; it does not weaken CI or remove checks.

## Changes

- Added raw GitHub workflow verification scripts for PowerShell and shell.
- Strengthened static workflow tests to reject a flattened `name: CI on:` sample.
- Documented GitHub CLI path troubleshooting and remote verification without `gh`.
- Updated CI docs, testing notes, roadmap/status, and agent rules.

## Validation

Local validation completed before commit. Post-push raw workflow verification is recorded after push.

## Validation Update

- Local workflow line count after rewrite: `68`
- Remote verifier pre-push check: passed against current `main`
- Ruff: passed
- Pytest: `236 passed`
- Python smoke: passed
- Transform registry validation: passed locally
- Solved-baseline manifest validation: passed locally
- Result-store manifest validation: passed locally
- CI PowerShell scripts: passed
- Workflow static validation script: passed
- Bash syntax checks: skipped; local `bash` delegates to WSL and no WSL distributions are installed.
- CMake CPU smoke: configure/build/CTest passed with Visual Studio Debug config and `LPGPU_ENABLE_CUDA=OFF`.
- Git safety: raw files staged `0`, generated outputs staged `0`, SQLite outputs staged `0`, `LiberPrimus-Research-Report.md` staged `0`.

## GitHub Issue Status

`gh` is available and authenticated in this shell via `C:\Program Files\GitHub CLI\gh.exe`. Issue #7 was found and updated with a Stage 2C-followup-2 status comment. The issue remains open pending post-push verification because the latest visible CI run failed before this follow-up.
