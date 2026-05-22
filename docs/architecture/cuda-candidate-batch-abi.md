# CUDA Candidate Batch ABI

Stage 5U defines Candidate Batch ABI v0 as a contract-only, no-GPU-safe surface for future native and CUDA backend work.

The ABI is not a kernel implementation. It records shared token-buffer, transform-parameter, key-schedule, stream-schedule, score-vector, top-k, backend-surface, and result-store compatibility contracts so future stages can test conformance before widening CUDA scope.

## Scope

- `candidate_batch_abi_v0` uses candidate-major ordering and structure-of-arrays buffer surfaces.
- Token values are Gematria index-29 values `0..28`; separator placeholders use explicit metadata and must not be transformed.
- Transformable masks must align with token counts and keep separators masked out.
- Generated output bodies remain ignored; committed records are compact metadata and hashes only.
- `gematria_shift_score_only` parity remains distinct from original transform-family semantics.

## Not Authorized

Stage 5U does not run CUDA, modify CUDA source, add kernels, benchmark, process raw data, publish generated bodies, upgrade method families to solved, activate the canonical corpus, finalize page boundaries, or make a solve claim.

Stage 5V has since proved no-GPU Candidate Batch ABI conformance through Python reference fixtures. Stage 5W then prepared the prime-minus-one stream native parity contract and selected `Stage 5X - prime-minus-one stream no-GPU native parity execution and result-store preflight`.
