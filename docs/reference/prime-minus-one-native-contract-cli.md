# Prime-Minus-One Native Contract CLI

The `libreprimus prime-minus-one-native-contract` CLI builds and validates Stage 5W records.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-source-inventory --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-stream-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-prime-schedule --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-candidate-batch-mapping --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-native-parity-preparation --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-result-store-preflight --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-guardrails --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-next-stage-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract validate-stage5w --results-dir experiments/results/prime-minus-one-native-contract/stage5w
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-contract summary
```

## Rules

The commands are no-GPU-safe and raw-data-free. They write committed YAML metadata under `data/cuda/` and ignored JSON reports under `experiments/results/prime-minus-one-native-contract/stage5w/`.
