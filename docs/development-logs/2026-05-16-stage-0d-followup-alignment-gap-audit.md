# Stage 0D-followup Alignment Gap Audit Developer Log

## Task Summary

Implemented Stage 0D-followup diagnostics for transcript alignment gaps, bounded stream/logical-line matching, and stricter page-boundary confidence auditing.

## Starting Branch and Commit

- branch: `main`
- starting commit: `f13e164bf0fcca15e754cadb885f3414522ade9c`
- target GitHub repo: `NoxxGames/LiberPrimus-GPU`
- origin normalized from the moved `LiberPrimusSolver` URL to `https://github.com/NoxxGames/LiberPrimus-GPU.git` after GitHub verified both resolve to the same repository.

## Existing Stage 0C and Stage 0D Source Status

- Pastebin raw TXT present: `data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`
- rtkd raw transcript present: `data/raw/transcripts/rtkd/liber-primus__transcription--master.txt`
- scream314 raw reference present: `data/raw/transcripts/scream314/liber_primus.md`
- raw files are ignored and were not staged.
- `LiberPrimus-Research-Report.md` remains ignored, untracked, and unstaged.

## Reproduced Baseline

The Stage 0D baseline was reproduced before code changes:

- transcript physical lines: 931
- Pastebin line pairs: 185
- alignment records: 185
- exact / high / medium / low / none: 1 / 1 / 28 / 2 / 153
- page-boundary candidates: 74
- high-confidence boundaries: 74
- Parable candidate: true

## Parser and View Design

Added `transcript_sources/views.py` with:

- physical line view;
- rune stream view with offset-to-line/column mapping;
- logical line view split on slash terminators and markers;
- page marker view;
- candidate LP2 span view.

Views preserve raw text and raw glyphs and set `trusted_as_canonical=false`.

## Alignment Algorithm Design

Added bounded deterministic matching passes:

- physical-line exact;
- logical-line exact;
- stream-subsequence exact;
- documented variant-normalized stream matching;
- decimal-index stream matching;
- bounded neighbor support;
- word-length tie-breaking only.

The implementation uses hash maps and n-gram indexes. It does not add CUDA, brute force, unbounded all-vs-all matching, or unbounded dynamic programming.

## Gap Taxonomy

Added `alignment/gap_analysis.py` and generated `alignment_gap_diagnostic` records with reason labels for matched, variant, stream-subsequence, segmentation, ambiguous, empty, and unknown cases.

## Boundary Confidence Tightening

Added `alignment/boundary_audit.py` and tightened `page_boundaries.py`:

- empty-pair-only evidence cannot be high confidence;
- word-length-only evidence cannot be high confidence;
- explicit markers require nearby strong alignment for high confidence;
- Parable anchor requires alignment support for high confidence;
- all candidates remain `canonical_page_boundary=false`;
- overgeneration is flagged.

## Glyph `ᛂ` Status

The raw glyph is preserved. The normalized view remains documented-only as `ᛂ -> ᛄ` when supported by observed prime value 37. No canonical Gematria mapping was changed.

## Follow-up Smoke Result

Real-source follow-up smoke:

- transcript physical lines: 931
- transcript logical lines: 798
- transcript rune stream length: 15933
- Pastebin line pairs: 185
- exact / high / medium / low / none: 52 / 129 / 0 / 2 / 2
- no-match reduction: 151
- logical-line matches: 0
- stream-subsequence matches: 181
- decimal-index matches: 0
- variant-normalized matches: 129
- boundary high / medium / low / none: 50 / 3 / 21 / 0
- overgeneration warning: true
- glyph variant observations: 1

Generated outputs were written under `data/normalized/alignment/` and were not staged.

## Tests Run

Added synthetic tests for transcript views, stream alignment, gap analysis, boundary audit, CLI commands, and real-source conditional follow-up smoke.

Validation commands are recorded in the final task report.

## Git Safety Result

Raw files, generated alignment outputs, `.venv`, build outputs, and `LiberPrimus-Research-Report.md` are not staged. Only explicit source, test, documentation, tutorial, and log files are intended for staging.

## GitHub Issue Update

Issue `#1` (`Stage 0D-followup: resolve transcript-alignment gaps and boundary confidence`) was found in `NoxxGames/LiberPrimus-GPU`. A status comment was added with the baseline, follow-up counts, gap taxonomy, boundary audit, remaining limitations, and the recommendation to keep the issue open for human review. Labels `stage-0d`, `alignment`, and `needs-human-review` were confirmed.

## Files Created or Updated

- alignment and transcript-view Python modules;
- Stage 0D-followup CLI commands;
- Stage 0D-followup tests;
- research docs;
- developer and research logs;
- policy/status/tutorial docs.

## Known Limitations

Two records remain unmatched and two remain low confidence. Boundary candidates are still overgenerated relative to expected LP2 page count, so human review remains required before corpus freeze.

## Next Recommended Stage

If the remaining gap count is acceptable, proceed to Stage 0E to freeze the Gematria profile and separator grammar. Otherwise run Stage 0D-followup-2 to manually inspect remaining unmatched spans and segmentation policy.
