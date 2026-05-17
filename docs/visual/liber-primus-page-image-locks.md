# Liber Primus Page Image Locks

Local original page images live under `third_party/LiberPrimusPages/` and are ignored by Git.

Stage 3K writes committed metadata only:

- `data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl`
- `data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl`

The image scan records filename, relative path, file size, SHA-256, format, width, height, prime-dimension flags, and color mode. It does not run OCR, image interpretation, text experiments, or seed generation.

Generated scan summaries remain ignored under `experiments/results/archive-visual-registry/stage3k/`.
