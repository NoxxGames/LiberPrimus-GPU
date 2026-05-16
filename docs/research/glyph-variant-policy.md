# Glyph Variant Policy

## Status

Stage 0D defines a normalized-view policy for glyph variant `ᛂ`. It does not change canonical Gematria mapping.

## Observed Issue

Stage 0C found `ᛂ` in the local Pastebin TXT. The legacy validation profile does not include that glyph.

## Stage 0C Evidence

Stage 0C recorded 453 alias warnings for `ᛂ`, all with observed prime value `37`.

## Stage 0D Alignment Evidence

Stage 0D emits one `glyph_variant_observation` record for `ᛂ` with occurrence count `453`. The real-source alignment has limited transcript support and preserves all raw glyphs.

## Prime-Value Evidence

Prime value `37` maps to decimal index `11`, Latin label `J`, and canonical candidate glyph `ᛄ` in `legacy_validation_gematria_primus_v0`.

## Transcript Evidence

When a transcript line match supports the normalized view, the output records the matched transcript glyphs. This is supporting evidence only.

## Normalized-View Rule

A generated normalized view may map `ᛂ -> ᛄ` only when the observed prime value is `37`, the mapping is explicitly recorded, and output records set `variant_mapping_applied=true` where applicable.

## Raw Preservation Rule

Raw records must preserve `ᛂ`. Source records must not rewrite raw glyphs in place.

## Why This Is Not a Canonical Mapping Change

Stage 0D has not frozen a canonical Gematria profile. The mapping is a documented alignment view, not a source-truth change.

## Tests

Tests verify raw glyph preservation, normalized-view mapping, `variant_mapping_applied=true` where applicable, and no mutation of the validation profile.
