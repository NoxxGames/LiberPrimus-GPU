# Cipher Catalog

## Purpose

This catalog records planned transform families and the standards required before implementation.

## Stage 0A status

No real cipher modules are implemented in Stage 0A. Placeholder modules return smoke statuses only.

## Future transform registry

Later stages should register transforms with stable IDs, CPU reference behavior, parameters, inverse behavior when available, and test vectors.

## Direct translation

Direct rune-to-symbol translation must wait for a frozen Gematria profile and transcript policy.

## Mod-29 Caesar

A mod-29 Caesar transform will need explicit alphabet order, wrap rules, and known controls.

## Atbash

Atbash variants must define alphabet order and whether digits, spaces, and punctuation are in scope.

## Affine mod 29

Affine transforms must validate invertibility and define parameter enumeration policy.

## Repeating-key Vigenere

Repeating-key transforms require key-source policy, length limits, and null controls.

## Prime / phi-prime stream

Prime-derived streams must define sequence generation, indexing, offset, modulus, and reproducible fixtures.

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
