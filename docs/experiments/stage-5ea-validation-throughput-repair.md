# Stage 5EA Validation Throughput Repair

Stage 5EA is validation and reviewability infrastructure. It does not perform the deferred number-fact review batch, add source-lock evidence, add Source Browser overlays, generate byte streams, execute token-block work, run CUDA, or make solve claims.

## Scope

- Create `data/project-state/current-stage-state.yaml` as the active current-stage registry.
- Verify Stage 5DZ records remain complete without requiring Stage 5DZ to remain the latest stage.
- Normalize validation wrapper stage IDs so `stage-5ea`, `stage5ea`, and `5ea` resolve to `validate-stage5ea`.
- Record doc-ledger tier policy and historical-test isolation.
- Cache Source Browser number-fact overlays for table, filter, and detail-panel rendering.
- Preserve the Stage 5CM-and-later 8-worker validation cap and finite timeout cleanup policy.

## Boundary

Number-fact review batch 3 is deferred to Stage 5EB. Stage 5EA writes compact metadata only and keeps no-active, no-byte-stream, and no-execution gates closed.
