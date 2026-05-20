# Native CPU Backend CLI

Stage 5D adds the `libreprimus native-cpu` command group.

## Commands

Run the native smoke path:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli native-cpu run-smoke `
  --native-executable build/stage5d-native-cpu/src/native_cpu/Debug/lpgpu_native_cpu_backend_cli.exe `
  --manifest experiments/manifests/native-cpu/stage5d-native-cpu-smoke.yaml `
  --out-dir experiments/results/native-cpu/stage5d `
  --capabilities-out data/native-cpu/stage5d-native-cpu-backend-capabilities.yaml `
  --diagnostics-out data/native-cpu/stage5d-native-cpu-diagnostic-records.yaml `
  --allow-warnings
```

Check threading parity:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli native-cpu check-threading-parity `
  --native-executable build/stage5d-native-cpu/src/native_cpu/Debug/lpgpu_native_cpu_backend_cli.exe `
  --manifest experiments/manifests/native-cpu/stage5d-native-cpu-threading-parity.yaml `
  --out-dir experiments/results/native-cpu/stage5d `
  --threading-out data/native-cpu/stage5d-native-cpu-threading-records.yaml `
  --thread-counts 1,2,4,8,16 `
  --allow-warnings
```

Check native/Python parity:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli native-cpu check-python-parity `
  --native-executable build/stage5d-native-cpu/src/native_cpu/Debug/lpgpu_native_cpu_backend_cli.exe `
  --manifest experiments/manifests/native-cpu/stage5d-native-python-parity.yaml `
  --out-dir experiments/results/native-cpu/stage5d `
  --parity-out data/native-cpu/stage5d-native-cpu-parity-records.yaml `
  --allow-warnings
```

Validate committed records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli native-cpu validate-stage5d `
  --capabilities data/native-cpu/stage5d-native-cpu-backend-capabilities.yaml `
  --threading data/native-cpu/stage5d-native-cpu-threading-records.yaml `
  --parity data/native-cpu/stage5d-native-cpu-parity-records.yaml `
  --diagnostics data/native-cpu/stage5d-native-cpu-diagnostic-records.yaml `
  --summary data/native-cpu/stage5d-native-cpu-summary.yaml `
  --results-dir experiments/results/native-cpu/stage5d
```

The CLI does not execute CUDA, broad experiments, or raw-data processing. Generated JSON reports
remain ignored.
