# Cookie Signed-Variant Pack CLI

Stage 3U extends the `post-discord` CLI group for `EXP-3R-001`.

## Validate Manifest

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-cookie-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml
```

This checks the manifest is SHA-256-only, bounded by cap `576`, GPU/hashcat/fuzzy matching disabled, and no-solve.

## Run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-cookie-signed-variants `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/post-discord/stage3u `
  --allow-warnings
```

The command executes only `EXP-3R-001`. It writes ignored outputs:

- `hash_candidate_records.jsonl`
- `exact_matches.jsonl`
- `summary.json`
- `warnings.jsonl` when deduplication or other non-fatal warnings occur

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord cookie-signed-summary `
  --results-dir experiments/results/post-discord/stage3u
```

The summary prints counts only. Generated candidate records remain local ignored outputs.
