# Dataset Policy

## Data policy

Data handling must protect raw evidence and preserve provenance. Stage 0B adds a non-canonical legacy workbook source class without promoting it to corpus truth.

## Immutable raw data

`data/raw/` is immutable. Do not overwrite, normalize, crop, repair, OCR, transcribe, or deduplicate raw files in place.

## Planned source classes

Future source classes include images, transcripts, message extracts, hashes, source metadata, license notes, and `legacy_analysis_workbook`.

`legacy_analysis_workbook` is non-canonical. It may provide solved-page delta hints, Prime Sums hints, and formula inventory, but it is not canonical corpus data.

## Planned source repositories

Stage 0B should evaluate candidate source repositories and mirrors before anything is imported.

## Transcript versioning

Transcripts must have explicit version IDs, source references, normalization rules, and SHA-256 locks.

## Image hashes

Images must be stored with SHA-256 hashes and acquisition metadata before derived text is trusted.

## Normalized corpus

Normalized data belongs under `data/normalized/` and must be reproducible from raw locks and documented rules.

Workbook-derived extraction outputs under `data/normalized/legacy-workbook/` are generated and ignored unless a later stage explicitly promotes selected records through a reviewed process.

## Solved fixtures

Solved fixtures belong under `data/solved/` or `tests/golden/` only after a reproduction requirement is defined.

## Licensing and redistribution caution

Do not assume public availability means redistribution is permitted. Record source and licensing status before adding data.

## Acquisition scripts policy

Acquisition scripts must not mutate existing raw files. They should verify hashes and refuse ambiguous overwrites.

## Corpus lock policy

Corpus locks will record file path, SHA-256, size, source, acquisition date, transcript profile, and Gematria profile.

Legacy workbook lock files live under `data/locks/legacy-workbooks/`. The raw workbook is ignored and hash-locked; only checksum and metadata files are committed.
