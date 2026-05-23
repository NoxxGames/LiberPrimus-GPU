# Bounded P56 Hash Lineage And Reference Contract

Stage 5AD-fix separates two hash materials:

- Formula-output material: input tokens `[25, 11]`, stream values `[1, 2]`, output tokens `[24, 9]`, hash `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`.
- Stage 5L candidate-major reference material: the Stage 5L prepared candidate-major output table, hash `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`.

The Stage 5AD CUDA run produced the formula-output hash and therefore agrees with the Stage 5X formula trace, not with the Stage 5L candidate-major expected hash used as the Stage 5AD parity target.

Stage 5AE should repair reporting by naming the hash material being checked and preserving Stage 5AD as failed. It must not silently rewrite historical records or claim a CUDA parity pass.
