# Page 49-51 Coordinate Source-Lock Workflow

## Stage 5BB Note

Stage 5AW does not alter Stage 5AR coordinates or the Stage 5AP token transcription. It only repairs parser-derived branch metadata from Stage 5AV; Stage 5AX adds validation infrastructure only; Stage 5AY designs preflight manifests and gates only; Stage 5AZ repairs duplicate manifest metadata only; Stage 5BB scaffolds a no-execution runner and active-manifest registry only. Coordinate and image-source truth still come from the Stage 5AR original-image coordinate records.

Use this workflow when reviewing the Stage 5AR page 49-51 original-image coordinate lock.

1. Start from `data/project-state/stage5ar-summary.yaml`.
2. Verify original image metadata in `data/token-block/stage5ar-original-page-image-source-lock.yaml`.
3. Confirm that any compared image appears in `data/token-block/stage5ar-original-page-image-variants.yaml`.
4. Use `data/token-block/stage5ar-page-split-records.yaml` for the 10/13/9 logical split.
5. Use `data/token-block/stage5ar-token-pixel-coordinate-records.yaml` for token bounding boxes.
6. Keep `data/token-block/stage5ar-token-case-policy.yaml` and `data/token-block/stage5ar-token-case-ambiguity-records.yaml` open when reviewing token text.
7. Treat `data/token-block/stage5ar-dwh-coordinate-context.yaml` as context only. Do not run DWH hash/preimage search.
8. For token-case decisions, use the Stage 5AU review pack v2 and blank decision template instead of editing the canonical transcription directly.

Generated reports under `experiments/results/token-block/stage5ar/` are local diagnostics and remain ignored. Raw images under `third_party/LiberPrimusPages/` remain ignored.

Do not use screenshots, crops, modified images, web-rendered pages, or private generated images as coordinate truth. Do not OCR, interpret image semantics, search hashes, decode the block, run stego tools, run CUDA, benchmark, execute scored experiments, activate the canonical corpus, finalise page boundaries, or make solve claims.
