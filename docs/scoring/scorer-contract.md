# Scorer Contract

Stage 4I defines the durable scorer contract for CPU batch and future CUDA parity work. The contract describes existing scoring behavior; it does not create a new scoring model.

Every score summary must identify the scorer, scorer version, input stream, candidate, transform family, score status, confidence label when scored, calibration profile, and safety flags. `solve_claim=false`, `trusted_as_canonical=false`, and `cuda_used=false` are required.

Scores are triage metadata only. A high score may create a review lead, but it cannot validate plaintext or prove a Liber Primus page solved.

Generated scoring consolidation outputs remain under ignored `experiments/results/scoring-consolidation/stage4i/`. Committed scoring records live under `data/scoring/`.
