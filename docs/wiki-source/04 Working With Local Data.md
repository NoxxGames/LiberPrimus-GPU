> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Working With Local Data

## Place Local Raw Files

Use the documented raw paths:

- Workbook: `<repo-root>\data\raw\legacy-workbooks\tranlsations.xlsx`
- Pastebin TXT: `<repo-root>\data\raw\legacy-pastebins\58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`
- rtkd transcript: `<repo-root>\data\raw\transcripts\rtkd\liber-primus__transcription--master.txt`

## Why Raw Files Are Ignored

Raw files may have redistribution, licensing, size, or provenance constraints. The project commits README files and locks, not raw data.

## Lock Metadata

Lock metadata records source ID, URL, local filename, SHA-256, size, and canonical status.

## What Not To Commit

Do not commit raw files, generated JSON/JSONL, SQLite databases, CSV exports, build directories, `.venv`, or cache folders.

## Generated Corpus Candidates

Stage 0E writes generated corpus candidate outputs under `data/normalized/corpus-candidates/`. They are ignored because `canonical_corpus_active=false` until a later review stage.
