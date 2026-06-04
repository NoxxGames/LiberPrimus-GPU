# Stage 5DG Real Operator Approval Record Workflow

Use this workflow when reviewing or rebuilding the Stage 5DG metadata package.

## Build

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5dg
```

## Focused Validators

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-stage5df-findings
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-real-operator-approval-record
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-operator-approval-scope
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-operator-approval-nonactivation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-stage5de-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-stage5dc-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-selected-option-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-unselected-options-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-real-record-boundary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-deep-research-absence
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-combined-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-activation-nonauthorization
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-stage5bd-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-active-lineage-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-target-context
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-handoff-continuity
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-credential-redaction-policy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg-governance-scope
```

## Aggregate Validation

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dg
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dg-summary
```

## Boundary

Stage 5DG creates exactly one valid real operator approval record. Operator approval alone does not satisfy the combined gate and does not authorize Deep Research acceptance, activation, active input, byte streams, execution, target validation, Tor/network access, CUDA, or solve claims.
