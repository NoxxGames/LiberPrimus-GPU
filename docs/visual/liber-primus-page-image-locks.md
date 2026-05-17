# Liber Primus Page Image Locks

Local original page images live under `third_party/LiberPrimusPages/` and are ignored by Git.

Stage 3K writes committed metadata only:

- `data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl`
- `data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl`

The image scan records filename, relative path, file size, SHA-256, format, width, height, prime-dimension flags, and color mode. It does not run OCR, image interpretation, text experiments, or seed generation.

Generated scan summaries remain ignored under `experiments/results/archive-visual-registry/stage3k/`.

## Stage 3M deterministic features

Stage 3M reads the same ignored local page images and writes generated feature records under `experiments/results/image-analysis/stage3m/`.

The feature records include grayscale statistics, threshold summaries, 4-connected component summaries, symmetry metrics, bit-plane summaries, and review-only visual feature candidates. They remain generated outputs and are not committed.

Raw page images stay ignored. Feature candidates are not experiment seeds until a future review stage promotes a specific observation.
