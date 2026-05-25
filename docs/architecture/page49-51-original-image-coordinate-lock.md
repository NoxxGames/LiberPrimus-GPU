# Page 49-51 Original-Image Coordinate Lock

Stage 5AR closes the page 49-51 coordinate source gap by anchoring the Stage 5AP token block to local original page images in `third_party/LiberPrimusPages/`.

Coordinate truth is restricted to original page-image pixel space. Screenshots, crops, modified images, web-rendered pages, static-site exports, and private generated images can be inventoried as variants, but they cannot be coordinate sources.

Committed records:

- `data/token-block/stage5ar-original-page-image-source-lock.yaml`
- `data/token-block/stage5ar-original-page-image-variants.yaml`
- `data/token-block/stage5ar-page-split-policy.yaml`
- `data/token-block/stage5ar-page-split-records.yaml`
- `data/token-block/stage5ar-token-pixel-coordinate-policy.yaml`
- `data/token-block/stage5ar-token-pixel-coordinate-records.yaml`
- `data/token-block/stage5ar-token-coordinate-validation.yaml`
- `data/project-state/stage5ar-summary.yaml`

The lock selects three original image candidates: pages 49, 50, and 51. Each is recorded with path, SHA-256, dimensions, image format, colour mode, and raw-image commit guards. The pixel coordinate builder writes 256 token bounding boxes using deterministic image projections only. It does not OCR, classify glyph meaning, interpret token semantics, or change the Stage 5AP transcription.

Stage 5AR validates the accepted 10/13/9 logical split in source-locked image context and records `valid_with_review_required` because human review is still required before any future bounded preflight can treat coordinates as reviewed.

