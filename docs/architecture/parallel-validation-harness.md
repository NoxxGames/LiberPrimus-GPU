# Stage 5AX Parallel Validation Harness

Stage 5AX adds local validation-speed infrastructure. It does not replace the conservative CI path and does not run cryptanalytic work.

The harness classifies validation commands before execution. Only commands marked `read_only_parallel_safe` or `read_only_parallel_safe_with_isolated_temp` may run concurrently. Git mutation, GitHub issue mutation, network/remote commands, commit/push, generated-output-producing build steps, and blocked cryptanalytic commands remain serial or disabled.

Pytest uses `pytest-xdist` when it is available. When xdist is unavailable, the harness falls back to deterministic file sharding across capped subprocess workers. The committed shard plan records test files once and keeps generated logs under ignored `experiments/results/ci/parallel-validation/stage5ax/`.

Stage 5AX records wall-clock validation timings only as infrastructure diagnostics:

- `validation_timing_recorded=true`
- `benchmark_performed=false`
- `cryptanalytic_benchmark_performed=false`

Bounded token-block preflight design was moved to Stage 5AY after the user inserted this validation stage.
