# Image Compression Artefact Preflight

Stage 4E records a future deterministic image/source-variant audit branch for JPEG-like artefacts observed or discussed around Liber Primus depictions. This page is a backlog and policy note, not an analysis result.

## Working Hypotheses

PNG page images may show compression-like features for several ordinary reasons:

- source artwork had JPEG intermediates;
- images were recompressed before being placed in PNG containers;
- public mirrors contain different compression histories;
- visible features are ordinary compression or scanner noise;
- intentional visual artefacts are possible but less likely and require controls.

## Future Tests

A future preflight stage may compare locked source variants with deterministic metrics:

- filename, count, SHA-256, file-size, dimension, and color-mode comparison;
- DCT/blockiness estimates;
- edge and noise residual views;
- recompress-difference maps;
- channel and bitplane views;
- star-like symbol candidate review;
- known JPEG and non-JPEG negative controls.

These tests must be bounded, deterministic, and source-variant aware. They must not infer hidden meaning from artefacts.

## Policy

Compression-like or star-like features remain review candidates only. They are not solve evidence, not canonical observations, and not experiment seeds. Any future image-derived branch must preserve source lineage, negative controls, and `usable_as_experiment_seed=false` until an explicit review stage changes that.
