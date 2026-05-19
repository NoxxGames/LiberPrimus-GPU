# Image Preflight CLI

The `libreprimus image-preflight` group builds and validates Stage 4M image preflight records.

## Build

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
  --source-variant-out data/observations/visual/stage4m-image-source-variant-preflight-records.yaml `
  --compression-out data/observations/visual/stage4m-image-compression-preflight-records.yaml `
  --artifact-candidates-out data/observations/visual/stage4m-image-artifact-review-candidates.yaml `
  --summary-out data/observations/visual/stage4m-image-preflight-summary.yaml `
  --bigram-readiness-out data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml `
  --allow-missing-bigram-image `
  --allow-warnings
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-preflight validate `
  --source-variant data/observations/visual/stage4m-image-source-variant-preflight-records.yaml `
  --compression data/observations/visual/stage4m-image-compression-preflight-records.yaml `
  --artifact-candidates data/observations/visual/stage4m-image-artifact-review-candidates.yaml `
  --summary data/observations/visual/stage4m-image-preflight-summary.yaml `
  --bigram-readiness data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml
```

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-preflight summary `
  --summary data/observations/visual/stage4m-image-preflight-summary.yaml `
  --bigram-readiness data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml
```

The CLI does not execute image transforms, stego extraction, OCR, AI/ML interpretation, or bigram matrix regeneration.
