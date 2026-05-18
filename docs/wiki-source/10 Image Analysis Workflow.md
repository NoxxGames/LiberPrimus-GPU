> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Image Analysis Workflow

## Purpose

Run deterministic local page-image analysis without OCR, AI/ML, or image-derived cipher execution.

## Commands

Stage 3M feature analysis:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-analysis analyze-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-analysis/stage3m `
  --allow-missing `
  --allow-warnings
```

Stage 3P transform review artefacts:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-transform run-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-transforms/stage3p `
  --allow-missing `
  --allow-warnings
```

## Expected Outputs

Generated JSONL records summarize grayscale stats, thresholds, components, symmetry, bitplanes, and
review-only feature flags. Stage 3P also writes derived review images, per-image contact sheets,
a global contact sheet, per-image review pages, and:

```text
experiments/results/image-transforms/stage3p/review_index.html
```

## What Not To Commit

Raw images, generated image-analysis JSONL outputs, generated transform images, contact sheets,
review HTML, and transform JSONL records.

## OutGuess Regression Boundary

Stage 3V adds OutGuess regression under `libreprimus stego`, but it is not part of the image-analysis transform workflow. It uses explicit stego manifests and optional local historical fixtures only. Do not run broad OutGuess scans across `third_party/LiberPrimusPages/`; those images remain ignored and outside Stage 3V unless a future manifest lists a tiny reviewed control subset.

## Troubleshooting

If local images are absent, `--allow-missing` supports raw-data-free validation.

If transform generation is slow on high-resolution images, keep the Stage 3P bounded preview
settings rather than producing full-resolution derived artefacts. Original image identity is still
tracked by Stage 3K locks.
