# Cookie And Hash Artefacts

Stage 3K records cookie/hash artefacts in `data/observations/web/cookie-hash-records-v0.yaml`.

The 2013 `167` and `761` cookie/hash values are stored as archived claims with `candidate_hash_type=unknown_256bit_hex`. Stage 3K does not crack hashes and does not claim a preimage.

Cookie/hash records must keep:

- `trusted_as_canonical=false`
- `preimage_status=unknown`, `not_attempted`, or `rejected`
- source provenance
- review status

Stage 3L adds a bounded SHA-256-only preimage pack runner for these two archived artefacts. It tests explicit literal and numeric/base29 candidate packs, logs exact byte strings, and found zero exact SHA-256 matches.

Any future hash-preimage work must remain bounded and exact-match only unless a later manifest explicitly expands the scope.
