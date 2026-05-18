# Stage 3U Cookie Signed-Variant Pack

Stage 3U executes only `EXP-3R-001`, the cookie SHA-256 signed-variant manifest created in Stage 3R.

This is a bounded CPU exact-match check over manifest-declared signed/public strings and byte variants. It is not hash cracking, hashcat, dictionary search, CUDA, live Tor, Discord raw-log processing, image processing, or solve evidence.

## Inputs

- Manifest: `experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml`
- Cookie records: `data/observations/web/cookie-hash-records-v0.yaml`
- Targets:
  - `cookie-2013-167-v0`
  - `cookie-2013-761-v0`
- Algorithm: `sha256`
- Encoding: `utf-8`

## Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-cookie-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-cookie-signed-variants `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/post-discord/stage3u `
  --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord cookie-signed-summary `
  --results-dir experiments/results/post-discord/stage3u
```

## Result

The local Stage 3U run generated `156` candidates before deduplication and `105` deduplicated byte strings. It made `210` exact target comparisons and found `0` exact SHA-256 matches.

Generated candidate JSONL, exact-match JSONL, summary JSON, and warnings remain ignored under `experiments/results/post-discord/stage3u/`.

No fuzzy matching, partial matching, alternate hash algorithm, GPU/hashcat, external dictionary, live Tor, raw Discord processing, image processing, or solve claim is made.
