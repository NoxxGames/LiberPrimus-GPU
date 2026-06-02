# Stage 5CW Real-Decision Package Preflight Workflow

Use this workflow when reviewing or maintaining Stage 5CW records.

1. Build the compact metadata:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5cw
```

2. Run the focused validators:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-stage5cv-findings
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-real-decision-package-preflight
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-future-real-decision-requirements
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-preflight-misuse
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-stage5cu-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-stage5cs-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-options-nonselection
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-real-record-blocker
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-combined-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-activation-nonauthorization
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-stage5bd-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-active-lineage-preservation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-handoff-continuity
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw-credential-redaction-policy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cw
```

3. Inspect the summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5cw-summary
```

Treat every Stage 5CW record as review-only preflight metadata. A future real decision stage must still create an explicit real record, select exactly one Stage 5CS option, preserve Stage 5BD/active lineage or record a reviewed supersession, and pass the real-record validation gates. Stage 5CW itself authorizes no active input, byte stream, execution, approval, activation, scoring, CUDA, benchmark, website expansion, method-status upgrade, or solve claim.
