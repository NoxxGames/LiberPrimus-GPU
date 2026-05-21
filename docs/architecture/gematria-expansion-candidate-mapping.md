# Gematria Expansion Candidate Mapping

Stage 5Q maps only committed solved-fixture-safe candidates that can feed the existing Gematria `shift_score` semantics without deriving original transform-family behavior.

The allowed candidate class is direct-translation solved fixtures with committed plaintext/profile provenance. Stage 5Q found three such additional fixtures:

- `p57-parable`
- `some-wisdom`
- `the-loss-of-divinity`

The exact five-buffer pack used by Stage 5L, Stage 5M, and Stage 5O remains a consumed control. Those records are retained for auditability but excluded from the new candidate count.

Blocked solved fixtures stay blocked when they require original-family semantics, such as rotated reverse-Gematria or explicit-key Vigenere. Stage 5Q does not force those families into the Gematria `shift_score` kernel contract.

Generated JSON reports stay ignored under `experiments/results/gematria-expansion-candidate-mapping/stage5q/`. The committed records are compact YAML metadata under `data/cuda/`.

Stage 5Q does not execute CUDA, modify CUDA source, add kernels, run benchmarks, process raw data, publish generated result bodies, use unsolved pages, or make solve claims.

## Stage 5R Result

Stage 5R consumed only the three Stage 5Q mapped direct-translation candidates and matched all three CUDA output-token hashes against the Stage 5Q native hashes. The Stage 5Q consumed-control and original-family blockers remain preserved; Stage 5R does not retroactively widen candidate mapping scope.
## Stage 5S Follow-Up

Stage 5S consumes only the three Stage 5Q mapped direct-translation candidates that Stage 5R ran.
It does not reclassify the Stage 5L/5M/5O five-buffer pack as new candidates and does not unblock
the original-family reverse/Vigenere fixtures. Remaining expansion direction is deferred to the
Stage 5M-5S Deep Research review.
