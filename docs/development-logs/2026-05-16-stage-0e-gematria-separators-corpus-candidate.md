# Stage 0E Gematria, Separators, and Corpus Candidate Developer Log

## Task Summary

Created frozen tooling profiles for Gematria Primus, rtkd separators, and glyph variants, then generated an rtkd master corpus v0 candidate while keeping canonical corpus activation false.

## Starting Branch and Commit

- branch: `main`
- starting commit: `1d2ce141d34ba70a46e84ba2831dfddd535f6494`
- target repo: `NoxxGames/LiberPrimus-GPU`
- raw sources and locks were present.
- `LiberPrimus-Research-Report.md` remained ignored and unstaged.

## Directories and Ignore Policy

Added committed profile and schema directories under `data/profiles/` and `schemas/corpus/`. Added ignored generated corpus candidate output policy under `data/normalized/corpus-candidates/`.

## Gematria Profile

- profile: `data/profiles/gematria/gematria-primus-v0.json`
- SHA-256: `93577209028c964523068b5975180e05bda5b1a07b2675d4e35d03d6d164c5c2`
- entries: 29
- `canonical_profile_active=true`
- `canonical_corpus_active=false`
- `ᛂ` is not a canonical Gematria rune.

## Glyph Variant Profile

- profile: `data/profiles/glyph-variants/glyph-variants-v0.json`
- SHA-256: `5acae61c4ea2aa9f2f2fb76bdcafb7ed9c6504bd98caf29590a95d7d43271d6d`
- variant count: 1
- `ᛂ -> ᛄ` is normalized-view only.
- canonical mapping changed: false.

## Separator Grammar

- profile: `data/profiles/separators/rtkd-separator-grammar-v0.json`
- SHA-256: `303f3062ad8b41bf84ab068f2fd6601b1efb3291872d53956669ea3dd7d88e3c`
- separator class count: 12
- `%` and `/` are preserved but do not finalize page boundaries.

## Corpus Candidate Generation

Generated ignored outputs under `data/normalized/corpus-candidates/rtkd-master-v0-candidate/`.

Real-source smoke counts:

- physical lines: 931
- logical lines: 1729
- token count: 22382
- rune tokens: 15933
- separator tokens: 5795
- numeric literals: 344
- unknown symbols: 310
- variant-mapped tokens: 0
- page candidates: 74
- warnings: 311

The manifest has `canonical_corpus_candidate=true`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Validation

Profile validation and corpus candidate validation passed during implementation. Full pytest and ruff validation are recorded in the final report.

## Git Safety

Raw transcript files, raw Pastebin text, generated corpus candidate outputs, generated alignment outputs, `.venv`, build outputs, and `LiberPrimus-Research-Report.md` must not be staged.

## GitHub Issue Status

Issue `Stage 0E: freeze Gematria profile and separator grammar` should be updated with profile hashes, candidate generation status, test result, and remaining limitations.

Issue `#2` was found and closed with a completion comment after profile validation, corpus candidate generation, pytest, and ruff passed. Issue `#3` was updated with a Stage 0E handoff comment noting that the generated corpus candidate is inactive and that Stage 1A should focus on solved-page golden fixtures and review.

## Known Limitations

Canonical corpus is not active. Page boundaries remain reviewable. Solved-page golden fixtures and cipher modules are not implemented.

## Next Recommended Stage

Stage 1A: implement solved-page golden fixture framework and reproduce direct-translation solved pages using Stage 0E profiles and corpus candidate generator, without brute-force search.
