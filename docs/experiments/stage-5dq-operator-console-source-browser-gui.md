# Stage 5DQ Operator Console Source Browser GUI

Stage 5DQ implements the Liber Primus Operator Console v0 Source Browser as local review infrastructure. The stage is not source-locking, experiment execution, target selection, active-ingestion authorization, or puzzle solving.

Implemented scope:

- operator-console Python package with optional PySide6 GUI entrypoint
- source-browser normalization over committed metadata
- manual-entry, override, tombstone, path-alias, saved-filter, and column-profile scaffolds
- context-file status/open helpers
- CLI commands and aliases
- Stage 5DQ project-state records and validation

Recorded local Stage 5DQ counts:

- source-browser records scanned: `1292`
- source-browser entries loaded: `1293`
- missing local paths recorded as warnings: `7253`
- manual entries: `0`
- manual overrides: `0`
- tombstones: `0`

No route extraction, OCR, image forensics, AI/ML interpretation, DWH/hash search, byte-stream generation, scoring, CUDA, benchmarking, website expansion, raw-source mutation, generated-output publication, canonical-corpus activation, page-boundary finalisation, or solve claim was performed.
