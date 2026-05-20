# Benchmark Planning CLI

The Stage 4Q CLI group is `libreprimus benchmark-planning`.

Commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli benchmark-planning environment `
  --manifest experiments/manifests/benchmarks/stage4q-benchmark-environment.yaml `
  --out-dir experiments/results/benchmarks/stage4q `
  --allow-warnings
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli benchmark-planning cpu-smoke `
  --manifest experiments/manifests/benchmarks/stage4q-cpu-benchmark-smoke.yaml `
  --out-dir experiments/results/benchmarks/stage4q `
  --allow-warnings
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli benchmark-planning build-plan `
  --manifest experiments/manifests/benchmarks/stage4q-cuda-parity-readiness.yaml `
  --plan-out data/benchmarks/stage4q-cpu-benchmark-plan.yaml `
  --readiness-out data/benchmarks/stage4q-cuda-parity-readiness.yaml `
  --summary-out data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml `
  --out-dir experiments/results/benchmarks/stage4q `
  --allow-warnings
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli benchmark-planning validate-stage4q `
  --results-dir experiments/results/benchmarks/stage4q `
  --plan data/benchmarks/stage4q-cpu-benchmark-plan.yaml `
  --readiness data/benchmarks/stage4q-cuda-parity-readiness.yaml `
  --summary data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml
```

The commands are raw-data-free. Generated JSON and JSONL diagnostics remain ignored. CPU smoke timing fields are diagnostics only and must not be used as performance claims.
