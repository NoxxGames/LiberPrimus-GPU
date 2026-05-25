# Token-Block CLI

Stage 5AP adds `libreprimus token-block` for metadata-only source-lock and preflight records.

Core commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-source-lock --search-roots third_party --search-roots research-inputs --search-roots website-export --search-roots data
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-transcription
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-alphabet-registry
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-mapping-preflight
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-null-control-plan
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-dwh-context
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ap
```

Generated reports are written under `experiments/results/token-block/stage5ap/` and remain ignored. The CLI must not perform OCR, image interpretation, decoding, hash/preimage search, CUDA execution, benchmark work, or hypothesis execution.
