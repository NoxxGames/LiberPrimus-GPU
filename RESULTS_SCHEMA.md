# Results Schema

## Purpose

Define planned result records before generated outputs exist.

## Stage 0A status

The result schema is planned, not finalized. Stage 0B implements legacy workbook extraction record shapes for non-canonical generated artefacts.

## Result record principles

Records must be replayable, reviewable, compact, and explicit about uncertainty.

## Planned JSONL fields

Planned fields include result ID, experiment ID, manifest hash, corpus lock ID, transform chain, candidate summary, scores, null-control scores, rank, timestamps, and review status.

Implemented legacy workbook record types:

- `legacy_workbook_sheet`
- `legacy_solved_delta`
- `legacy_prime_sum`
- `legacy_workbook_formula`
- `legacy_workbook_summary`
- `legacy_pastebin_line_pair`
- `legacy_pastebin_anchor`
- `legacy_pastebin_summary`
- `transcript_line`
- `scream314_reference_record`
- `pastebin_transcript_alignment`
- `lp2_page_boundary_candidate`
- `glyph_variant_observation`
- `stage0d_alignment_summary`

## Planned SQLite tables

Planned tables include experiments, runs, corpus_locks, transform_steps, scores, candidates, null_controls, hardware, and reviews.

## Required provenance fields

Required provenance will include git commit, manifest path and hash, tool versions, corpus locks, Gematria profile, transcript profile, random seed, and command line.

## Score breakdown fields

Scores should include component names, raw values, normalized values, weights, null-control distributions, and threshold notes.

## Hardware metadata

Hardware metadata should include CPU, RAM, GPU, driver, CUDA toolkit, compiler, OS, and relevant build flags.

## Reproducibility metadata

Reproducibility metadata should include run ID, timestamps, environment summary, deterministic seed, output schema version, and source data hashes.

## False-positive warnings

Every candidate record must be treated as unverified until rerun, compared to controls, and manually reviewed.

Workbook-derived records must include `trusted_as_canonical=false` and must not be treated as source truth.

Pastebin-derived records must include `source_id`, `source_sha256`, `source_local_filename`, and `trusted_as_canonical=false`.

Alignment-derived records must include source IDs, source SHA-256 hashes, confidence labels, and `trusted_as_canonical=false`. Boundary candidates must include `canonical_page_boundary=false`.

Public tutorials must not present generated results as evidence unless they are manifest-backed, provenance-complete, and explicitly reviewed. Stage 0D-P examples are smoke outputs only.

## Stage 0D-followup Record Types

Implemented/generated Stage 0D-followup record types include:

- `transcript_view_record`
- `alignment_gap_diagnostic`
- `page_boundary_confidence_audit`
- `stage0d_followup_alignment_summary`

These are diagnostic records only. They must include source hashes, confidence or reason labels where applicable, and non-canonical flags. Generated JSON/JSONL outputs under `data/normalized/alignment/` remain ignored.

## Stage 0E Corpus Schemas

Stage 0E adds schemas under `schemas/corpus/` for:

- `gematria-profile-v0`
- `glyph-variant-profile-v0`
- `separator-grammar-v0`
- `corpus_candidate_manifest`
- `corpus_token`
- `corpus_line`
- `corpus_page_candidate`
- `corpus_generation_warning`

Generated manifest and page records require `canonical_corpus_active=false`, `page_boundaries_final=false`, `canonical_page_boundary=false`, and `trusted_as_canonical=false` where applicable.

## Stage 1A Solved Fixture Schemas

Stage 1A adds schemas under `schemas/corpus/` for:

- `solved_page_fixture`
- `solved_page_reproduction_record`
- `solved_page_reproduction_summary`

Fixture and reproduction records require provenance hashes and keep `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.
