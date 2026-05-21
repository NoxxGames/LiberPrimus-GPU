# Gematria Solved-Fixture Mapping CLI

The Stage 5L command group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping --help
```

Build commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping build-token-mapping --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping build-native-parity --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping build-output-hash-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping build-score-summary-shape --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping build-summary --allow-warnings
```

Validation command:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping validate-stage5l `
  --token-mapping data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml `
  --native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml `
  --output-hash-contract data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml `
  --score-summary-shape data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml `
  --summary data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-mapping/stage5l
```

The CLI is raw-data-free and no-GPU-safe. It writes generated JSON reports under ignored paths and
committed aggregate YAML records under `data/cuda/`.
