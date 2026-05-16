# Stage 0E Corpus Candidate Generation

## Stage Summary

Stage 0E freezes tooling profiles and generates an rtkd master corpus v0 candidate. It does not activate a canonical corpus and does not solve pages.

## Inputs

- rtkd master transcript raw file and lock
- Stage 0D-followup page-boundary candidate outputs when present
- Gematria profile v0
- Separator grammar v0
- Glyph variant profile v0

## Profile Freeze

Gematria, separator grammar, and glyph variant profiles are committed with SHA-256 locks and validation tests. `canonical_profile_active=true` applies to profiles only.

## Tokenizer Design

The tokenizer preserves raw runes, documented glyph variants, separators, whitespace, numeric literals, unknown symbols, source line numbers, and source columns. Unknown symbols produce warnings.

## Generated Counts

The real-source smoke generated 22382 tokens, 15933 rune tokens, 5795 separator tokens, 1729 logical lines, and 74 reviewable page candidates.

## Warnings

Warnings are generated for unknown symbols and page-candidate overgeneration. They are not solve evidence.

## Boundary Handling

Stage 0D-followup page candidates are imported as reviewable metadata only. All page candidates keep `canonical_page_boundary=false`.

## Remaining Limitations

The corpus candidate is not active canonical corpus. Page boundaries remain reviewable, solved-page golden fixtures are not implemented, and generated outputs are ignored.

## Next Stage

Stage 1A should add solved-page golden fixture framework and direct-translation reproduction using Stage 0E profiles and generated candidate records.
