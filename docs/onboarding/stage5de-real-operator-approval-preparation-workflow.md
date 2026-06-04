# Stage 5DE Real Operator Approval Preparation Workflow

Use this workflow when reviewing or rebuilding the Stage 5DE metadata package.

## Build

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5de
```

## Focused Validators

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-stage5dd-findings
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-review-label-anomaly
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-real-operator-approval-preparation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-future-operator-approval-requirements
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-stage5dc-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-real-approval-noncreation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-combined-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-activation-nonauthorization
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-real-record-boundary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-stage5bd-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-active-lineage-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-handoff-continuity
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-credential-redaction-policy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de-governance-scope
```

## Aggregate Validation

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5de
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5de-summary
```

## Review Boundary

Stage 5DE is preparation only. A future Stage 5DG-style prompt would still need to explicitly create a real operator approval record, and that approval alone still would not authorize activation, active input, byte streams, execution, target validation, Tor access, CUDA, or solve claims.
