# Hash Material Policy For Parity Records

Parity hashes must record what bytes or canonical JSON structures were hashed.

Stage 5AE records these allowed contexts:

- `formula_output_vs_formula_output`
- `cuda_formula_vs_stage5x_formula`
- `candidate_major_reference_vs_candidate_major_reference`
- `synthetic_control_vs_synthetic_control`

Forbidden contexts include formula-output hashes compared against candidate-major reference hashes, synthetic controls compared against bounded p56 formula hashes, and any comparison that omits the canonical JSON shape.

Generated result bodies remain ignored. Committed records may store compact hashes, roles, schemas, and policy metadata only.
