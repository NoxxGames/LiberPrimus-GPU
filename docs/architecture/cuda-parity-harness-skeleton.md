# CUDA Parity Harness Skeleton

Stage 5B creates a planning-only CUDA parity harness skeleton. It consumes Stage 5A target plans, Stage 4O parity expectations, Stage 4P unified result references, and Stage 4Q benchmark/parity readiness records, then writes committed metadata that a future CUDA implementation stage must cite.

Stage 5B does not add CUDA kernels, modify CUDA source, run GPU benchmarks, require CUDA hardware, claim performance, claim speedups, process raw data, activate the canonical corpus, finalise page boundaries, or make solve claims.

## Record Sets

- `data/cuda/stage5b-cuda-parity-harness-plan.yaml`
- `data/cuda/stage5b-cuda-parity-fixtures.yaml`
- `data/cuda/stage5b-cuda-backend-capability.yaml`
- `data/cuda/stage5b-future-kernel-parity-matrix.yaml`
- `data/cuda/stage5b-cuda-parity-harness-summary.yaml`

Generated reports remain ignored under `experiments/results/cuda-parity/stage5b/`.

## Harness Boundary

The harness records define future comparison obligations:

- exact `output_token_hash` matching;
- exact `output_text_hash` matching where applicable;
- Stage 4I score-summary shape compatibility;
- deterministic top-k ordering where a future kernel returns ranked outputs;
- explicit blocked conditions for unsupported adapters or missing CPU references.

Readiness means only that a future implementation can be planned against a CPU reference. It is not execution approval.

Stage 5C adds a separate build/device readiness layer. CUDA build profiles, toolchain detection, optional device metadata, and smoke-build status must be cited by future CUDA implementation stages, but they still do not authorize kernels, GPU benchmarks, speedup claims, or local GPU requirements.

Stage 5D adds the native CPU backend/threading baseline that Stage 5E cites when selecting the
first CUDA adapter and Stage 5F uses for the synthetic CUDA parity implementation. Harness records
alone are not enough: future CUDA work needs Stage 5D native output hashes, Stage 5F synthetic
parity records, and native/Python parity records.
