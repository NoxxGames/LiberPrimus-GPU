# Stage 5R Expanded Solved-Fixture CUDA Parity

Stage 5R tested whether the existing Gematria CUDA kernel preserves the Stage 5Q native output-token hash contract for the three newly mapped direct-translation solved fixtures.

All three scoped CUDA runs matched their Stage 5Q native hashes:

| Fixture | Tokens | Transformable | Status |
| --- | ---: | ---: | --- |
| `p57-parable` | 118 | 95 | passed |
| `some-wisdom` | 108 | 85 | passed |
| `the-loss-of-divinity` | 94 | 78 | passed |

This is parity evidence only. It does not validate unsolved pages, original transform families, performance, or plaintext claims. The recommended next stage is Stage 5S for compact reporting and result-store integration.
