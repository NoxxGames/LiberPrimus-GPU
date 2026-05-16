# Canonical Corpus v0 Candidate

## Status

Generated candidate only. `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Corpus Candidate ID

`rtkd-master-v0-candidate`

## Source Transcript

`rtkd-master-transcription`

Source SHA-256: `e21743ccd9a07f3845d52a329c61b9fa69e9ca6a44ee3ba0db8f28a0d7065004`

## Profiles Used

- Gematria: `gematria-primus-v0`
- Separator grammar: `rtkd-separator-grammar-v0`
- Glyph variants: `glyph-variants-v0`

## Output Files

Generated outputs are ignored under:

`data/normalized/corpus-candidates/rtkd-master-v0-candidate/`

Files include manifest, tokens, lines, page candidates, warnings, separator inventory, and summary.

## Manifest Fields

The manifest records source SHA-256, profile IDs and SHA-256s, generator version, git commit, counts, warnings, and non-activation flags.

## Token Record Model

Token records preserve raw text, token kind, source positions, rune index/prime metadata where applicable, variant mapping metadata, and `trusted_as_canonical=false`.

## Line Record Model

Line records summarize logical lines, token ranges, rune indices, prime values, separator counts, source physical line spans, and signature hashes.

## Page Candidate Model

Page candidates are imported from Stage 0D-followup boundary diagnostics as reviewable metadata only. They keep `canonical_page_boundary=false` and `page_boundaries_final=false`.

## Current Real-Source Counts

- physical lines: 931
- logical lines: 1729
- tokens: 22382
- rune tokens: 15933
- separator tokens: 5795
- numeric literals: 344
- unknown symbols: 310
- variant-mapped tokens: 0
- page candidates: 74
- warnings: 311

## Before Activation

Activation requires human review of page candidates, solved-page golden fixtures, separator policy review, provenance review, and CI validation.
