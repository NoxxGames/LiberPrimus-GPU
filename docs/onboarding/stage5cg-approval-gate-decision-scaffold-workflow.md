# Stage 5CG Approval-Gate Decision Scaffold Workflow

Use this workflow for Stage 5CG post-review approval-gate integration and decision scaffolding.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5cg
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-operator-decision-scaffold
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-deep-research-decision-scaffold
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-combined-approval-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-active-planning-input-decision-scaffold
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-stage5ce-wording-review
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-no-byte-stream-transition-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-no-execution-transition-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cg
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5cg-summary
```

Stage 5CG records are metadata only. The decision records are scaffolds, not approvals; the combined approval gate remains unsatisfied; active planning input remains unauthorized and unselected; String 4 remains inactive and non-canonical; Stage 5BD run-plan IDs remain unchanged; byte-stream generation remains closed; and execution remains closed.

Future Stage 5CH review should cite the Stage 5CG findings integration, decision scaffolds, combined approval-gate scaffold, Stage 5CE proposal/gate preservation records, Stage 5CE wording review, no-byte/no-execution transition gates, Stage 5BD preservation record, active-lineage preservation record, and guardrail.
