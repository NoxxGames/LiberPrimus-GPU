# Stego Fixture Source-Lock CLI

The Stage 4F CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-fixtures --help
```

## Build

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-fixtures build `
  --stage4e-source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
  --stage4e-source-health data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml `
  --stage4b-sources data/observations/archive/stage4b-promoted-source-records.yaml `
  --out-dir experiments/results/stego-fixtures/stage4f `
  --outguess-fixtures-out data/observations/stego/stage4f-outguess-fixture-source-records.yaml `
  --audio-fixtures-out data/observations/stego/stage4f-audio-fixture-source-records.yaml `
  --source-health-out data/locks/third-party/stage4f-stego-fixture-source-health.yaml `
  --toolchain-out data/observations/stego/stage4f-toolchain-requirements.yaml `
  --manifest-out-dir experiments/manifests/stego/stage4f-disabled `
  --allow-warnings
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-fixtures validate `
  --outguess-fixtures data/observations/stego/stage4f-outguess-fixture-source-records.yaml `
  --audio-fixtures data/observations/stego/stage4f-audio-fixture-source-records.yaml `
  --source-health data/locks/third-party/stage4f-stego-fixture-source-health.yaml `
  --toolchain data/observations/stego/stage4f-toolchain-requirements.yaml `
  --manifest-dir experiments/manifests/stego/stage4f-disabled
```

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-fixtures summary `
  --outguess-fixtures data/observations/stego/stage4f-outguess-fixture-source-records.yaml `
  --audio-fixtures data/observations/stego/stage4f-audio-fixture-source-records.yaml `
  --source-health data/locks/third-party/stage4f-stego-fixture-source-health.yaml `
  --toolchain data/observations/stego/stage4f-toolchain-requirements.yaml `
  --manifest-dir experiments/manifests/stego/stage4f-disabled
```

Generated reports are ignored under `experiments/results/stego-fixtures/stage4f/`.
