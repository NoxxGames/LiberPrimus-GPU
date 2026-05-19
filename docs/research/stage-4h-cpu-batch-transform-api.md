# Stage 4H CPU Batch Transform API Research Note

Stage 4H follows the Stage 4G cookie exact-candidate refresh and shifts the workbench back to architecture. The project now has enough bounded CPU experiment and source-review history to justify a stable CPU batch API before any future CUDA parity work.

Research outcome:

- CPU batch API is active infrastructure.
- Current transform registry entries have explicit CPU batch adapter coverage.
- Generated CPU batch records carry deterministic output hashes.
- Minimal triage scoring can be attached as metadata without solve claims.
- CUDA remains deferred.

Next research step:

Stage 4I should consolidate scorer output and calibration reporting so future CUDA parity can compare transform-and-score records, not just transform hashes.
