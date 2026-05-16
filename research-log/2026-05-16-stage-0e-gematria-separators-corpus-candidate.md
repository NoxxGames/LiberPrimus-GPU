# Stage 0E Profile Freeze and Corpus Candidate Research Log

Stage 0E freezes tooling profiles but does not activate a final canonical corpus.

Frozen profiles:

- `gematria-primus-v0`
- `glyph-variants-v0`
- `rtkd-separator-grammar-v0`

The Gematria profile defines the 29-entry rune/index/prime mapping and excludes `ᛂ` as a canonical rune. The glyph variant profile documents `ᛂ -> ᛄ` as normalized-view-only with raw preservation. The separator grammar preserves rtkd-style separators as tokens and explicitly prevents `%` and `/` from becoming final page boundaries.

The rtkd master corpus candidate generated from the local locked transcript has 931 physical lines, 1729 logical lines, 22382 tokens, 15933 rune tokens, and 74 reviewable page candidates. It remains a generated candidate with `canonical_corpus_active=false`.

Remaining research work:

- review page-candidate overgeneration;
- add solved-page golden fixtures;
- reproduce direct-translation solved pages;
- decide whether corpus candidate records can be promoted in a later activation stage.
