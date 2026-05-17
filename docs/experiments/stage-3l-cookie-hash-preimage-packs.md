# Stage 3L Cookie Hash Preimage Packs

Stage 3L runs a bounded CPU-only SHA-256 preimage check against the two archived cookie/hash artefacts recorded in Stage 3K.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli hash-preimage validate-packs `
  --pack-dir data/observations/web/hash-preimage-candidate-packs

.\.venv\Scripts\python.exe -m libreprimus.cli hash-preimage run `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --pack-dir data/observations/web/hash-preimage-candidate-packs `
  --out-dir experiments/results/hash-preimage/stage3l `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli hash-preimage summary `
  --results-dir experiments/results/hash-preimage/stage3l
```

The run tested `1809` deduplicated candidate byte strings against `2` cookie targets for `3618` comparisons. It found `0` exact SHA-256 matches.

Generated outputs remain ignored under `experiments/results/hash-preimage/stage3l/`. No solve claim is made.
