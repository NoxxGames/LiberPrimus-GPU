# Cookie Hash Preimage Packs

Stage 3L defines two explicit SHA-256-only candidate packs for the archived 2013 cookie/hash artefacts:

- `hist_cookie_literal_pack_v1`
- `hist_cookie_base29_numeric_pack_v1`

The packs live under `data/observations/web/hash-preimage-candidate-packs/`. They are curated, bounded, and inspectable. They do not import external dictionaries, recurse over phrase combinations, run hashcat, use GPU acceleration, or test non-SHA-256 algorithms.

Stage 3U adds a manifest-backed post-Discord pack for signed/public strings:

- `EXP-3R-001-cookie-sha256-signed-variants-a.yaml`

That manifest is not a broad dictionary. It expands only manifest-declared base strings and byte variants, uses UTF-8 and SHA-256 only, and writes generated results under `experiments/results/post-discord/stage3u/`.

Stage 4G adds the source-backed cookie refresh:

- `experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml`

Stage 4G executes it as the designated refresh stage with Stage 4B cookie candidate source records and
existing cookie targets. The manifest view uses raw UTF-8 strings and SHA-256 only unless a future
manifest explicitly declares otherwise. The run found `0` exact matches from `8` comparisons.

Every generated candidate record logs the exact literal string before UTF-8 encoding, byte variant, byte-string SHA-256, target cookie, digest, and exact-match status. Partial and fuzzy hash matches are out of scope.

An exact SHA-256 match would be an `exact_preimage_candidate`, not a Liber Primus solve claim.
Without new exact source strings, the SHA-256 cookie pack family remains negative/deprioritised.
