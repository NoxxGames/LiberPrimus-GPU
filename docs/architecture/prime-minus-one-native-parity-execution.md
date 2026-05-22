# Prime-Minus-One Native Parity Execution

Stage 5X executes a bounded no-GPU Python reference for prime-minus-one stream parity. It consumes Stage 5W mapping and expected-hash records, executes only mappings marked ready, and writes compact metadata under `data/cuda/`.

Execution scope:

- `stage5w-mapping-synthetic-prime-control-v0`
- `stage5w-mapping-p56-stage4o-bounded-v0`

Blocked scope:

- `stage5w-mapping-p56-full-fixture-blocked-v0`

Stage 5X does not run CUDA, native C++ CMake, GPU benchmarks, raw page data, or unsolved-page inputs. Generated token bodies and reports remain ignored under `experiments/results/prime-minus-one-native-parity/stage5x/`.

The bounded p56 record compares against the Stage 5W expected hash sourced from Stage 5L compact candidate-major metadata. That is not full p56 parity and is not solve evidence.

Stage 5Y consumes these Stage 5X records for compact reporting and CUDA contract readiness gating only. It does not rerun native parity, execute CUDA, modify CUDA source, add kernels, benchmark, publish generated bodies, or clear the full-p56 blocker.
