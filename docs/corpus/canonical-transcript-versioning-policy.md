# Canonical Transcript Versioning Policy

## Status: Proposed Stage 0D Policy

This document proposes transcript versioning rules. It does not activate a canonical corpus.

## Scope

The policy covers raw transcript sources, transcript version IDs, normalized views, glyph variants, page boundaries, and promotion requirements.

## Definitions

Raw source: an immutable file under `data/raw/`.

Transcript source: a raw source containing transcript text or transcript-like structure.

Transcript version: a locked, named interpretation of a transcript source.

Canonical transcript candidate: a source/version under review for future activation.

Active canonical corpus: a later promoted corpus with frozen source locks, grammar, Gematria profile, and tests.

Normalized view: generated records derived from raw data under documented rules.

Glyph variant: a raw glyph whose relationship to the active rune profile is unresolved or source-specific.

Page boundary: a source marker or inferred boundary between page regions.

Alignment hint: a non-canonical generated record connecting sources.

## Source Hierarchy

Primary transcript candidate: rtkd master transcription.

Secondary reference: scream314 `liber_primus.md`.

Legacy source: Pastebin vGMK330j local TXT.

Legacy source: solved-page spreadsheet `tranlsations.xlsx`, if present.

## What Can Become Canonical

A locked transcript source plus reviewed separator grammar, frozen Gematria profile, validated page-boundary policy, and reproducible tests may become a canonical transcript version.

## What Cannot Become Canonical

Legacy Pastebin rows, workbook-derived rows, terminal output, generated alignments, and tentative boundary candidates cannot become canonical by themselves.

## Raw-Source Locking Rules

Every raw source must have SHA-256, file size, source URL, local path, acquisition timestamp, and `trusted_as_canonical=false` until activation.

## Transcript Version ID Format

Use lowercase source IDs with a version and status suffix, for example `<source-id>-v<number>-<status>`.

## Proposed Version ID

`rtkd-master-transcription-v0-proposed`

## Canonical Activation Requirements

- Raw SHA-256 lock exists.
- Parser passes.
- Separator grammar documented.
- Gematria profile frozen.
- Glyph variant policy documented.
- Solved-page reproduction tests exist.
- Alignment to legacy sources reviewed.
- Developer log exists.
- CI tests pass.

## Page-Boundary Policy

Page boundaries stay tentative until source markers, page images or authoritative references, and regression tests agree. Stage 0D boundary candidates are never canonical boundaries.

## Separator Preservation Policy

Raw separators are preserved in transcript records. Normalized views may classify separators but must retain source line numbers and raw text.

## Glyph Variant Policy

Raw glyphs are preserved. Normalized views may apply documented mappings only with explicit evidence fields.

## Legacy-Source Use Policy

Legacy sources can provide parser validation, alignment hints, and golden-fixture hints. They cannot prove plaintext or activate corpus records.

## Generated Output Policy

Generated alignment and normalized outputs remain ignored by Git unless a later promotion process explicitly creates reviewed fixture records.

## Corpus Freeze Checklist

Confirm source locks, parser tests, separator grammar, Gematria profile, glyph variants, page boundaries, solved-page reproduction, provenance schema, and developer logs.

## Stage 0E Or Stage 1 Prerequisites

Resolve Stage 0D alignment gaps or explicitly document them before generating canonical corpus v0 candidate records.

## Stop Conditions

Stop if raw sources would be overwritten, page boundaries would be asserted without evidence, glyph variants would be silently rewritten, or generated outputs would be staged as source truth.

## Stage 0D-followup Implications

Stage 0D-followup improves legacy Pastebin alignment through stream views but does not activate the canonical corpus. Corpus v0 candidate records still require Gematria profile freeze, separator grammar freeze, reviewed page-boundary metadata, and explicit handling of the remaining unmatched or low-confidence alignment records.
