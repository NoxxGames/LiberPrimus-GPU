# Results Schema

## Purpose

Define planned result records before generated outputs exist.

## Stage 0A status

The result schema is planned, not finalized. No real result records are generated in Stage 0A.

## Result record principles

Records must be replayable, reviewable, compact, and explicit about uncertainty.

## Planned JSONL fields

Planned fields include result ID, experiment ID, manifest hash, corpus lock ID, transform chain, candidate summary, scores, null-control scores, rank, timestamps, and review status.

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
