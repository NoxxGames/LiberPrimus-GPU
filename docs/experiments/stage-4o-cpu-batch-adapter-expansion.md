# Stage 4O CPU Batch Adapter Expansion

Stage 4O is an infrastructure stage. It runs only small CPU-only synthetic and solved-fixture-safe batch commands to write ignored generated records and a committed aggregate summary.

## Manifests

- `experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml`
- `experiments/manifests/cpu-batch/stage4o-adapter-expansion-smoke-batch.yaml`
- `experiments/manifests/cpu-batch/stage4o-cpu-cuda-parity-readiness.yaml`

Each manifest keeps `cpu_only=true`, `cuda_used=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `generated_outputs_committed=false`.

## Generated Outputs

Generated outputs remain ignored under `experiments/results/cpu-batch/stage4o/`:

- `result_records.jsonl`
- `adapter_coverage.json`
- `parity_expectations.jsonl`
- `scoring_compatibility.json`
- `summary.json`
- `warnings.jsonl`

## Boundaries

Stage 4O does not execute unsolved-page campaigns, process raw data, change solved-baseline expected outputs, add new cipher families, implement CUDA, or make solve claims.
