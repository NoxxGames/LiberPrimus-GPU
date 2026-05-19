# Stego Positive-Control CLI

Stage 4N adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-positive-controls build `
  --out-dir experiments/results/stego-positive-controls/stage4n `
  --cache-dir third_party/StegoPositiveControls `
  --outguess-readiness-out data/observations/stego/stage4n-outguess-positive-control-readiness.yaml `
  --audio-readiness-out data/observations/stego/stage4n-audio-positive-control-readiness.yaml `
  --fixture-cache-out data/observations/stego/stage4n-fixture-cache-records.yaml `
  --expected-output-out data/observations/stego/stage4n-expected-output-records.yaml `
  --toolchain-out data/observations/stego/stage4n-toolchain-readiness.yaml `
  --summary-out data/observations/stego/stage4n-positive-control-summary.yaml `
  --allow-warnings
```

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-positive-controls validate `
  --outguess-readiness data/observations/stego/stage4n-outguess-positive-control-readiness.yaml `
  --audio-readiness data/observations/stego/stage4n-audio-positive-control-readiness.yaml `
  --fixture-cache data/observations/stego/stage4n-fixture-cache-records.yaml `
  --expected-output data/observations/stego/stage4n-expected-output-records.yaml `
  --toolchain data/observations/stego/stage4n-toolchain-readiness.yaml `
  --summary data/observations/stego/stage4n-positive-control-summary.yaml
```

The build command does not fetch by default and does not execute stego/audio tools. Generated reports remain ignored under `experiments/results/stego-positive-controls/stage4n/`; local fixture bytes remain ignored under `third_party/StegoPositiveControls/`.
