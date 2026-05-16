# Stage 2D Follow-Up 2 README Non-Goals Remote Verification

## Initial State

- Branch: `main`.
- Local HEAD: `91135ccf17ad898e82db980cde9d180b694c0b1a`.
- `origin/main`: `91135ccf17ad898e82db980cde9d180b694c0b1a`.
- Local equals remote: `true`.
- Git status before changes: clean.
- Local README top-level `## Non-goals`: `false`.
- `origin/main` README top-level `## Non-goals`: `false`.
- GitHub API README top-level `## Non-goals`: `false`.
- Raw README top-level `## Non-goals`: `false`.
- Local/origin/API/raw README `## Current boundaries and deferred work`: `true`.
- Latest CI status before changes: success.
- Raw/generated/research-report staged: `0/0/0`.
- Discrepancy classification: `none`.

## Changes

- Tightened README wording with the explicit sentence `CUDA/search/scoring are deferred, not permanently excluded.`
- Strengthened README boundary tests to reject exact top-level `## Non-goals` headings and require Stage 2D/Stage 2E wording.
- Added remote README verification scripts using `git fetch` and `git show origin/main:README.md` as the authoritative check.
- Updated public documentation wording policy and remote blob verification docs.
- Added AGENTS rules banning top-level README non-goals sections for temporary boundaries.

## Validation

- Ruff: passed.
- Full pytest: `305 passed`.
- Documentation consistency: `15 pass, 0 fail, 0 warning, 0 skipped`.
- Full consistency suite: `67 pass, 0 fail, 0 warning, 0 skipped`.
- Result-store consistency through `run-consistency-checks.ps1`: `7 pass, 0 fail, 0 warning, 0 skipped`.
- Public docs status script: passed.
- Lock hash verification: passed.
- Workflow static validation: passed.
- Remote README verifier: passed against `origin/main`, GitHub API, and raw URL diagnostics.
- Git safety before commit: raw/generated/research-report staged `0/0/0`.
