# Stage 3T GP/Rune Claim Verifier

Stage 3T executes only `EXP-3R-004`, the GP/rune claim verifier manifest created in Stage 3R.

This is a bounded CPU verification task. It recomputes exact claims against committed profiles and review records. It does not search neighbouring spans, process raw Discord logs, process raw page images, use CUDA, activate canonical corpus, finalize page boundaries, or claim a solve.

## Scope

- Manifest: `experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml`
- Claim cap: `64`
- Inputs: Stage 3R promoted observation records, Stage 3K visual numeric observations, Gematria Primus profile
- Outputs: ignored JSON/JSONL verification files under `experiments/results/post-discord/stage3t/`

## Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-gp-rune-verifier `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --visual-observations data/observations/visual/visual-numeric-observations-v0.yaml `
  --out-dir experiments/results/post-discord/stage3t `
  --allow-warnings
```

## Status Classes

- `verified`
- `unverified`
- `boundary_sensitive`
- `missing_source_span`
- `unsupported_claim_type`
- `duplicate_claim`
- `malformed_claim`

Missing exact spans remain missing. The verifier does not run off-by-one checks or fuzzy span searches.

## Stage 3T Result

The local Stage 3T run loaded `25` claims and deduplicated `25`. It classified `23` as verified and `2` as unsupported. No claims were unverified, boundary-sensitive, missing-source-span, malformed, or duplicate in this committed input set.

No solve claim is made.
