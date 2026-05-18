# Deterministic Image Transform Suite

Stage 3P adds a local review pipeline for ignored Liber Primus page images. It creates deterministic preview transforms, metrics, contact sheets, and a local HTML review index under `experiments/results/image-transforms/stage3p/`.

The suite is for visual review only. It does not run OCR, AI/ML interpretation, steganography extraction, image-derived cipher experiments, CUDA, canonical corpus activation, page-boundary finalization, or solve claims.

## Transform Families

- Basic previews: grayscale, invert, autocontrast, posterize, thresholds `32, 64, 96, 128, 160, 192, 224`.
- Channel previews: RGB channel split and alpha when available.
- Bitplanes: grayscale bitplanes `0..7`.
- Edge maps: deterministic finite-difference edge magnitude.
- Split/mirror views: vertical halves, horizontal halves, mirrored halves, half-difference maps, and 180-degree rotation difference.
- Component overlays: largest foreground component boxes at thresholds `64, 128, 192`.

Large source images are downscaled for generated review previews so the stage remains bounded. Source identity still comes from the Stage 3K image lock records and original SHA-256 hashes.

## Output Policy

Generated images, contact sheets, HTML pages, JSONL records, and summaries are ignored:

```text
experiments/results/image-transforms/stage3p/
```

Do not commit raw page images or generated transform artefacts.
