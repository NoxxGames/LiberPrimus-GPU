# Stage 3M Deterministic Image Analysis

Stage 3M follows the archive/image research recommendation to perform deterministic local image analysis before any AI interpretation, OCR, steganography extraction, or image-derived search.

Run summary:

- Images analysed: `58`
- Threshold values: `32, 64, 96, 128, 160, 192, 224`
- Threshold records: `406`
- Component records: `406`
- Symmetry records: `58`
- Bitplane records: `464`
- Visual feature candidates: `71`

Feature summary:

- `dense_text_like_candidate`: `56`
- `high_symmetry_candidate`: `7`
- `low_bitplane_anomaly_candidate`: `6`
- `sparse_dot_like_candidate`: `2`
- `high_noise_candidate`: `0`

Top symmetric image IDs:

- `liber-primus-page-image-50`
- `liber-primus-page-image-55`
- `liber-primus-page-image-57`
- `liber-primus-page-image-49`
- `liber-primus-page-image-56`
- `liber-primus-page-image-51`
- `liber-primus-page-image-32`
- `liber-primus-page-image-53`
- `liber-primus-page-image-6`
- `liber-primus-page-image-7`

Top sparse/dot-like image IDs:

- `liber-primus-page-image-57`
- `liber-primus-page-image-32`

Generated outputs remain ignored under `experiments/results/image-analysis/stage3m/`.

No OCR, AI/ML image interpretation, image-derived cipher run, CUDA change, canonical corpus activation, page-boundary finalization, or solve claim is made.
