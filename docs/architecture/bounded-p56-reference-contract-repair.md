# Bounded P56 Reference Contract Repair

Stage 5AE separates three hash roles:

- Formula-output hash: valid for formula parity and CUDA formula parity.
- Candidate-major reference hash: valid for Stage 5L/5X candidate-major reference lineage only.
- Synthetic control hash: valid only for Stage 5AA synthetic control comparisons.

The formula-output hash `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387` must not be compared against candidate-major reference material. The reference hash `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87` must not be used as a formula-parity expected hash.

Future parity stages must name the hash material and comparison role before validating a result. Missing or mixed hash material is a blocker, not a reason to reinterpret an old failure.
