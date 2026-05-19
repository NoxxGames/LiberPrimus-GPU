# Reviewed Observation Promotion Ledger

Stage 4L joins Stage 4J review decisions with Stage 4K source-lock records.
The ledger records whether each reviewed observation is ready only as a source
reference, ready only as a control, blocked, deferred, quarantined, rejected, or
ready for a future manifest.

Stage 4L does not execute any manifest. `ready_for_manifest` is a planning
state, not permission to run an experiment. Future manifests must cite the
specific readiness records they depend on.

Local summary:

- Reviewed observations loaded: 96.
- Ledger records created: 96.
- Ready for manifest: 0.
- Ready as control-only: 17.
- Source-reference-only: 14.
- Blocked/deferred/quarantined/rejected: 47 / 2 / 15 / 1.
- Manifest readiness records: 12.

Visual cuneiform and dot observations remain blocked or quarantined until exact
coordinates, accepted readings, and review-state requirements exist. Cookie work
remains blocked after the Stage 4G zero exact-match result unless new
source-backed exact strings appear. Stego/audio work remains blocked until
assets, toolchains, and expected-output controls are available.
