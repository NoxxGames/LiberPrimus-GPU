# Observation Promotion Policy

Observation promotion requires all applicable gates:

- source is locked, or the source is a synthetic test fixture;
- review state is `accepted` or `promoted_to_manifest`;
- `solve_claim=false`;
- `trusted_as_canonical=false` by default;
- `usable_as_experiment_seed=true` appears only after explicit promotion;
- visual candidates have page/image references;
- visual seed candidates have coordinates or a documented non-coordinate
  rationale;
- cuneiform candidates have coordinates and an accepted reading;
- dot/binary candidates have explicit ordering, polarity, coordinates, and
  ambiguity resolution;
- Discord-derived leads have public-source corroboration;
- negative controls promote only as controls.

Stage 4J promotes zero observations to candidate manifests. It records why each
reviewed item is blocked, deferred, quarantined, accepted as source metadata, or
usable only as a control.
