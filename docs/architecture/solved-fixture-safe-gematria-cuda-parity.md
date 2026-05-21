# Solved-Fixture-Safe Gematria CUDA Parity

Stage 5M is the first approved CUDA run over committed solved-fixture-safe Gematria token buffers. It uses only the existing `gematria_mod29_shift_score_kernel` and the five Stage 5L mapped token buffers.

The execution scope is deliberately narrow:

- input records come from `data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml`;
- expected hashes come from `data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml`;
- output hashes use `sha256_canonical_json_v1`;
- original transform-family semantics are not exercised except as numeric `shift_score` buffers;
- no unsolved page, raw Liber Primus, Discord, image, stego, audio, canonical-corpus, or page-boundary data is processed.

Stage 5M adds host-side runner plumbing for the existing kernel so the local optional CUDA run can consume generated input files. It does not add a new CUDA kernel and does not change device arithmetic.

The committed records are:

- `data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml`;
- `data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml`;
- `data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml`;
- `data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml`.

Generated JSON reports stay ignored under `experiments/results/gematria-solved-fixture-cuda/stage5m/`.

Stage 5M is correctness metadata only. It is not a benchmark, speedup claim, broad CUDA implementation, solve claim, canonical corpus activation, or page-boundary finalization.
