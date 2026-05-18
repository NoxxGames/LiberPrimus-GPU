# Stage 3U Cookie Signed-Variant Pack Development Log

## Purpose

Stage 3U executes only `EXP-3R-001`, the cookie SHA-256 signed-variant manifest created in Stage 3R.

## Initial State

- Local HEAD matched `origin/main` at `d33683101371b02ace82340cbd37d4590f45ed41`.
- Stage 3T CI run `26049794499` passed.
- The Stage 3U manifest, Stage 3K/3L cookie records, hash-preimage package, and post-Discord package were present.
- Raw Discord logs and raw page images were present locally but were not processed.
- Existing consistency, public-docs, lock-hash, workflow, and Wiki source checks passed before edits.

## Policy

Stage 3U may execute the manifest because it is bounded, CPU-only, SHA-256-only, and generated-output-ignored. The stage must not run hashcat, CUDA, external dictionaries, fuzzy matching, live Tor, raw Discord processing, image processing, canonical corpus activation, page-boundary finalization, or solve claims.

## Implementation

- Added `python/libreprimus/post_discord/cookie_signed_variant_pack.py`.
- Added CLI commands:
  - `post-discord validate-cookie-manifest`
  - `post-discord run-cookie-signed-variants`
  - `post-discord cookie-signed-summary`
- Added Stage 3U consistency checks for manifest validation and ignored generated outputs.

## Local Run

- Target cookies: `2`
- Base strings: `13`
- Byte variants: `12`
- Generated candidates before deduplication: `156`
- Candidates after deduplication: `105`
- Duplicate byte-string candidates: `51`
- Target comparisons: `210`
- Exact SHA-256 matches: `0`

Generated outputs remain ignored under `experiments/results/post-discord/stage3u/`.

## Documentation And Validation

- Updated Stage 3U experiment, research, CLI, web-cookie, README/status/roadmap, tutorial, Wiki-source, testing, schema, and agent-policy documentation.
- Focused Stage 3U tests passed: `12 passed`.
- Full Python tests passed: `801 passed`.
- Ruff passed for `python/libreprimus` and `tests/python`.
- CLI smoke, consistency checks, CI scripts, lock verification, workflow validation, Wiki source validation, and Wiki dry-run generation passed locally.
