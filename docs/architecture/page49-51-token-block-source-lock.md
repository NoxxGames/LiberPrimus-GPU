# Page 49-51 Token-Block Source Lock

Stage 5AP records the page 49-51 token-block candidate as source-lock and preflight metadata. It does not decode the block, infer text, perform hash or preimage search, run stego tools, run CUDA, benchmark, or make solve claims.

Committed records:

- `data/token-block/stage5ap-page49-51-source-lock.yaml`
- `data/token-block/stage5ap-page49-51-image-provenance.yaml`
- `data/token-block/stage5ap-token-block-canonical-transcription.yaml`
- `data/token-block/stage5ap-token-block-coordinate-records.yaml`
- `data/project-state/stage5ap-summary.yaml`

The source-lock layer records local page-image metadata hashes where images are available, but raw page images remain ignored. The canonical transcription is a 32 row by 8 column token grid supplied for review. Logical coordinates are provenance anchors, not page-boundary finalisation and not OCR output.

Stage 5AQ may use these records for Deep Research source-lock review of exact token-to-value claims. Any future execution stage must cite the Stage 5AP source-lock, transcription, mapping, null-control, DWH context, and guardrail records before it can propose a bounded manifest.
