# Stage 3K Local Image Lock Summary

Stage 3K scanned local Liber Primus page images and committed metadata-only lock records. Raw images remain ignored and uncommitted.

## Local Scan

- Source directory: `third_party/LiberPrimusPages/`
- Image files scanned: `58`
- Image lock records written: `58`
- Image artifact records written: `58`
- Prime-dimension image count: `0`
- Generated scan summary: `experiments/results/archive-visual-registry/stage3k/local-image-scan-summary.json`

## Committed Metadata

- Lock records: `data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl`
- Image artifact records: `data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl`

## Safety

- Raw image files under `third_party/LiberPrimusPages/` are ignored.
- Generated scan summary is ignored.
- Metadata records are noncanonical and do not include OCR, AI interpretation, seed generation, or solve claims.
