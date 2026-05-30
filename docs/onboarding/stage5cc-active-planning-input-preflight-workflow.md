# Stage 5CC Active-Planning-Input Preflight Workflow

Use this workflow for Stage 5CC inactive-sidecar active-planning-input proposal preflight metadata.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5cc
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-citation-contract
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-fail-closed-triggers
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-activation-preconditions
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-active-planning-input-preflight
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-no-byte-stream-transition-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-no-execution-transition-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cc
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5cc-summary
```

Stage 5CC records are transition-preflight metadata only. The active-planning input is not selected or authorized, String 4 remains inactive and non-canonical, Stage 5BD run-plan IDs remain unchanged, byte-stream generation remains closed, and execution remains closed.

Future stages must cite the Stage 5CC citation-preservation record, fail-closed trigger exact-set contract, activation-precondition exact-set contract, active-planning-input preflight, no-byte-stream transition gate, no-execution transition gate, Stage 5BD preservation record, active-lineage preservation record, and guardrail before proposing any sidecar transition.
