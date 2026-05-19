# Promotion Readiness Policy

Observation promotion is the gate between review records and future manifests.
It is not experiment execution.

A record can be `ready_for_manifest` only when all required gates pass:

- Review state is accepted or promoted to manifest.
- Source is locked or explicitly synthetic/test-fixture safe.
- `solve_claim=false`.
- `usable_as_experiment_seed=true` is explicit.
- Visual observations have page/image references.
- Cuneiform and dot observations have coordinates or a documented
  non-coordinate rationale.
- Discord-derived observations have public-source corroboration.
- Scoring labels are triage-only and are not the promotion reason by themselves.
- Numeric/frequency pattern claims have reproducible matrix generation,
  declared ordering/indexing conventions, null controls, and multiple-testing
  controls.

Control-only observations may be used as negative/null controls without being
accepted as true claims.
