# Gematria CUDA Result-Store CLI

Stage 5P adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store build-result-store-integration --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store build-score-summary-integration --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store build-method-status-impact --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store build-generated-body-policy --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store build-controlled-expansion-candidates --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store validate-stage5p
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store summary
```

The commands are metadata-only. They read committed YAML records, write committed compact YAML
summaries, and write ignored JSON reports. They do not run CUDA.
