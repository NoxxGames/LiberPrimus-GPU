# CUDA Planning CLI

The `libreprimus cuda-planning` group manages Stage 5A planning records.

Commands:

- `build-target-plan`: writes target-plan and non-target YAML records from Stage 4Q readiness, Stage 4O parity expectations, and Stage 4P unified result references.
- `build-parity-scaffold`: writes planning-only scaffold records for ready CUDA planning targets.
- `build-implementation-gates`: writes implementation-gate records and the committed Stage 5A summary.
- `validate-stage5a`: validates schemas, counts, guardrail flags, target/scaffold consistency, and non-target coverage.
- `summary`: prints committed Stage 5A summary counts.

The CLI does not compile CUDA, add kernels, run GPU benchmarks, run broad experiments, process raw data, or make solve claims.
