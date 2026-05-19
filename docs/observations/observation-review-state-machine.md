# Observation Review State Machine

Stage 4J review states are:

- `pending`
- `needs_human_review`
- `needs_source_lock`
- `needs_coordinates`
- `accepted`
- `rejected`
- `deferred`
- `quarantined`
- `superseded`
- `negative_control`
- `promoted_to_manifest`

Automated policy checks may defer, quarantine, reject, or flag an observation.
They do not accept visual meaning. Acceptance of visual meaning requires human
or source-lock verifier review, and manifest promotion remains a separate
record.

Accepted means â€œthe review decision is accepted as metadata.â€ It does not mean
canonical plaintext, solved page, or experiment seed. `promoted_to_manifest` is
the only state that may support seed use, and only when all promotion gates pass.
