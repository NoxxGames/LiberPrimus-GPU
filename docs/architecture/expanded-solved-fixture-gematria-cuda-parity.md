# Expanded Solved-Fixture Gematria CUDA Parity

Stage 5R is the controlled CUDA parity run for the three Stage 5Q mapped direct-translation fixtures:

- `p57-parable`
- `some-wisdom`
- `the-loss-of-divinity`

The stage uses the existing `gematria_mod29_shift_score_kernel` and the Stage 5Q token buffers, transformable masks, candidate shifts, and native output-token hashes. It compares CUDA output-token hashes to Stage 5Q native hashes under the same canonical JSON hash contract.

Stage 5R is correctness metadata only. It adds no CUDA kernels, changes no device arithmetic, runs no unsolved pages, uses no raw Liber Primus page data, runs no benchmark, publishes no generated result bodies, and makes no solve claim.

Generated reports remain ignored under `experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/`. Committed records live under `data/cuda/`.
