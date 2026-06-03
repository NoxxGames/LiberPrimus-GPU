# Stage 5CY Option-Selection Decision Preflight Workflow

Use this workflow when reviewing or maintaining Stage 5CY records.

1. Build the compact metadata:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5cy
```

2. Run the focused validators:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-stage5cx-findings
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-real-decision-preflight-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-operator-option-selection-preflight
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-option-selection-requirements
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-option-selection-misuse
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-options-nonselection
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-validation-count-reconciliation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-real-record-blocker
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-combined-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-activation-nonauthorization
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-stage5cw-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-stage5cu-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-stage5cs-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-stage5bd-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-active-lineage-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-handoff-continuity
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-credential-redaction-policy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy-governance-scope-control
```

3. Run the aggregate validator and summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5cy-summary
```

Treat every Stage 5CY record as review-only preflight metadata. A future real decision stage must still create an explicit real record, select exactly one Stage 5CS option, cite Stage 5CW count reconciliation, preserve Stage 5BD and active lineage or record a reviewed supersession, and pass real-record validation gates. Stage 5CY itself authorizes no active input, byte stream, execution, approval, activation, scoring, CUDA, benchmark, website expansion, method-status upgrade, or solve claim.

After Stage 5CZ review, the project should force an explicit operator choice or explicitly pause further governance expansion unless Stage 5CZ finds a concrete defect.
