# Atbash-Family Fixtures

## Purpose

Atbash-family fixtures are known-solved regression tests for reverse Gematria and rotated reverse Gematria. They are test expectations, not solve claims.

## Fixture List

| Fixture ID | Method | Rotation | Status |
| --- | --- | ---: | --- |
| `a-warning-reverse-gematria` | `reverse_gematria` | none | pass |
| `a-koan-a-man-rotated-reverse-gematria` | `rotated_reverse_gematria` | 3 | pass |
| `an-instruction-rotated-reverse-gematria` | `rotated_reverse_gematria` | 3 | pass |

## Formulas

Reverse Gematria:

```text
decoded_index = 28 - cipher_index
```

Rotated reverse Gematria:

```text
decoded_index = (28 - cipher_index + rotation) mod 29
```

Rotations must be declared in the fixture. Stage 1B does not infer or search rotations.

## Expected Text And Hashes

Expected normalized text is stored only as controlled fixture text with provenance and SHA-256 hashes. It uses Gematria profile preferred Latin labels, so profile spellings may differ from conventional English rendering.

## Reproduction Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture stage1b-smoke `
  --direct-fixture-dir data/fixtures/solved-pages/direct-translation-v0 `
  --atbash-fixture-dir data/fixtures/solved-pages/atbash-family-v0 `
  --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate `
  --direct-out-dir data/normalized/solved-baselines/direct-translation-v0 `
  --atbash-out-dir data/normalized/solved-baselines/atbash-family-v0 `
  --allow-pending `
  --allow-warnings
```

Generated reproduction records are ignored and must not be committed.

## Caveats

All spans remain reviewable. `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false` remain required.
