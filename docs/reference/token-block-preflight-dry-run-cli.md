# Token-Block Preflight Dry-Run CLI

Stage 5BD commands are under `libreprimus token-block`.

Build order:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-dry-run-policy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-active-manifest-lock
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-dry-run-plan
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-future-result-path-validation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-plan-counters
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-fixture-dry-run-records
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bd-execution-gates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-validation-evidence
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-archive-marker
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bd-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bd
```

The commands write compact committed metadata and ignored JSON reports. They do not generate real token bytes, materialise variants, enumerate the full branch space, run DWH/hash searches, decode, score, run CUDA, or benchmark.
