# 2026-05-16 Stage 0C Legacy Pastebin Ingestion

## Summary

Stage 0C ingested the local `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt` source as a non-canonical legacy LP2 rune/prime-value artefact.

## Source status

The local TXT was moved to `data/raw/legacy-pastebins/` and ignored by Git. Lock metadata was committed under `data/locks/legacy-pastebins/`.

## Interpretation

Rows alternate between rune word groups and nested Gematria prime-value arrays. Numeric rows are prime values, not decimal modulo-29 indices.

## Validation

A Python-only `legacy_validation_gematria_primus_v0` profile validates the 29 Gematria prime values and converts them to decimal indices for generated records. Unknown glyph variants are warnings, not silent corrections.

## Anchor status

The final Parable rune word anchor is detected as a non-authoritative alignment hint. Page boundaries remain not finalized.

## Non-goals

No canonical transcript was created. No unsolved-page cryptanalysis was attempted. No CUDA code changed.

## Next

Stage 0D should align legacy Pastebin line pairs with primary transcript/page-image sources and assign tentative page-boundary confidence labels.
