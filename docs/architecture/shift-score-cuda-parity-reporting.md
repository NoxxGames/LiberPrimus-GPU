# shift_score CUDA Parity Reporting

Stage 5G reports the existing Stage 5F `shift_score_kernel` synthetic CUDA/native parity result. It does not widen the kernel, add a new kernel, run solved pages, run unsolved pages, or turn the synthetic fixture into production Gematria mod-29 CUDA.

## Recorded Surface

The committed parity report is `data/cuda/stage5g-shift-score-parity-report.yaml`.

It records:

- selected kernel: `shift_score_kernel`
- selected target: `stage5a-caesar_mod29-cuda-target`
- transform family: `caesar_mod29`
- adapter family: `native_cpu_synthetic_shift_adapter`
- fixture: `stage5d-native-synthetic-shift-fixture-v0`
- native reference hash: `76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`
- CUDA output hash: `76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`

The current result means only that the Stage 5F synthetic uppercase Latin fixture still matches the Stage 5D native synthetic reference.

## Boundaries

- The fixture is uppercase Latin A-Z synthetic parity.
- The current kernel is not production Gematria mod-29 behavior.
- Solved-fixture CUDA execution remains blocked.
- Real Liber Primus page data remains out of scope.
- GPU benchmark commands remain out of scope.
- Generated reports remain ignored under `experiments/results/cuda-parity-reporting/stage5g/`.

## Next Contract Work

Stage 5H must define the Gematria mod-29 `shift_score` contract and native parity fixture preparation before any solved-fixture-safe CUDA execution can be considered.
