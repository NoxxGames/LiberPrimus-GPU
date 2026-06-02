# Stage 5CU Option Negative-Fixture Hardening

Stage 5CU started from commit `f32cd0390565af7fc63760962f7e644a53751d30` on `main`, matching `origin/main`. The verified remote was `https://github.com/NoxxGames/LiberPrimus-GPU.git`; no credential-bearing remote was detected.

Implemented:

- Added `python/libreprimus/token_block/stage5cu.py` with Stage 5CT findings integration, Stage 5CS option preservation, decision-option negative fixtures, real-decision negative fixtures, option-selection misuse validation, real-record blockers, no-active/no-byte/no-execution gates, Stage 5BD preservation, active-lineage preservation, handoff continuity, credential-redaction preservation, and Stage 5CV next-stage routing.
- Added Stage 5CU `token-block` CLI commands for build, focused validation, aggregate validation, and summary display.
- Generated committed Stage 5CU records under `data/project-state/`, `data/token-block/`, `data/source-harvester/`, and `data/historical-route/`, with matching schemas.
- Added focused Stage 5CU tests and current/next-stage source-of-truth test updates.
- Updated CI consistency scripts to validate Stage 5CU records and generated-output ignore policy.
- Updated current-state docs, onboarding docs, staged plan, source-of-truth records, and research summary.

Guardrails preserved:

- Operator decision option count remains `6`; selected option ID remains null.
- Negative fixture count is `41`; option-selection misuse row count is `13`.
- Real decision negative fixture target classes count is `10`.
- Real operator decision, real approval, Deep Research acceptance, combined gate, activation, active planning input, byte streams, execution, scoring, CUDA, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, and solve claim remain false.
- Stage 5BD run-plan ID count remains `10`.
- Active-lineage record count remains `8`.
- Stage 5CM-and-later local validation cap remains `8` workers.
- `codex-output/` is the only Codex handoff root; `codex_output/` remains unused.

Validation completed locally:

- Focused Stage 5CU build, validators, aggregate validation, and summary: passed.
- `ruff check python/libreprimus tests/python`: passed.
- `pytest -q tests/python`: `2446 passed`.
- `run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto`: passed with xdist and `failed_command_count=0`.
- `run-consistency-checks.ps1`: passed, including Stage 5AH stage-ledger/current-next coverage with zero findings.
- `run-consistency-checks.sh` via Git Bash with `PYTHON=.venv/Scripts/python.exe`: passed.
- Public-docs status, lock-hash validation, workflow static validation, wiki-source validation, and wiki dry-run sync: passed.

Implementation note: Stage 5CU tests exposed a Windows/xdist race where a test worker could read a Stage 5CU YAML record while another worker rebuilt it. The shared token-block YAML/JSON/JSONL write helpers now use a temp file plus atomic replace with a short Windows retry loop, keeping readers from seeing partial metadata files.

GitHub issue: `#137` (`Stage 5CU: operator-decision option negative-fixture hardening`).

Commit, push, and CI verification will be recorded after remote validation.
