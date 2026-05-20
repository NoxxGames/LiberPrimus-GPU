# Future CUDA Parity Benchmark Gates

Future CUDA work remains deferred until Stage 5 explicitly scopes planning or scaffolding. A future CUDA target must satisfy these gates before implementation can be trusted:

- CPU reference behavior exists and is covered by a Stage 4O adapter.
- Stage 4O parity expectations exist for output token hashes, output text hashes, score-summary shape, separator behavior, line/reset behavior, and unknown-token handling.
- Stage 4P unified result surfaces can compare the CPU output with method status and score-summary state.
- The benchmark scope is raw-data-free or uses approved solved-fixture-safe inputs.
- Generated outputs, raw data, SQLite databases, and local reports remain uncommitted.
- Tests check parity before optimization.

Stage 4Q readiness state is not permission to write CUDA kernels. It only records which transform families are ready for future planning, which are blocked, and which are skipped because they are not CUDA transform targets.

Stage 5A converts that readiness state into explicit CUDA target-plan, parity scaffold, non-target, and implementation-gate records. These records are still planning metadata; GPU benchmarks remain blocked until a later harness proves exact CPU/GPU parity.
