# Bounded P56 Mismatch CLI

Stage 5AD-fix adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-hash-lineage --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-token-trace --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-stream-trace --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-formula-trace --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-hash-material-trace --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-reference-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-root-cause --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-repair-readiness --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-guardrails --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-next-stage-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch validate-stage5ad-fix
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-mismatch summary
```

The commands read committed metadata and write ignored diagnostic JSON plus compact committed YAML. They do not execute CUDA or read raw corpus data.
