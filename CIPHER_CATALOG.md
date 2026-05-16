# Cipher Catalog

## Purpose

This catalog records planned transform families and the standards required before implementation.

## Stage 0A status

No real cipher modules are implemented in Stage 0A. Placeholder modules return smoke statuses only.

Stage 0B legacy workbook ingestion does not implement real cipher modules. It only extracts non-canonical hint records.

Stage 0C local Pastebin ingestion does not implement cipher modules. It only validates legacy rune/prime-value serialization.

Stage 0D transcript alignment does not implement cipher modules. It prepares corpus views and alignment hints for future transforms only.

## Future transform registry

Later stages should register transforms with stable IDs, CPU reference behavior, parameters, inverse behavior when available, and test vectors.

## Direct translation

Direct rune-to-symbol translation must wait for a frozen Gematria profile and transcript policy.

The workbook can support future tests for direct translation, reverse Gematria, and rotated reverse Gematria. These modules remain unimplemented unless added in a later stage.

## Mod-29 Caesar

A mod-29 Caesar transform will need explicit alphabet order, wrap rules, and known controls.

## Atbash

Atbash variants must define alphabet order and whether digits, spaces, and punctuation are in scope.

## Affine mod 29

Affine transforms must validate invertibility and define parameter enumeration policy.

## Repeating-key Vigenere

Repeating-key transforms require key-source policy, length limits, and null controls.

The legacy workbook supports future tests for Vigenere `DIVINITY` and `FIRFUMFERENFE`, but these modules are not implemented by Stage 0B.

## Prime / phi-prime stream

Prime-derived streams must define sequence generation, indexing, offset, modulus, and reproducible fixtures.

Prime values from the local Pastebin source must be converted to decimal indices before any future modulo-29 cipher operation.

Transcript alignment records may contain decimal-index views for comparison, but cipher transforms must still wait for a frozen Gematria profile and canonical transcript policy.

Public docs must not describe planned or placeholder cipher modules as implemented solver functionality.

The workbook supports future tests for a prime-minus-one stream, including p56 hint checks. This is not a canonical corpus claim.

## Prime-gap stream

Prime-gap transforms must define gap source, indexing, modulus, and expected controls.

## Length-derived streams

Length-derived streams must document which text length and normalization rules feed the stream.

## Simple transpositions

Transpositions must define grid shape, padding, direction, and incomplete-row policy.

## Composition engine

Composed transforms need manifest serialization and full replay. A flexible engine without controls is a false-positive risk.

## Do-not-start-with list

Do not start with brute force, page-specific hacks, GPU-only transforms, or transforms whose CPU reference cannot be tested.

## Stage 0D-followup reminder

Transcript alignment prepares corpus views for future transform work, but it does not implement cipher modules. Prime values from legacy sources must still be converted to decimal indices before any modulo-29 transform. Public docs must not describe planned transform families as implemented.
