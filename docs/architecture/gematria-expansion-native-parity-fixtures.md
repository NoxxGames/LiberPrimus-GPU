# Gematria Expansion Native Parity Fixtures

Stage 5Q prepares native parity metadata for mapped Gematria expansion candidates without running CUDA.

Each prepared record contains:

- the source token mapping record;
- candidate shifts `[0, 1, 3, 13, 28]`;
- candidate-major output ordering;
- expected output token values for transformable rune tokens;
- preserved separator and token-kind metadata;
- a deterministic SHA-256 hash over canonical JSON hash material.

The native parity records are future CUDA references. They are not result bodies, speed measurements, or solve evidence.

Stage 5R CUDA work cited these hashes only for controlled solved-fixture-safe parity and matched all three prepared direct-translation records. Any broader fixture expansion, original transform-family execution, benchmark, or unsolved-page use still requires a separate stage.
