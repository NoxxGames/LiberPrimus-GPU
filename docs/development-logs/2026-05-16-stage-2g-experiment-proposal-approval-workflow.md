# Stage 2G Experiment Proposal Approval Workflow

## Initial State

- Branch: `main`.
- Local HEAD: `abeefd45be7d2cd3332bc6f971c98efb9a811ef3`.
- `origin/main`: `abeefd45be7d2cd3332bc6f971c98efb9a811ef3`.
- Local equals remote: `true`.
- Git status before changes: clean.
- Latest CI status: success.
- Existing consistency suite: `109 pass, 0 fail, 0 warning, 0 skipped`.
- Remote blob verification: passed.
- Stage 2F execution harness present: `true`.
- Stage 2E dry-run planner present: `true`.
- Stage 2D consistency package present: `true`.
- Raw/generated/research-report staged: `0/0/0`.

## Implementation Notes

- Stage 2G adds proposal schemas, approval records, review checklists, approval gates, review-packet generation, CLI commands, tests, and documentation.
- All committed proposal examples remain blocked pending explicit human approval.
- Stage 2G does not execute proposals, generate candidates, score outputs, use CUDA, activate the canonical corpus, or finalize page boundaries.

## Validation

- Stage 2G targeted tests: `35 passed`.
- `ruff check python/libreprimus tests/python`: passed.
- `pytest -q tests/python`: `418 passed`.
- `libreprimus.cli smoke`: passed.
- `libreprimus.cli consistency check-all --allow-warnings`: `131 pass, 0 fail, 0 warning, 0 skipped`.
- `scripts/ci/run-consistency-checks.ps1`: passed.
- `scripts/ci/verify-public-docs-status.ps1`: `11 passed`.
- `scripts/ci/verify-lock-hashes.ps1`: passed.
- `scripts/ci/validate-workflow-static.ps1`: `13 passed`.
- Stage 2G local review smoke generated `5` packets, blocked `5` proposals, and approved `0`.
- Generated review packets were written only under ignored paths in `experiments/results/proposal-reviews/stage2g/`.
- Raw files, generated outputs, SQLite outputs, and `LiberPrimus-Research-Report.md` were not staged.

## GitHub Issue

- Created issue: <https://github.com/NoxxGames/LiberPrimus-GPU/issues/15>.
- Labels: `stage-2`, `experiments`, `testing`, `documentation`, `needs-human-review`.
- Final issue comment/closure depends on post-push CI status.
