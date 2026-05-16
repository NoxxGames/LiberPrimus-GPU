# Stage 2F Bounded CPU Execution Harness

## Initial State

- Branch: `main`.
- Local HEAD: `e43c70e2653ed39111f9fd4139675466a4b015e2`.
- `origin/main`: `e43c70e2653ed39111f9fd4139675466a4b015e2`.
- Local equals remote: `true`.
- Git status before changes: clean.
- Latest CI status: success.
- Existing consistency suite: `87 pass, 0 fail, 0 warning, 0 skipped`.
- Remote blob verification: passed.
- Stage 2E schemas present: `true`.
- Stage 2E dry-run planner present: `true`.
- Transform registry present: `true`.
- Result store present: `true`.
- Raw/generated/research-report staged: `0/0/0`.

## Implementation Notes

- Added Stage 2F CPU execution schemas, manifests, safety gates, execution planner, synthetic execution runner, solved-fixture replay path, result export, summary loading, CLI commands, tests, and documentation.
- Generated CPU execution outputs are ignored under `experiments/results/cpu-execution/`.
- Stage 2F permits synthetic and solved-fixture-only execution. It blocks unsolved execution, search, candidate generation, scoring, CUDA, canonical corpus activation, and page-boundary finalization.

## Validation

- Stage 2F local execution smoke: passed.
  - Safe manifests executed: `6`.
  - Blocked unsolved manifests: `1`.
  - Execution results: `6 pass, 0 fail, 0 error`.
  - Search, candidate generation, scoring, CUDA, unsolved execution: all `false`.
- `ruff check python/libreprimus tests/python`: passed.
- `pytest -q tests/python`: `383 passed`.
- `libreprimus.cli smoke`: passed.
- `libreprimus.cli consistency check-all --allow-warnings`: `109 pass, 0 fail, 0 warning, 0 skipped`.
- `scripts/ci/run-consistency-checks.ps1`: passed.
- `scripts/ci/verify-public-docs-status.ps1`: `11 passed`.
- `scripts/ci/verify-lock-hashes.ps1`: passed.
- `scripts/ci/validate-workflow-static.ps1`: `13 passed`.
- Generated CPU execution outputs were written only under ignored paths in `experiments/results/cpu-execution/stage2f/`.
- Raw files, generated outputs, SQLite outputs, and `LiberPrimus-Research-Report.md` were not staged.

## GitHub Issue

- Created issue: <https://github.com/NoxxGames/LiberPrimus-GPU/issues/14>.
- Labels: `stage-2`, `experiments`, `testing`, `documentation`, `needs-human-review`.
- Final issue comment/closure depends on post-push CI status.
