# Stage 1B Atbash-Family Golden Fixtures Developer Log

## Initial State

- Branch: `main`
- Starting commit: `201e1a0da8dc5715514dc0823b68f89f38f0f52e`
- Target GitHub repo: `NoxxGames/LiberPrimus-GPU`
- Origin: `https://github.com/NoxxGames/LiberPrimus-GPU.git`
- Raw rtkd, scream314, and legacy Pastebin files present and ignored.
- Stage 0E profile hashes matched the expected hashes.
- Stage 1A fixture framework and direct fixture set were present.
- Raw files staged: `0`
- Generated outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`

## Task Summary

Implemented CPU-only reverse Gematria and rotated reverse Gematria reproduction for known solved fixtures. This stage adds no search, no CUDA, no Vigenere, no prime stream, no corpus activation, and no page-boundary finalization.

## Fixture And Output Directories

- Added `data/fixtures/solved-pages/atbash-family-v0/`.
- Added ignored output path `data/normalized/solved-baselines/atbash-family-v0/`.
- Added `.gitignore` exceptions for the atbash output directory `.gitkeep` only.

## Schema And Model Updates

- Preserved Stage 1A fixture compatibility.
- Kept method families for `reverse_gematria` and `rotated_reverse_gematria`.
- Added reproduction record support for `decoded_index_formula` and `transform_parameters`.
- Preserved `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Transform Implementation

- Added `reverse_gematria_index`: `decoded_index = 28 - cipher_index`.
- Added `rotated_reverse_gematria_index`: `decoded_index = (28 - cipher_index + rotation) mod 29`.
- Rotation must be declared in fixture manifests.
- No rotation discovery or brute-force behavior was implemented.

## Fixtures

- `a-warning-reverse-gematria`: passing intended, explicit logical-line range `10..27`.
- `a-koan-a-man-rotated-reverse-gematria`: passing intended, explicit logical-line range `110..190`, rotation `3`.
- `an-instruction-rotated-reverse-gematria`: passing intended, explicit logical-line range `192..196`, rotation `3`.

## Smoke Result

- Direct regression: `4/0/0/0` pass/fail/pending/skipped.
- Atbash-family: `3/0/0/0` pass/fail/pending/skipped.
- Generated outputs path: `data/normalized/solved-baselines/atbash-family-v0/`.
- Generated outputs staged: `0`.

## Tests

Added Stage 1B transform, schema, reproduction, CLI, and real-source conditional tests.

- Pytest: `126 passed`.
- Ruff: passed.
- C++ tests: skipped because this was a Python/docs/fixture-transform stage.

## GitHub Issue Update

Issue `#5` (`Implement CPU transform registry and baseline cipher modules`) was found and updated with a Stage 1B status comment. Labels `stage-1`, `testing`, `needs-human-review`, and `ciphers` were applied or confirmed. The issue remains open because Vigenere, prime streams, generic affine/search, scoring, and broader transform registry work remain incomplete.

## Git Safety

Final pre-commit validation confirmed:

- Raw transcript and Pastebin files are ignored.
- Generated corpus candidate outputs are ignored.
- Generated Atbash-family solved-baseline JSON/JSONL outputs are ignored.
- `LiberPrimus-Research-Report.md` is not tracked or staged.
- `.venv` and build outputs are not staged.
- Only fixture metadata, Python source, tests, docs, schema, README/.gitkeep, and logs are intended for staging.

## Known Limitations

Stage 1B does not implement Vigenere, prime streams, generic affine search, scoring, CUDA kernels, or any unsolved-page search.

## Next Recommended Stage

Stage 1C: explicit-key Vigenere solved-page reproduction for locked references only.
