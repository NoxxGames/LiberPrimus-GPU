# Stage 5BY Inactive-Sidecar Planning Manifest Workflow

Use this workflow for the Stage 5BY inactive planning-sidecar scaffold.

Required commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5by
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5by-source-digest-uniqueness
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5by-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5by
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5by-summary
```

Stage 5BY records are planning metadata only. The sidecar is inactive, non-canonical, not active input, not dry-run ingested, and not execution-capable.

Reviewers should check the Stage 5BW duplicate source-digest classification, the record-family equivalence map, the inactive scaffold, the no-execution sidecar, the Stage 5BD run-plan preservation record, and the guardrail record before any future planning-ingestion stage is considered.
