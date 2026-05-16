# Stage 2D Follow-Up README Boundaries

## Initial State

- Branch: `main`.
- Local HEAD: `9526068c9ff899f1ce178867025eeb480955ea24`.
- `origin/main`: `9526068c9ff899f1ce178867025eeb480955ea24`.
- Local equals remote: `true`.
- Git status before changes: clean.
- README exact `## Non-goals for Stage 0A` heading present: `false`.
- README retained ambiguous top-level `## Non-goals` wording: `true`.
- README current status and next milestone checks: passing.
- STATUS current: `true`.
- ROADMAP current: `true`.
- Raw/generated/research-report staged: `0/0/0`.

## Changes

- Replaced the README top-level non-goals section with `Current boundaries and deferred work`.
- Added explicit subsections for permanent safety rules, current boundaries, deferred future work, and completed work since Stage 0A.
- Cleaned nearby Stage 0A-era README wording for CUDA, data policy, and testing policy.
- Added public documentation wording policy.
- Added static README boundary tests.
- Added AGENTS public documentation wording rules.

## Validation

- Focused README/docs tests: `14 passed`.
- Ruff: passed.
- Full pytest: `304 passed`.
- Python smoke: passed.
- Documentation consistency: `15 pass, 0 fail, 0 warning, 0 skipped`.
- Full consistency suite: `67 pass, 0 fail, 0 warning, 0 skipped`.
- Result-store consistency through `run-consistency-checks.ps1`: `7 pass, 0 fail, 0 warning, 0 skipped`.
- Public docs status script: passed.
- Lock hash verification: passed.
- Workflow static validation: passed.
- Git safety before commit: raw/generated/research-report staged `0/0/0`.
