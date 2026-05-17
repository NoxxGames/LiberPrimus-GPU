# Hash Preimage CLI

Validate candidate packs:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli hash-preimage validate-packs `
  --pack-dir data/observations/web/hash-preimage-candidate-packs
```

Run the bounded exact-match experiment:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli hash-preimage run `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --pack-dir data/observations/web/hash-preimage-candidate-packs `
  --out-dir experiments/results/hash-preimage/stage3l `
  --allow-warnings
```

Print the generated summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli hash-preimage summary `
  --results-dir experiments/results/hash-preimage/stage3l
```

The command uses SHA-256 only, logs exact byte-string candidates, and performs exact digest comparison only. Generated outputs are ignored.
