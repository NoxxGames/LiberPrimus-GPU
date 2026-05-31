# Stage 5CK Approval-Record Fixture Pack Workflow

Stage 5CK packages synthetic approval and activation validation fixtures. It is not an approval, acceptance, activation, planning-ingestion, byte-stream, or execution stage.

Build and validate:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ck
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck-operator-fixtures
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck-deep-research-fixtures
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck-activation-decision-fixtures
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck-negative-validation-matrix
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck-review-package
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ck
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5ck-summary
```

Expected state after a valid build:

- Fixture packs exist and are explicitly fixture-only.
- Fixture records are rejected as actual approval, acceptance, or activation records.
- No actual operator approval record exists.
- No actual Deep Research acceptance record exists.
- No activation decision is valid now.
- The combined approval gate remains unsatisfied.
- Active-planning input is not selected or authorized.
- Stage 5BD run-plan IDs remain unchanged.
- No-byte-stream and no-execution gates remain closed.
- Generated diagnostics stay under `experiments/results/token-block/stage5ck/` and remain ignored.
- Local Codex completion summary uses `codex-output/stage5ck-codex-completion.md`; `codex_output/` must not be used.

Next stage: completed by Stage 5CL review and Stage 5CM readiness-boundary hardening; current routing is Stage 5CN Deep Research review before any actual approval-record or activation-capable stage.
