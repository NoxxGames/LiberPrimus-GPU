# Status

## Current stage

Stage 0C local legacy Pastebin ingestion.

## Completed in Stage 0A

Repository scaffold, documentation, CMake skeleton, optional CUDA smoke scaffold, Python package scaffold, Windows scripts, smoke manifest, and smoke tests.

## Completed in Stage 0B

Non-canonical legacy workbook ingestion support was added for `tranlsations.xlsx`, including raw-workbook ignore safety, lock metadata, Python XLSX parsing, CLI commands, synthetic tests, conditional real-workbook tests, and documentation.

## Completed in Stage 0C

Non-canonical local legacy Pastebin ingestion support was added for `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`, including raw-source ignore safety, lock metadata, Python TXT parsing, Gematria prime-value validation, CLI commands, synthetic tests, conditional real-source tests, documentation, and developer logs.

## Not yet implemented

No corpus import, cipher logic, Gematria freeze, scoring model, experiment runner, JSONL output, SQLite database, or serious CUDA kernel exists yet.

The real workbook was found locally and hash-locked as a raw legacy analysis artefact. It is not committed.

The real local TXT was found locally and hash-locked as a raw legacy LP2 rune/prime-value artefact. It is not committed. Developer log: `docs/development-logs/2026-05-16-stage-0c-legacy-pastebin-ingestion.md`.

## Toolchain status

Use `scripts/verify-toolchain.ps1` for the current host report. Stage 0A supports CPU-only builds and optional CUDA smoke builds.

## Next prompt recommendation

Stage 0D - align legacy Pastebin line-pairs with primary transcript/page-image sources, infer tentative page boundaries with confidence labels, create developer logs, and freeze a canonical transcript/versioning policy without attempting unsolved-page cryptanalysis.
