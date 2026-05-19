# Source Delta Audit CLI

The Stage 4E CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-delta-audit --help
```

## Run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-delta-audit run `
  --repo-url https://github.com/cicada-solvers/iddqd.git `
  --cache-dir third_party/CicadaSolversIddqd `
  --out-dir experiments/results/source-delta/stage4e `
  --source-delta-out data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
  --source-health-out data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml `
  --image-artifact-out data/observations/visual/stage4e-image-compression-artifact-observations.yaml `
  --manifest-out-dir experiments/manifests/stage4e-disabled `
  --allow-network `
  --allow-warnings
```

Network use is explicit through `--allow-network`. If the remote cannot be reached, the command records a deferred audit rather than fabricating source claims.

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-delta-audit validate `
  --source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
  --source-health data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml `
  --image-artifact data/observations/visual/stage4e-image-compression-artifact-observations.yaml `
  --manifest-dir experiments/manifests/stage4e-disabled
```

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-delta-audit summary `
  --source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
  --source-health data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml `
  --image-artifact data/observations/visual/stage4e-image-compression-artifact-observations.yaml `
  --manifest-dir experiments/manifests/stage4e-disabled
```

## Output Policy

Generated reports go under `experiments/results/source-delta/stage4e/` and remain ignored. The local cache under `third_party/CicadaSolversIddqd/` is ignored except for its README and `.gitkeep`.

The CLI commits metadata only. It must keep `raw_file_committed=false`, `binary_committed=false`, `font_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`.
