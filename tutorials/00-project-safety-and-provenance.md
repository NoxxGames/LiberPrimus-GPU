# Project Safety And Provenance

## Raw Data Policy

Raw data lives under `data/raw/` and is immutable. Do not edit, normalize, crop, OCR, transcribe, or deduplicate raw files in place.

Raw local files are intentionally ignored by Git. Commit lock metadata and documentation, not the raw files themselves.

## Canonical Vs Non-Canonical

Non-canonical sources can help generate hypotheses or tests. They are not corpus truth.

An active canonical corpus will require locked sources, documented normalization, frozen Gematria metadata, reviewed page boundaries, and reproducible tests. Stage 0D-P does not activate that corpus.

## Generated Outputs

Generated outputs live under ignored folders such as `data/normalized/legacy-pastebin/` and `data/normalized/alignment/`. They can be regenerated from raw locks and code.

## Reproducibility

Useful evidence needs source IDs, SHA-256 locks, local filenames, commands, git commits, and warnings. A screenshot or terminal table alone is not evidence.

## What Counts As Evidence

Evidence requires pinned inputs, a manifest or documented command, provenance fields, reviewed outputs, and negative controls when solving work begins.
