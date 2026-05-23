# Bounded P56 CUDA Parity Mismatch Investigation

Stage 5AD-fix investigates the Stage 5AD bounded p56 hash mismatch without rerunning CUDA or widening scope.

The investigation records that the Stage 5AD computed CUDA/formula hash `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387` matches the Stage 5X `formula_output_token_hash`. The Stage 5AD expected hash `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87` follows the Stage 5L candidate-major reference hash.

The primary root cause is `expected_hash_reference_lineage_mismatch`. Reference-contract and hash-material policy repair are required; CUDA kernel repair is not supported by current evidence.

Stage 5AD remains a failed historical parity record. Stage 5AD-fix adds no CUDA kernels, changes no CUDA source, runs no full p56, runs no unsolved pages, benchmarks nothing, and makes no solve claim.
