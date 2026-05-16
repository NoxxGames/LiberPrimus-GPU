# Legacy Google Sheet Workbook

## Status: Non-canonical legacy analysis source

`tranlsations.xlsx` is a non-canonical legacy analysis workbook. It is useful for extraction, validation hints, and later test design, but it is not canonical corpus data and is not proof of any unsolved plaintext.

## Source

The workbook is associated with Google Sheet ID `1JwbWW04y1Fy5Qvwca7B2e3dsFWd5rf3NSorFj53IBNE`.

## Local filename

The local filename is intentionally misspelled as `tranlsations.xlsx`. Preserve that spelling in metadata.

## Workbook lock metadata

Committed lock metadata lives under `data/locks/legacy-workbooks/`. The raw workbook belongs under `data/raw/legacy-workbooks/` and remains ignored by Git.

## Expected sheets

- `README`
- `Prime Sums`
- `A Warning`
- `Some Wisdom`
- `Welcome`
- `A Koan A Man`
- `The Loss Of`
- `A Koan During`
- `An Instruction`
- `p57 Parable`
- `p56 An End`

## Sheet classifications

`README` is classified as `readme`. `Prime Sums` is classified as `prime_sums`. The other known sheets are classified as `solved_delta_sheet`.

## What the workbook is useful for

The workbook can support sheet inventory, solved-page delta extraction, Prime Sums extraction, formula inventory, hypothesis generation, and golden-fixture hints for later solved-page reproduction.

## What the workbook must not be used for

Do not use it as canonical corpus, proof of unsolved-page plaintext, final Gematria mapping, direct GPU campaign input, or evidence of a solve by itself.

## Solved delta extraction model

The parser finds `Line N` blocks, then aligns nearby `Cipher Rune`, `Gematria Position`, `Message Rune`, `Gematria Position`, `Cipher-Message`, and `Message - Cipher` rows. It emits one record per visible aligned position and preserves source row and column coordinates.

Records with trailing blanks are skipped. Records with partial aligned values are emitted with warnings so the original workbook state remains visible.

## Prime Sums extraction model

The parser treats `Prime Sums` as alternating token rows and numeric rows. It preserves token cells as whole tokens and does not split transliterations such as `TH`, `EA`, `EO`, `(I)NG`, `IU`, `U`, or `V`.

## Formula inventory model

The workbook is loaded with formulas and cached values. Formula text is inventoried; formulas are not recalculated. Missing cached values are recorded as `null`.

## Validation rules

For numeric solved-delta records, the parser checks `(cipher_index - message_index) % 29` and `(message_index - cipher_index) % 29` against workbook delta cells. Validation warnings do not rewrite source values.

## Known caveats

Spreadsheet rows are not solves. The workbook contains legacy analysis claims and page-to-page shift pattern notes that remain unverified. Prime Sums rows and formula cells are hints, not source truth.

## Next-stage uses

Later stages may use workbook-derived records as solved-fixture hints while building canonical corpus locks, transcript policy, and Gematria profile metadata from primary sources.
