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

Stage 4M implements the first deterministic preflight for that backlog:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-preflight validate `
  --source-variant data/observations/visual/stage4m-image-source-variant-preflight-records.yaml `
  --compression data/observations/visual/stage4m-image-compression-preflight-records.yaml `
  --artifact-candidates data/observations/visual/stage4m-image-artifact-review-candidates.yaml `
  --summary data/observations/visual/stage4m-image-preflight-summary.yaml `
  --bigram-readiness data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml
```

The Stage 4M records are metric-only. They do not infer hidden data, run OCR/AI/ML, regenerate a
bigram matrix, or promote image artefacts to experiment seeds.

Stage 5I Gematria CUDA preparation is outside the image workflow. Image artefact, star-like,
compression, and bigram/Fibonacci observations must remain review/preflight records and must not be
used as CUDA inputs or kernel targets.

Stage 4J adds the review workflow that blocks visual observations from becoming experiment seeds
unless source/page references, coordinate or region evidence, and explicit review decisions are
present. Cuneiform, dot, delimiter, compression-artefact, braille, and constellation observations
remain noncanonical until accepted through that workflow.

## What Not To Commit

Raw images, generated image-analysis JSONL outputs, generated transform images, contact sheets,
review HTML, and transform JSONL records.

Generated Stage 4C annotation-site pages, copied review images, grid overlays, and blank coordinate
templates under `experiments/results/visual-annotation/stage4c/` are also generated outputs.

Generated Stage 4D bounded numeric verifier JSON/JSONL outputs under
`experiments/results/bounded-numeric/stage4d/` are also generated outputs.

Generated Stage 4E source-delta reports under `experiments/results/source-delta/stage4e/` and any
ignored `third_party/CicadaSolversIddqd/` raw cache contents are also not committed.

Generated Stage 4F stego/audio fixture reports under `experiments/results/stego-fixtures/stage4f/`
are also not committed. Raw images, audio, binaries, fonts, archives, and extracted payloads remain
outside Git.

Generated Stage 4J observation-review reports under
`experiments/results/observation-review/stage4j/` are also not committed.

Generated Stage 4M image-preflight JSONL and summary reports under
`experiments/results/image-preflight/stage4m/` are also not committed. Raw LP page images and the
raw `data/raw/images/Fib421.jpg` screenshot remain ignored.

Generated Stage 4N stego/audio positive-control readiness reports under
`experiments/results/stego-positive-controls/stage4n/` are also not committed. They are outside the
image workflow, but the same raw-artefact policy applies to historical image/audio fixture bytes and
extracted payloads.

## OutGuess Regression Boundary

Stage 3V adds OutGuess regression under `libreprimus stego`, but it is not part of the image-analysis transform workflow. It uses explicit stego manifests and optional local historical fixtures only. Stage 4F adds source-lock metadata and toolchain requirements for future fixture work without running tools. Stage 4N records positive-control readiness and synthetic controls without executing OutGuess, OpenPuff, MP3Stego, strings, hexdump, or audio tools. Do not run broad OutGuess scans across `third_party/LiberPrimusPages/`; those images remain ignored unless a future manifest lists a tiny reviewed control subset.

## Troubleshooting

If local images are absent, `--allow-missing` supports raw-data-free validation.

If transform generation is slow on high-resolution images, keep the Stage 3P bounded preview
settings rather than producing full-resolution derived artefacts. Original image identity is still
tracked by Stage 3K locks.
