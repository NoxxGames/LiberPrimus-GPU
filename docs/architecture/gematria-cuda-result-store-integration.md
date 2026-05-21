# Gematria CUDA Result-Store Integration

Stage 5P integrates only compact metadata from Stage 5O repeat parity into Stage 4P-compatible
result-store records. The committed records live under `data/cuda/` and cite fixture ids, candidate
ids, source transform families, output-token hashes, and no-solve/no-publication guardrails.

The generated JSON reports under `experiments/results/gematria-cuda-result-store/stage5p/` are
ignored. Stage 5P does not publish CUDA result bodies, token arrays, SQLite databases, or local
reports.

Stage 5P is read-only reporting infrastructure. It does not run CUDA, modify CUDA source, add
kernels, benchmark the GPU, widen solved-fixture scope, or enable unsolved-page CUDA.

Stage 5Q follow-up: compact Stage 5P records now feed
`libreprimus gematria-expansion-candidate-mapping`, which maps three additional direct-translation
solved-fixture-safe candidates for future bounded `shift_score` parity. The Stage 5L/5M/5O
five-buffer pack remains a consumed control and is excluded from new candidate counts.

Stage 5R follow-up: expanded solved-fixture CUDA parity now produces three compact preflight rows for Stage 5S result-store integration. Generated CUDA output bodies remain ignored and parity success still cannot upgrade method-family status to solved.
