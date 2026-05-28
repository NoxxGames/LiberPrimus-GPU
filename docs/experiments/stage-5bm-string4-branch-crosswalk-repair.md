# Stage 5BM String 4 Branch-Crosswalk Repair

Stage 5BM is a metadata-only reconciliation stage. It consumes Stage 5BL review context, Stage 5BK iddqd-v2 String 4 source-lock metadata, Stage 5AP page 49-51 token-block records, and Stage 5AW repaired branch metadata.

## Result

- String 4 branch-membership status: `partial_branch_match`.
- Positions checked: `256`.
- Canonical matches: `249`.
- Stage 5AW-supported noncanonical positions: `6`.
- Unsupported positions: `1`.
- Parser-inconclusive positions: `0`.

The six supported noncanonical differences are within the existing `I/l` ambiguity class. The single unsupported position is preserved as compact source-gap metadata for Stage 5BN review and human-review pack preparation.

## Boundaries

Stage 5BM does not make String 4 active input. It does not replace the Stage 5AP canonical transcription, change active token-block manifests, generate byte streams, materialise variants, enumerate the full branch product, run DWH/hash/preimage search, decode, score, run stego/audio/image/OCR/AI/CUDA/benchmark work, expand the website, or make a solve claim.

Full String 4 bodies, decoded bytes, and reconstructed token streams remain uncommitted. Generated diagnostics remain ignored under `experiments/results/token-block/stage5bm/`.
