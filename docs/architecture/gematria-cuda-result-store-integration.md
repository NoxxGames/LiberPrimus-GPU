# Gematria CUDA Result-Store Integration

Stage 5P integrates only compact metadata from Stage 5O repeat parity into Stage 4P-compatible
result-store records. The committed records live under `data/cuda/` and cite fixture ids, candidate
ids, source transform families, output-token hashes, and no-solve/no-publication guardrails.

The generated JSON reports under `experiments/results/gematria-cuda-result-store/stage5p/` are
ignored. Stage 5P does not publish CUDA result bodies, token arrays, SQLite databases, or local
reports.

Stage 5P is read-only reporting infrastructure. It does not run CUDA, modify CUDA source, add
kernels, benchmark the GPU, widen solved-fixture scope, or enable unsolved-page CUDA.
