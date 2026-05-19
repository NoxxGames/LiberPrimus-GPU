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

Stage 4C adds a separate visual-annotation workflow for cuneiform, delimiter, dot-pattern, and
visual negative-control review tasks:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli visual-annotation build `
  --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
  --image-artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --image-dir third_party/LiberPrimusPages `
  --out-dir experiments/results/visual-annotation/stage4c `
  --allow-warnings
```

The generated Stage 4C site and templates are local review aids. They do not infer cuneiform or dot
meaning and do not make visual observations usable as experiment seeds.

Stage 4D confirms this boundary in the numeric verifier path: cuneiform seed execution remains
deferred without accepted coordinates/readout, and delimiter/dot outputs are metadata or ambiguity
audits only.

Stage 4E adds only a source-variant and compression-artefact preflight backlog. It does not run image
transforms. JPEG-like artefacts, star-like shapes, and compression/noise features remain review
candidates until a future deterministic audit locks source variants and applies controls.

## What Not To Commit

Raw images, generated image-analysis JSONL outputs, generated transform images, contact sheets,
review HTML, and transform JSONL records.

Generated Stage 4C annotation-site pages, copied review images, grid overlays, and blank coordinate
templates under `experiments/results/visual-annotation/stage4c/` are also generated outputs.

Generated Stage 4D bounded numeric verifier JSON/JSONL outputs under
`experiments/results/bounded-numeric/stage4d/` are also generated outputs.

Generated Stage 4E source-delta reports under `experiments/results/source-delta/stage4e/` and any
ignored `third_party/CicadaSolversIddqd/` raw cache contents are also not committed.

## OutGuess Regression Boundary

Stage 3V adds OutGuess regression under `libreprimus stego`, but it is not part of the image-analysis transform workflow. It uses explicit stego manifests and optional local historical fixtures only. Do not run broad OutGuess scans across `third_party/LiberPrimusPages/`; those images remain ignored and outside Stage 3V unless a future manifest lists a tiny reviewed control subset.

## Troubleshooting

If local images are absent, `--allow-missing` supports raw-data-free validation.

If transform generation is slow on high-resolution images, keep the Stage 3P bounded preview
settings rather than producing full-resolution derived artefacts. Original image identity is still
tracked by Stage 3K locks.
