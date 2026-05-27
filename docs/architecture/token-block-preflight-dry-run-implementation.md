# Token-Block Preflight Dry-Run Implementation

Stage 5BD adds a metadata-only dry-run planning layer for the page 49-51 token-block preflight work. It consumes the Stage 5BB active-manifest registry and the Stage 5AW/5AZ repaired records, then writes deterministic plan metadata without generating real token-block byte streams or materialising variant branches.

The implementation lives under `python/libreprimus/token_block/preflight_runner/`. The package split keeps active-manifest loading, future-path validation, run-plan ID creation, fixture-only records, archive markers, validation-evidence consolidation, and gate checks separated from the older Stage 5BB module.

Stage 5BD is not an execution layer. The runner fails closed for real byte-stream generation, real branch materialisation, DWH/hash/preimage search, decoding, scoring, CUDA, benchmarks, website expansion, method-status upgrades, canonical corpus activation, page-boundary finalisation, and solve claims.

## Committed Records

- `data/token-block/stage5bd-dry-run-policy.yaml`
- `data/token-block/stage5bd-active-manifest-lock.yaml`
- `data/token-block/stage5bd-dry-run-plan-manifest.yaml`
- `data/token-block/stage5bd-run-plan-id-registry.yaml`
- `data/token-block/stage5bd-future-result-path-validation.yaml`
- `data/token-block/stage5bd-execution-gate-dry-run-validation.yaml`
- `data/token-block/stage5bd-no-byte-stream-proof.yaml`
- `data/project-state/stage5bd-summary.yaml`

Generated reports remain ignored under `experiments/results/token-block/stage5bd/`.
