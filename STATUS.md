# Status

## Current stage

Stage 0B legacy workbook ingestion.

## Completed in Stage 0A

Repository scaffold, documentation, CMake skeleton, optional CUDA smoke scaffold, Python package scaffold, Windows scripts, smoke manifest, and smoke tests.

## Completed in Stage 0B

Non-canonical legacy workbook ingestion support was added for `tranlsations.xlsx`, including raw-workbook ignore safety, lock metadata, Python XLSX parsing, CLI commands, synthetic tests, conditional real-workbook tests, and documentation.

## Not yet implemented

No corpus import, cipher logic, Gematria freeze, scoring model, experiment runner, JSONL output, SQLite database, or serious CUDA kernel exists yet.

The real workbook was found locally and hash-locked as a raw legacy analysis artefact. It is not committed.

## Toolchain status

Use `scripts/verify-toolchain.ps1` for the current host report. Stage 0A supports CPU-only builds and optional CUDA smoke builds.

## Next prompt recommendation

Stage 0C - mirror primary source archives, pin SHA-256 locks, define canonical transcript/versioning policy, and freeze Gematria profile metadata without implementing unsolved-page cryptanalysis.
