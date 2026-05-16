# Transcript Alignment Policy

## Purpose

Stage 0D aligns non-canonical legacy Pastebin line pairs with transcript-source lines to produce reviewable alignment hints.

## Inputs

Inputs are the ignored raw Pastebin TXT, the ignored rtkd master transcript candidate, and optional scream314 reference metadata.

## Matching Passes

The implementation builds signature indexes for raw rune sequences, documented variant-normalized rune sequences, decimal-index sequences, and bounded rune-subsequence lookups. It does not run unbounded all-vs-all fuzzy matching.

## Confidence Labels

Labels are `exact`, `high`, `medium`, `low`, and `none`.

`exact` requires a unique exact raw rune-sequence match. `high` allows a unique documented variant-normalized match. `medium` covers decimal-index or bounded subsequence matches. `low` indicates ambiguity. `none` means no deterministic match.

## Boundary Inference

Boundary candidates may use rtkd `%` source markers, alignment neighborhoods, preserved empty pairs, and the final Parable anchor. They are tentative records only.

## Performance Policy

Stage 0D uses deterministic hash/signature indexes and records elapsed milliseconds for parsing, signature building, matching, boundary inference, and glyph-variant summarization. Timing metadata is for regression awareness, not benchmark claims.

## Generated Records

Generated outputs include `transcript_line`, `pastebin_transcript_alignment`, `lp2_page_boundary_candidate`, `glyph_variant_observation`, and `stage0d_alignment_summary` records.

## Non-Canonical Status

All alignment-derived records must set `trusted_as_canonical=false`. Boundary records must set `canonical_page_boundary=false`.

## Review Process

Human review must inspect unmatched and ambiguous regions before any corpus-freeze stage uses alignment records.

## Known Limitations

The real Stage 0D smoke aligns only part of the Pastebin source deterministically. Many Pastebin line pairs remain unmatched against rtkd physical lines and need follow-up alignment work.
