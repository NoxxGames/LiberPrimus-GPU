# Stage 0D-followup Alignment Gap Audit

Stage 0D-followup rechecked the Stage 0D physical-line alignment and confirmed the baseline problem: 153 of 185 Pastebin line-pairs had no match while all 74 boundary candidates were marked high confidence.

The follow-up adds logical-line and rune-stream transcript views, then aligns Pastebin line-pairs using bounded signature and subsequence passes. The real-source smoke result improved alignment coverage to 52 exact, 129 high, 0 medium, 2 low, and 2 none. The no-match reduction is 151.

Boundary confidence is now stricter. The boundary audit reports 50 high, 3 medium, 21 low, and 0 none, with an overgeneration warning because 74 candidates still exceed the expected LP2 page count. Every boundary remains non-canonical.

Glyph `ᛂ` remains a raw-preserved variant with normalized-view-only handling toward candidate `ᛄ` under prime-value evidence 37. No canonical Gematria mapping was changed.

Remaining research questions:

- whether the two unmatched records are source defects, parser limitations, or structural rows;
- whether 50 high-confidence marker candidates should be further downgraded before corpus freeze;
- whether rtkd logical segmentation or Pastebin line-pair structure should drive LP2 page policy;
- how to reconcile overgenerated boundary candidates before canonical corpus v0.

This stage did not solve any page, activate a canonical corpus, or finalize page boundaries.
