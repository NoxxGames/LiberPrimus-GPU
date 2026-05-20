# Stage 5D Native C++ CPU Batch Threading

Stage 5D is infrastructure, not a new cryptanalytic experiment.

It builds and validates a native C++ CPU backend against a synthetic fixture, checks deterministic
threading parity across multiple thread counts, and compares native output to a Python reference
implementation. It does not use raw corpus material, execute broad searches, run CUDA transforms, or
make solve or performance claims.

## Outputs

Committed:

- `data/native-cpu/stage5d-native-cpu-backend-capabilities.yaml`
- `data/native-cpu/stage5d-native-cpu-threading-records.yaml`
- `data/native-cpu/stage5d-native-cpu-parity-records.yaml`
- `data/native-cpu/stage5d-native-cpu-diagnostic-records.yaml`
- `data/native-cpu/stage5d-native-cpu-summary.yaml`

Ignored:

- `experiments/results/native-cpu/stage5d/native_backend_capabilities.json`
- `experiments/results/native-cpu/stage5d/threading_parity_report.json`
- `experiments/results/native-cpu/stage5d/native_python_parity_report.json`
- `experiments/results/native-cpu/stage5d/native_cpu_diagnostics.json`
- `experiments/results/native-cpu/stage5d/summary.json`
- `experiments/results/native-cpu/stage5d/warnings.jsonl`

## Stop Conditions

Stop if native CPU work would require raw inputs, generated output publication, CUDA source changes,
GPU benchmarking, speedup claims, C++ launching Python worker scripts, website expansion, canonical
corpus activation, page-boundary finalisation, or solve claims.
