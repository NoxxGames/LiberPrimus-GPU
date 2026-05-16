# Legacy Pastebin vGMK330j

## Status: Non-canonical legacy LP2 rune/prime-value source

The local file `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt` is a non-canonical legacy LP2 rune/prime-value source. It is not a canonical transcript and is not decrypted plaintext.

## Public source URL

Public source: `https://pastebin.com/vGMK330j`

Raw URL reference: `https://pastebin.com/raw/vGMK330j`

## Local filename

The committed metadata preserves the local filename `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`.

## Local raw path

The local raw source belongs at `data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt` and is ignored by Git.

## Lock metadata

Checksum and provenance metadata live under `data/locks/legacy-pastebins/`.

## What the rows represent

The source uses alternating rows. A rune row contains comma-separated rune word groups. The following numeric row contains nested arrays of prime values aligned to those word groups.

## Why the numeric rows are Gematria prime values

The numeric rows contain Gematria Primus prime values such as `53`, `23`, and `67`, not decimal alphabet positions.

## Difference between prime values and decimal modulo-29 indices

Prime values must be converted through the Gematria profile inverse lookup before modulo-29 operations. For example, prime value `53` maps to decimal index `15`.

## Parser model

The parser reads UTF-8 text, preserves source line numbers and raw line text, parses alternating rune/prime rows, preserves `{}` empty pairs, and emits one `legacy_pastebin_line_pair` record per pair.

## Validation model

Stage 0C uses `legacy_validation_gematria_primus_v0`, a Python-only validation profile. It validates glyph prime values, detects unknown glyphs, records alias inference warnings when the observed prime value is known, and never silently changes source glyphs.

## Empty row handling

Literal `{}` records are preserved as empty line pairs. They are structural hints only and are not page boundaries.

## Page-boundary limitations

The source has no page labels. Page boundaries are not finalized in Stage 0C.

## Anchor inference

Anchor detection is non-authoritative. It emits hints only and sets `canonical_page_boundary=false`.

## Known solved final-page anchor

The parser detects the rune word `ᛈᚪᚱᚪᛒᛚᛖ` as a high-confidence final Parable alignment hint for `57.jpg`, without assigning corpus-wide page boundaries.

## What this source is useful for

The source is useful for parser validation, rune/prime alignment checks, empty-row preservation, future transcript alignment, and tentative anchor hints.

## What this source must not be used for

Do not use it as canonical corpus, decrypted plaintext, proof of a solve, final page-boundary evidence, direct GPU campaign input, or a final Gematria mapping authority.

## Generated outputs

Generated outputs live under `data/normalized/legacy-pastebin/` and remain ignored by Git.

## Next-stage alignment with canonical transcript

Stage 0D should align legacy line pairs with primary transcript and page-image sources using confidence labels before any canonical transcript policy is frozen.
