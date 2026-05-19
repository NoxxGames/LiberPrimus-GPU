# Cookie And Hash Artefacts

Stage 3K records cookie/hash artefacts in `data/observations/web/cookie-hash-records-v0.yaml`.

The 2013 `167` and `761` cookie/hash values are stored as archived claims with `candidate_hash_type=unknown_256bit_hex`. Stage 3K does not crack hashes and does not claim a preimage.

Cookie/hash records must keep:

- `trusted_as_canonical=false`
- `preimage_status=unknown`, `not_attempted`, or `rejected`
- source provenance
- review status

Stage 3L adds a bounded SHA-256-only preimage pack runner for these two archived artefacts. It tests explicit literal and numeric/base29 candidate packs, logs exact byte strings, and found zero exact SHA-256 matches.

Stage 3U executes the post-Discord signed/public string variant pack `EXP-3R-001`. It generated `156` candidates before deduplication, tested `105` deduplicated byte strings against both archived cookie values for `210` exact comparisons, and found zero exact SHA-256 matches.

Stage 4G executes the source-backed cookie refresh from Stage 4B candidate records. It generated `4`
candidates before and after deduplication, marked `2` previous-pack duplicates, tested `8` exact
SHA-256 comparisons against both archived cookie values, and found zero exact matches.

Any future hash-preimage work must remain bounded and exact-match only. After Stage 4G, do not rerun
cookie exact packs without newly source-locked exact candidate strings.
