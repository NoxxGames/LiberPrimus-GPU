# Gematria Expanded CUDA Result-Store CLI

Stage 5S adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-parity-report --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-result-store-integration --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-score-summary-integration --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-method-status-impact --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-generated-body-policy --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-boundary-review --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-next-step-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store build-summary --allow-warnings
```

Validate the committed Stage 5S records with:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store validate-stage5s `
  --parity-report data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml `
  --result-store-integration data/cuda/stage5s-gematria-expanded-cuda-result-store-integration.yaml `
  --score-summary-integration data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml `
  --method-status-impact data/cuda/stage5s-gematria-expanded-cuda-method-status-impact.yaml `
  --generated-body-policy data/cuda/stage5s-gematria-expanded-cuda-generated-body-policy.yaml `
  --boundary-review data/cuda/stage5s-gematria-expanded-cuda-boundary-review.yaml `
  --next-step-decision data/cuda/stage5s-gematria-expanded-cuda-next-step-decision.yaml `
  --summary data/cuda/stage5s-expanded-cuda-result-store-integration-summary.yaml `
  --results-dir experiments/results/gematria-expanded-cuda-result-store/stage5s
```

The CLI is raw-data-free and no-GPU-safe. It reads committed Stage 5R/Stage 4I/Stage 4P metadata and writes compact YAML records plus ignored JSON reports. It has no CUDA execution path.
