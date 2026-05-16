# CPU Experiment Execution CLI

## validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml
```

## plan

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli execution plan --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml --out-dir experiments/results/cpu-execution/stage2f --allow-warnings
```

## run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli execution run --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml --out-dir experiments/results/cpu-execution/stage2f --allow-warnings
```

## stage2f-run-all

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli execution stage2f-run-all --manifest-dir experiments/manifests/cpu-execution --out-dir experiments/results/cpu-execution/stage2f --allow-warnings
```

## summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli execution summary --results-dir experiments/results/cpu-execution/stage2f
```

## Troubleshooting

If a manifest fails validation, check the safety flags, corpus slice kind, transform ID, and output directory. The blocked unsolved negative manifest is expected to fail.
