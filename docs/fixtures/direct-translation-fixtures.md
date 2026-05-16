# Direct-Translation Fixtures

## Direct Translation Definition

Direct translation maps each rune token to the preferred Latin label in `gematria-primus-v0`. It uses no key, no shift, no Atbash, no Vigenere, and no prime stream.

## Sections In Scope

- `the-loss-of-divinity`
- `some-wisdom`
- `an-instruction-direct`
- `p57-parable`

## Normalization Policy

Preferred Latin labels are uppercase. Word separators become spaces. Clause separators become `. `. Visual line separators and physical newlines are joined. Numeric literals are preserved. Repeated whitespace collapses and output is trimmed.

## Fixture List

Fixtures live under `data/fixtures/solved-pages/direct-translation-v0/`.

## Expected Outputs And Hashes

Expected normalized strings are small committed test expectations with SHA-256 hashes. They use profile labels such as `U` and `C` rather than editorially rewriting to English spellings.

## Reproduction Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture stage1a-smoke --fixture-dir data/fixtures/solved-pages/direct-translation-v0 --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate --out-dir data/normalized/solved-baselines/direct-translation-v0 --allow-pending --allow-warnings
```

## Current Status

The current direct-translation fixture set has four passing fixtures and no pending fixtures.

## Known Caveats

Page boundaries remain reviewable, the corpus candidate is inactive, and direct translation does not cover reverse Gematria, Vigenere, or prime-derived solved sections.
