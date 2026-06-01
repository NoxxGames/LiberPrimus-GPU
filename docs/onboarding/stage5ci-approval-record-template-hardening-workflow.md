# Stage 5CI Approval-Record Template Hardening Workflow

Stage 5CI hardens future approval and activation-decision templates. It is not an approval, activation, planning-ingestion, or execution stage.

Build and validate:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ci
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci-operator-approval-template
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci-deep-research-acceptance-template
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci-combined-approval-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci-activation-decision-template
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci-negative-validation-contract
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ci
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5ci-summary
```

The focused validators must reject records that misread templates as actual approvals, satisfy the combined gate, authorize byte streams or execution, authorize dry-run ingestion, authorize manifest supersession, use deprecated Stage 5AW paths, use `codex_output`, or claim a solve.

Expected state after a valid build:

- Operator approval template hardened; no operator approval record exists.
- Deep Research acceptance template hardened; no acceptance record exists.
- Combined approval gate validation hardened; the gate is unsatisfied.
- Activation-decision template hardened; no active planning input is selected or authorized.
- Stage 5BD run-plan IDs remain unchanged.
- No-byte-stream and no-execution gates remain closed.
- Generated diagnostics stay under `experiments/results/token-block/stage5ci/` and remain ignored.
- Local Codex completion summary uses `codex-output/stage5ci-codex-completion.md`; `codex_output/` must not be used.

Next stage: completed by Stage 5CJ review, Stage 5CK fixture-pack follow-up, Stage 5CL review, Stage 5CM readiness-boundary hardening, Stage 5CN review, and Stage 5CO transition packaging; current routing is Stage 5CP Deep Research review before any actual approval-record or activation-capable stage.
