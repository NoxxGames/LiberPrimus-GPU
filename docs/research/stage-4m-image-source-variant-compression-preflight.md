# Stage 4M Image Source-Variant And Compression Preflight

Stage 4M creates a deterministic preflight layer for image source variants and compression-like artefacts.

## Outputs

- `data/observations/visual/stage4m-image-source-variant-preflight-records.yaml`
- `data/observations/visual/stage4m-image-compression-preflight-records.yaml`
- `data/observations/visual/stage4m-image-artifact-review-candidates.yaml`
- `data/observations/visual/stage4m-image-preflight-summary.yaml`
- `data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml`

Generated JSONL reports are ignored under `experiments/results/image-preflight/stage4m/`.

## Findings

The stage scanned `58` ignored local LP page images and produced `58` source-variant records and `58` compression metric records. All source-variant comparisons remain blocked until external source-variant image bytes are source-locked in an ignored cache. The single Stage 4E compression artefact observation remains a review-only candidate.

The bigram/Fibonacci-421 observation remains blocked. Stage 4M confirms the local `Fib421.jpg` hash when present, but does not regenerate a bigram matrix, read raw transcripts, run a frequency-pattern audit, or promote the claim.

## Boundaries

No raw images, generated visualisations, external variants, Discord logs, transcript material, or experiment outputs are committed. No hidden-message extraction, OCR, AI/ML interpretation, stego extraction, CUDA work, canonical corpus activation, page-boundary finalisation, or solve claim is made.
