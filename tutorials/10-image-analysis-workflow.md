# Image Analysis Workflow

## Purpose

Run deterministic local page-image analysis without OCR, AI/ML, or image-derived cipher execution.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-analysis analyze-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-analysis/stage3m `
  --allow-missing `
  --allow-warnings
```

## Expected Outputs

Generated JSONL records summarize grayscale stats, thresholds, components, symmetry, bitplanes, and
review-only feature flags.

## What Not To Commit

Raw images and generated image-analysis JSONL outputs.

## Troubleshooting

If local images are absent, `--allow-missing` supports raw-data-free validation.
