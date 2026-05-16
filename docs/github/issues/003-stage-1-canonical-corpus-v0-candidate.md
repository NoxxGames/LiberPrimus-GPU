# Stage 1: create canonical corpus v0 candidate records

## Summary

Create candidate canonical corpus records from locked transcript sources after profile and separator policy are ready.

## Current Status

No canonical corpus is active.

## Scope

Generate reviewed candidate records with source IDs, hashes, raw text preservation, normalized views, and non-final boundary metadata.

## Non-Goals

Do not claim new solves or use generated alignment hints as source truth.

## Deliverables

Corpus v0 candidate schema, generator, tests, and documentation.

## Acceptance Criteria

Candidate records are reproducible from locked raw sources and pass policy checks.

## Safety/Provenance Rules

Generated corpus candidates must keep provenance fields and explicit canonical activation status.

Suggested labels: stage-1, corpus, data-provenance, testing, safety

## Dependencies

Stage 0E Gematria and separator freeze.

## Links

- `DATASET.md`
- `RESULTS_SCHEMA.md`
