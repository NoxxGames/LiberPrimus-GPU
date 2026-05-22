# Expanded Gematria CUDA Parity Reporting

Stage 5S reports the Stage 5R expanded solved-fixture CUDA/native parity records without rerunning CUDA.

The source records are the three Stage 5Q mapped direct-translation fixtures executed by Stage 5R:

- `p57-parable`
- `some-wisdom`
- `the-loss-of-divinity`

The reporting layer preserves only compact metadata: fixture identifiers, candidate identifiers, token counts, transformable-token counts, Stage 5Q native hashes, Stage 5R CUDA hashes, and guardrail flags.

This reporting layer is not evidence of decrypted unsolved text, original direct-translation CUDA semantics, GPU performance, or broad solved-fixture readiness. Stage 5R exercised only the mapped `gematria_shift_score_only` semantics through the existing `gematria_mod29_shift_score_kernel`.

Generated reports live under `experiments/results/gematria-expanded-cuda-result-store/stage5s/` and are ignored.

Stage 5T consumes these compact parity-reporting records and converts the Stage 5M through Stage 5S
arc into a solved-family readiness matrix. It selects Stage 5U shared candidate batch ABI work
before more original-family kernel contracts, benchmarks, or unsolved-page CUDA can be considered.
