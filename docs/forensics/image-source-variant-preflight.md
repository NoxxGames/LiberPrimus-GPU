# Image Source-Variant Preflight

Stage 4M records local Liber Primus page-image metadata and source-variant readiness without downloading or comparing external image bytes.

## Scope

The preflight reads ignored local files under `third_party/LiberPrimusPages/` and writes committed metadata summaries under `data/observations/visual/`. It records filename, extension, SHA-256, file size, dimensions, color mode, local lock match, committed artifact record presence, and whether Stage 4E source-delta metadata identifies external LP image categories.

External `cicada-solvers/iddqd` variant image bytes are not downloaded in Stage 4M. When external variants are only known by metadata, records use `source_variant_status=blocked_external_variant_not_cached`.

## Policy

- Raw LP page images stay ignored and uncommitted.
- External variant images stay absent unless a later source-lock stage places them in an ignored cache.
- Source-variant records do not make page images canonical.
- Source-variant records do not enable image-derived experiment seeds.
- Source-variant readiness is preparation for a future controlled comparison, not a visual interpretation.

## CLI

Use:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-preflight build `
  --image-dir third_party/LiberPrimusPages `
  --image-artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
  --compression-observations data/observations/visual/stage4e-image-compression-artifact-observations.yaml `
  --promotion-readiness data/observations/review/stage4l-observation-promotion-readiness-records.yaml `
  --manifest-readiness data/observations/review/stage4l-manifest-readiness-records.yaml `
  --bigram-image data/raw/images/Fib421.jpg `
  --out-dir experiments/results/image-preflight/stage4m `
  --allow-missing-bigram-image `
  --allow-warnings
```

Generated JSONL reports remain ignored under `experiments/results/image-preflight/stage4m/`.
