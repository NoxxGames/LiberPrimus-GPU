# Cookie Hash Preimage Packs

Stage 3L defines two explicit SHA-256-only candidate packs for the archived 2013 cookie/hash artefacts:

- `hist_cookie_literal_pack_v1`
- `hist_cookie_base29_numeric_pack_v1`

The packs live under `data/observations/web/hash-preimage-candidate-packs/`. They are curated, bounded, and inspectable. They do not import external dictionaries, recurse over phrase combinations, run hashcat, use GPU acceleration, or test non-SHA-256 algorithms.

Every generated candidate record logs the exact literal string before UTF-8 encoding, byte variant, byte-string SHA-256, target cookie, digest, and exact-match status. Partial and fuzzy hash matches are out of scope.

An exact SHA-256 match would be an `exact_preimage_candidate`, not a Liber Primus solve claim.
