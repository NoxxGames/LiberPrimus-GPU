# Stage 5BF Historical Route Source Lock

Implemented `libreprimus historical-route` for local-only 2012-2017 Cicada route source-locking.

- Used preferred archive path `third_party/CicadaSolversIddqd`.
- Wrote compact committed records under `data/historical-route/` and `data/project-state/`.
- Wrote generated full inventory/report outputs under ignored `experiments/results/historical-route/stage5bf/`.
- Kept raw archive files, generated content packs, and `codex-output` uncommitted.
- Performed no network clone, live scraping, PGP keyserver fetch, stego execution, token experiment, DWH/hash search, CUDA, benchmark, scoring, website publication, or solve claim.

## Validation

- Stage 5BF local build/summary/validate completed with `1043` high-priority artifacts and `0` validation errors.
- Added Stage 5BF schema, guardrail, taxonomy, source-lock candidate, next-stage, CLI, and ignore-policy tests.
- `python -m pytest -q tests/python`: `1973 passed`.
- `python -m ruff check python/libreprimus tests/python`: passed.
- `python -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md`: passed.
- `python -m libreprimus.cli consistency check-doc-staleness --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml --strict`: passed.
- `python -m libreprimus.cli consistency check-state-drift`: passed.
- `python -m libreprimus.cli consistency check-all --allow-warnings`: passed.
- `python -m libreprimus.cli observation-review check-paths --repo-root .`: passed.
- `python -m libreprimus.cli smoke`: passed.
- `scripts/ci/run-parallel-validation.ps1 -Workers 16 -PytestWorkers 16 -PytestMode auto`: passed with xdist.
- `scripts/ci/run-consistency-checks.ps1`: passed, including Stage 5AH stage-ledger coverage with `0` findings.
- `scripts/ci/verify-public-docs-status.ps1`, `verify-lock-hashes.ps1`, `validate-workflow-static.ps1`, `scripts/github/validate-wiki-source.ps1`, and `scripts/github/sync-tutorials-to-wiki.ps1 --DryRun`: passed.
- `scripts/ci/run-consistency-checks.sh` was not run locally because the only available `bash.exe` is WSL and no WSL distribution is installed.
