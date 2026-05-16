# Add solved-page golden fixture framework

## Summary

Add a framework for known solved-page reproduction tests.

## Current Status

Workbook and Pastebin sources provide hints, but no canonical solved fixtures are active.

## Scope

Define fixture format, provenance fields, expected transforms, and regression tests.

## Non-Goals

Do not add unsolved-page plaintext or page-specific hacks.

## Deliverables

Golden fixture schema, test helpers, docs, and example synthetic fixture.

## Acceptance Criteria

Known solved-page reproduction can be tested from locked inputs when approved.

## Safety/Provenance Rules

Fixtures must not be promoted from legacy sources without review.

Suggested labels: testing, corpus, data-provenance, needs-human-review

## Dependencies

Canonical transcript candidate and Gematria profile.

## Links

- `TESTING.md`
- `docs/research/legacy-google-sheet-workbook.md`
