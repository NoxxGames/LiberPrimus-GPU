# Vigenere Fixtures

## Purpose

Stage 1C Vigenere fixtures are known-solved test expectations. They are not new solve claims and do not activate the corpus.

## Fixture List

- `welcome-divinity-vigenere`
- `a-koan-during-firfumferenfe-vigenere`

## Explicit-Key Vigenere Formula

`decoded_index = (cipher_index - key_index[key_position]) mod 29`

Key position advances only on enciphered rune tokens.

## Declared Keys

- Welcome: `DIVINITY`
- A Koan: During: `FIRFUMFERENFE`

## Skip Rules

Both fixtures declare `cleartext_f_pass_through`. The manifests include explicit token indices for the pass-through `F` tokens. The rule is not global.

## Expected Text And Hashes

- Welcome SHA-256: `06b270b815d7c9e55ec2a68dc93ee7738d058d109a7032701e0ee2bf5bb14d52`
- A Koan: During SHA-256: `05d763dea5efcfc30368409a2250338337c16de68f12e4e80888f61e00ff2461`

Expected text is small committed test data with locked-reference provenance.

## Reproduction Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture reproduce-vigenere `
  --fixture-dir data/fixtures/solved-pages/vigenere-v0 `
  --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate `
  --out-dir data/normalized/solved-baselines/vigenere-v0 `
  --allow-pending `
  --allow-warnings
```

## Current Status

Current real-source result: `2` pass, `0` fail, `0` pending, `0` skipped.

## Known Caveats

The normalized output uses Gematria profile preferred Latin labels, so `V` is represented as `U`, `K` as `C`, and some `NG` sequences appear as `ING`. Page spans remain reviewable.
