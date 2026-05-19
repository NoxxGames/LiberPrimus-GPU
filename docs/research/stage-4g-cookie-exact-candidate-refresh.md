# Stage 4G Research Summary: Cookie Exact-Candidate Refresh

Stage 4G executed the designated Stage 4B cookie pack refresh without broadening the method family.

The stage tested the two historical cookie targets:

- `cookie-2013-167-v0`
- `cookie-2013-761-v0`

Only source-backed base strings from Stage 4B cookie records and existing cookie artefact records were
used. The Stage 4B manifest did not declare extra variants or hash families, so Stage 4G used raw
UTF-8 strings and SHA-256 only.

Result:

- `4` generated candidates
- `4` deduplicated candidates
- `2` candidates already covered by previous packs
- `8` exact SHA-256 comparisons
- `0` exact matches

Interpretation:

This is a negative bounded exact-match result. It does not disprove the historical cookie artefact,
but it further deprioritises SHA-256 exact packs until new exact source strings are locked. Any future
cookie work needs a new source-backed candidate string, a bounded manifest, and the same no-fuzzy,
no-hashcat, no-GPU policy.
