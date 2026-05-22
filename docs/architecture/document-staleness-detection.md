# Document Staleness Detection

Stage 5AB hardens operational Markdown freshness checks. The detector uses a committed source-of-truth record, an operational file map, and a dynamic stage parser so future stages do not need one regex per stage label.

The checker is strict for current-state labels such as current completed stage, current work, latest completed stage, next, and existing CUDA code. Historical logs under `docs/development-logs/**` and `research-log/**` are exempt because they preserve original stage context.

Guardrails:

- Website expansion is a future unnumbered project, not Stage 6.
- Stage ordering supports suffixes such as `Stage 5Z`, `Stage 5AA`, `Stage 5AB`, and `Stage 5AC`.
- Stale `Existing CUDA code ... only ...` cap sentences should be replaced with source-of-truth references instead of long brittle lists.
- Findings are generated under `experiments/results/doc-staleness/stage5ab/` and remain ignored.

Stage 5AB adds no CUDA execution, CUDA source changes, kernels, benchmarks, scored experiments, raw-data processing, website expansion, or solve claims.
