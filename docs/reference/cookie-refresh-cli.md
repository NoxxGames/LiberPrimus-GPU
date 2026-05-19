# Cookie Refresh CLI

The Stage 4G CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cookie-refresh --help
```

Run the source-backed exact refresh:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cookie-refresh run `
  --manifest experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml `
  --candidate-sources data/observations/web/stage4b-cookie-candidate-source-records.yaml `
  --cookie-targets data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/cookie-refresh/stage4g `
  --summary-out data/observations/web/stage4g-cookie-refresh-summary.yaml `
  --allow-warnings
```

Validate outputs:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cookie-refresh validate `
  --results-dir experiments/results/cookie-refresh/stage4g `
  --summary data/observations/web/stage4g-cookie-refresh-summary.yaml
```

Print the committed aggregate:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cookie-refresh summary `
  --summary data/observations/web/stage4g-cookie-refresh-summary.yaml
```

The CLI enforces exact-match-only policy, manifest-declared byte variants and algorithms, SHA-256 by
default, cap checking, `no_solve_claim=true`, `cuda_used=false`, and `hashcat_used=false`.
