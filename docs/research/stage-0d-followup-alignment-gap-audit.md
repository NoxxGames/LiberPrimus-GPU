# Stage 0D-followup Alignment Gap Audit

## Status

Stage 0D-followup is a non-canonical diagnostic stage. It improves alignment evidence and boundary confidence labels, but it does not activate a canonical corpus and does not prove any plaintext.

## Problem Statement

Stage 0D aligned the 185 legacy Pastebin line-pairs against rtkd physical transcript lines. That view produced 153 no-match records and 74 high-confidence boundary candidates. Those two facts were inconsistent: boundary confidence was too strong for the observed line-pair coverage.

## Previous Stage 0D Baseline

The reproduced real-source baseline was:

- rtkd physical lines: 931
- Pastebin line pairs: 185
- alignment records: 185
- exact / high / medium / low / none: 1 / 1 / 28 / 2 / 153
- page-boundary candidates: 74
- high-confidence boundary candidates: 74
- Parable boundary candidate: true

## Why Physical-Line Matching Was Insufficient

The rtkd source is not guaranteed to use the same segmentation as the Pastebin source. Pastebin rows may correspond to logical slash-delimited lines or to contiguous subsequences inside a larger rune stream. Stage 0D physical-line matching therefore undercounted valid alignments.

## Transcript Views Added

Stage 0D-followup adds deterministic transcript views:

- physical line view
- logical line view split on documented line terminators
- flattened rune stream view with source offset mapping
- page marker view
- candidate LP2 span view when a contiguous span can be found

All views preserve raw glyphs and source line/column mapping and remain `trusted_as_canonical=false`.

## Improved Alignment Passes

The follow-up matcher uses bounded indexed passes:

- physical-line exact matching
- logical-line exact matching
- stream-subsequence exact matching
- documented variant-normalized stream matching
- decimal-index stream matching
- bounded neighbor support
- word-length tie-breaking only, never high confidence by itself

No unbounded all-vs-all search or dynamic programming is used.

## Gap Taxonomy

Gap diagnostics classify pairs with labels including:

- `matched_exact`
- `matched_variant_normalized`
- `matched_decimal_index`
- `segmentation_mismatch_possible`
- `stream_subsequence_match_possible`
- `glyph_variant_possible`
- `duplicate_signature_ambiguous`
- `empty_pair`
- `unknown`

## New Alignment Results

The real-source follow-up smoke produced:

- alignment records: 185
- exact / high / medium / low / none: 52 / 129 / 0 / 2 / 2
- no-match reduction: 151
- stream-subsequence matches: 181
- variant-normalized matches: 129
- unresolved records: 4, including empty and ambiguous records

These records are generated diagnostics and are ignored by Git.

## Boundary Audit

Boundary confidence now accounts for explicit markers, local alignment coverage, anchors, no-match density, ambiguity, and overgeneration. Empty-pair-only and word-length-only evidence cannot produce high confidence.

The real-source audit produced:

- boundary candidates: 74
- high / medium / low / none: 50 / 3 / 21 / 0
- overgeneration warning: true
- canonical page boundary: false for every candidate

## Glyph Variant Status

Glyph `ᛂ` remains raw-preserved. The normalized view may map it to candidate `ᛄ` only when the prime-value evidence is recorded. The canonical Gematria mapping was not changed.

## Performance/Timing Note

Timing metadata is recorded for diagnostics only. The real-source follow-up smoke completed in a few seconds on ordinary CPU hardware. Timing is not a benchmark record.

## Remaining Unresolved Pairs

Two records still have no match and two remain low confidence. These should be inspected manually before any corpus freeze.

## What This Stage Does Not Prove

This stage does not solve any unsolved page, does not prove page boundaries, does not activate a canonical transcript, and does not make legacy Pastebin rows canonical.

## Next Recommended Stage

If the remaining ambiguous records are acceptable for policy work, proceed to Stage 0E to freeze the Gematria profile and separator grammar. If not, run Stage 0D-followup-2 to manually inspect remaining unmatched spans and segmentation choices.
