# OutGuess Regression CLI

Detect OutGuess:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-detect `
  --out-dir experiments/results/stego/outguess/stage3v `
  --allow-missing-tool
```

Validate the manifest and artefact records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-validate-manifest `
  --manifest experiments/manifests/stego/outguess-regression-v1.yaml `
  --artifacts data/observations/stego/outguess-artifacts-v0.yaml
```

Run the explicit regression cases:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-run `
  --manifest experiments/manifests/stego/outguess-regression-v1.yaml `
  --artifacts data/observations/stego/outguess-artifacts-v0.yaml `
  --out-dir experiments/results/stego/outguess/stage3v `
  --allow-missing-tool `
  --allow-missing-assets `
  --allow-warnings
```

Print the summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-summary `
  --results-dir experiments/results/stego/outguess/stage3v
```

`--outguess-path` can point at a specific local executable. The CLI does not install OutGuess, download fixtures, run CUDA, or scan unlisted images.
