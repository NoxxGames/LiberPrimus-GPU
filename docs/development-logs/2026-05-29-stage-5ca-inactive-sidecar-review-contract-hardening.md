# Stage 5CA - Inactive-Sidecar Review Contract Hardening

Implemented Stage 5CA as metadata-only review-contract hardening.

- Added `libreprimus token-block build-stage5ca`, focused Stage 5CA validators, aggregate validation, and summary display.
- Created compact Stage 5CA records for Stage 5BZ findings integration, exact future-runner citation contract, fail-closed triggers, activation preconditions, manifest-supersession preflight, sidecar transition policy, Stage 5BY scaffold preservation, Stage 5BD plan preservation, active-lineage preservation, no-active-ingestion, no-byte-stream, DWH quarantine, guardrails, handoff policy, summary, and next-stage routing.
- Preserved String 4 as inactive, non-canonical, not active input, not dry-run ingested, not byte-stream generated, and not execution-capable.
- Preserved Stage 5BD run-plan ID count `10` and the corrected Stage 5AW active-lineage path.
- Added Stage 5CA schemas and tests for exact citations, fail-closed triggers, activation preconditions, supersession preflight, sidecar gates, Stage 5BD preservation, active lineage, reviewability, ignore policy, and schema validation.
- Updated current-state docs, source-of-truth metadata, consistency wrappers, and token-block CLI reference.

Validation notes:

- Stage 5CA build and focused validators passed locally.
- Stage 5CA direct pytest subset passed before full-suite validation.
- Generated diagnostics remain under `experiments/results/token-block/stage5ca/` and are ignored.
- `codex-output/stage5ca-codex-completion.md` is the local handoff path and must remain ignored.
