# Page 49-51 Coordinate Source-Lock Workflow

Use this workflow when reviewing the Stage 5AR page 49-51 original-image coordinate lock.

1. Start from `data/project-state/stage5ar-summary.yaml`.
2. Verify original image metadata in `data/token-block/stage5ar-original-page-image-source-lock.yaml`.
3. Confirm that any compared image appears in `data/token-block/stage5ar-original-page-image-variants.yaml`.
4. Use `data/token-block/stage5ar-page-split-records.yaml` for the 10/13/9 logical split.
5. Use `data/token-block/stage5ar-token-pixel-coordinate-records.yaml` for token bounding boxes.
6. Keep `data/token-block/stage5ar-token-case-policy.yaml` and `data/token-block/stage5ar-token-case-ambiguity-records.yaml` open when reviewing token text.
7. Treat `data/token-block/stage5ar-dwh-coordinate-context.yaml` as context only. Do not run DWH hash/preimage search.

Generated reports under `experiments/results/token-block/stage5ar/` are local diagnostics and remain ignored. Raw images under `third_party/LiberPrimusPages/` remain ignored.

Do not use screenshots, crops, modified images, web-rendered pages, or private generated images as coordinate truth. Do not OCR, interpret image semantics, search hashes, decode the block, run stego tools, run CUDA, benchmark, execute scored experiments, activate the canonical corpus, finalise page boundaries, or make solve claims.

