# Stego-Controls CLI

Stage 5AP adds `libreprimus stego-controls` for OutGuess positive-control readiness records. It is not an OutGuess execution interface.

Core commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-controls build-stage5ap-outguess-toolchain-readiness
.\.venv\Scripts\python.exe -m libreprimus.cli stego-controls build-stage5ap-outguess-positive-control-matrix
.\.venv\Scripts\python.exe -m libreprimus.cli stego-controls build-stage5ap-outguess-historical-fixture-readiness
.\.venv\Scripts\python.exe -m libreprimus.cli stego-controls build-stage5ap-outguess-guardrail
.\.venv\Scripts\python.exe -m libreprimus.cli stego-controls validate-stage5ap-outguess
```

Generated reports are written under `experiments/results/stego-controls/stage5ap/` and remain ignored. Historical stego fixtures remain blocked until assets, expected outputs, and tools are source-locked by a later explicit stage.
