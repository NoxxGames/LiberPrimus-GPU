# Status

## Current stage

Stage 0D transcript alignment and canonical transcript policy scaffolding.

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

## Completed in Stage 0D

The rtkd master transcript was downloaded, ignored, and hash-locked as a proposed primary transcript candidate. The scream314 markdown was downloaded, ignored, and hash-locked as secondary context.

Stage 0D added transcript parsers, signature-based Pastebin alignment, tentative page-boundary candidates, glyph variant `ᛂ` observations, CLI commands, tests, docs, and developer logs.

Real-source smoke summary: rtkd physical lines `931`, Pastebin line pairs `185`, exact matches `1`, high-confidence matches `1`, medium-confidence matches `28`, low-confidence matches `2`, no matches `153`, boundary candidates `74`, glyph variant occurrences `453`.

Developer log: `docs/development-logs/2026-05-16-stage-0d-transcript-alignment-policy.md`.

## Completed in Stage 0D-P

Public-facing tutorials were added under `tutorials/`. GitHub issue templates, issue seed files, label definitions, wiki source pages, and helper scripts were added under `.github/`, `docs/github/`, and `scripts/github/`.

AGENTS.md now documents push, issue idempotency, and wiki mirror policy. Stage 0D-followup remains the next technical stage.

GitHub labels were created or updated and 10 seed issues were opened. Wiki source pages were prepared, but wiki publish failed because the wiki git endpoint was not reachable despite wiki being enabled.

## Toolchain status

Use `scripts/verify-toolchain.ps1` for the current host report. Stage 0A supports CPU-only builds and optional CUDA smoke builds.

## Next prompt recommendation

Stage 0D-followup - resolve transcript-alignment gaps, ambiguous page-boundary candidates, and glyph-variant evidence before corpus freeze.
