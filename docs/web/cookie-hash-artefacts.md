# Cookie And Hash Artefacts

Stage 3K records cookie/hash artefacts in `data/observations/web/cookie-hash-records-v0.yaml`.

The 2013 `167` and `761` cookie/hash values are stored as archived claims with `candidate_hash_type=unknown_256bit_hex`. Stage 3K does not crack hashes and does not claim a preimage.

Cookie/hash records must keep:

- `trusted_as_canonical=false`
- `preimage_status=unknown`, `not_attempted`, or `rejected`
- source provenance
- review status

Any future hash-preimage work must be a bounded manifest-driven experiment with controls.
