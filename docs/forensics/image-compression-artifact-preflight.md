# Image Compression Artefact Preflight

Stage 4E records a future deterministic image/source-variant audit branch for JPEG-like artefacts observed or discussed around Liber Primus depictions. Stage 4M implements the first metadata-only preflight for that branch. This page is a policy note; the Stage 4M aggregate result is in `docs/forensics/image-compression-artifact-preflight-results.md`.

## Working Hypotheses

PNG page images may show compression-like features for several ordinary reasons:

- source artwork had JPEG intermediates;
- images were recompressed before being placed in PNG containers;
- public mirrors contain different compression histories;
- visible features are ordinary compression or scanner noise;
- intentional visual artefacts are possible but less likely and require controls.

## Stage 4M Preflight

Stage 4M records local LP page-image metadata, source-variant readiness, deterministic compression metrics, and review-only artifact candidates. It does not download external variants or produce visualisations for commit.

- filename, count, SHA-256, file-size, dimension, and color-mode comparison;
- 8x8 blockiness proxy;
- edge and noise residual summaries;
- channel histogram summary;
- bitplane summaries;
- star-like/compression-like candidate review state;
- bigram/Fibonacci-421 readiness tracking as blocked, not executed.

Future source-variant comparison remains blocked until external variant bytes are source-locked in an ignored cache.

## Policy

Compression-like or star-like features remain review candidates only. They are not solve evidence, not canonical observations, and not experiment seeds. Any future image-derived branch must preserve source lineage, negative controls, and `usable_as_experiment_seed=false` until an explicit review stage changes that.
