# Stage 5CA Inactive-Sidecar Review Contract Workflow

Use this workflow for Stage 5CA inactive sidecar review-contract hardening.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ca
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ca-citation-contract
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ca-fail-closed-triggers
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ca-activation-preconditions
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ca-manifest-supersession-contract
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ca-sidecar-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ca
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5ca-summary
```

Stage 5CA records are review-contract metadata only. The sidecar remains inactive, non-canonical, not active input, not dry-run ingested, not byte-stream generated, and not execution-capable.

Future stages must cite the Stage 5CA exact citation contract, fail-closed trigger contract, activation-precondition contract, manifest-supersession preflight contract, Stage 5BD preservation record, active-lineage preservation record, no-active-ingestion proof, and no-byte-stream proof before proposing any sidecar transition.
