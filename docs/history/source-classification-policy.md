# Source Classification Policy

Stage 3K source records must include `source_class`, `review_status`, `canonical_status`, and `trusted_as_canonical=false`.

Allowed source classes:

- `primary_signed`
- `strong_community_technical`
- `secondary_archive`
- `reference_only_tooling`
- `archived_claim`
- `speculative_observation`
- `negative_control_material`

`canonical_status=canonical_active` is not allowed in Stage 3K. Live Tor crawling is out of scope. Mutable community pages can be useful discovery material, but they stay noncanonical until separately locked and reviewed.

Stage 3N Discord HTML ingestion is a source-discovery layer only. Discord claims are not source
truth, and committed records must be aggregate/redacted with raw logs, message bodies, usernames,
and private URLs excluded.
