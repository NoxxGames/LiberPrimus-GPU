# Stage 0E: freeze Gematria profile and separator grammar

## Summary

Define the first reviewed Gematria profile and transcript separator grammar.

## Current Status

Stage 0C uses `legacy_validation_gematria_primus_v0`; Stage 0D preserves raw glyph variants and rtkd separators.

## Scope

Document rune entries, glyph variants, separator tokens, normalized views, and tests.

## Non-Goals

Do not solve unsolved pages or finalize page boundaries.

## Deliverables

Gematria profile metadata, separator grammar policy, tests, and updated corpus policy docs.

## Acceptance Criteria

Profile and separator grammar are locked, reviewed, and used by parsers without raw mutation.

## Safety/Provenance Rules

Preserve raw glyphs and record any normalized-view mapping.

Suggested labels: stage-0e, corpus, data-provenance, testing, safety

## Dependencies

Stage 0D glyph variant policy and transcript parser.

## Links

- `docs/research/glyph-variant-policy.md`
- `docs/corpus/canonical-transcript-versioning-policy.md`
