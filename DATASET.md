# Dataset Policy

## Data policy

Data handling must protect raw evidence and preserve provenance. Stage 0D adds raw transcript source classes and alignment outputs without activating canonical corpus truth.

## Immutable raw data

`data/raw/` is immutable. Do not overwrite, normalize, crop, repair, OCR, transcribe, or deduplicate raw files in place.

## Planned source classes

Future source classes include images, transcripts, message extracts, hashes, source metadata, license notes, `legacy_analysis_workbook`, `legacy_lp2_rune_prime_value_pastebin_local_txt`, and raw transcript sources.

`legacy_analysis_workbook` is non-canonical. It may provide solved-page delta hints, Prime Sums hints, and formula inventory, but it is not canonical corpus data.

`legacy_lp2_rune_prime_value_pastebin_local_txt` is non-canonical. It contains local Pastebin vGMK330j LP2 rune rows and Gematria prime-value rows. Page boundaries are not finalized from this source.

`primary_transcript_candidate` sources are raw transcript files under review for later canonical activation. The rtkd master transcription is proposed as `rtkd-master-transcription-v0-proposed`, but it is not active canonical corpus in Stage 0D.

`secondary_solved_page_and_numbering_reference` sources may provide page-label and solved-section context. The scream314 markdown is secondary context only.

## Planned source repositories

Stage 0B should evaluate candidate source repositories and mirrors before anything is imported.

## Transcript versioning

Transcripts must have explicit version IDs, source references, normalization rules, and SHA-256 locks.

## Image hashes

Images must be stored with SHA-256 hashes and acquisition metadata before derived text is trusted.

## Normalized corpus

Normalized data belongs under `data/normalized/` and must be reproducible from raw locks and documented rules.

Workbook-derived extraction outputs under `data/normalized/legacy-workbook/` are generated and ignored unless a later stage explicitly promotes selected records through a reviewed process.

Pastebin-derived extraction outputs under `data/normalized/legacy-pastebin/` are generated and ignored unless a later stage explicitly promotes selected records through a reviewed process.

Stage 0D alignment outputs under `data/normalized/alignment/` are generated and ignored. They can inform future corpus selection but are not source truth.

## Solved fixtures

Solved fixtures belong under `data/solved/` or `tests/golden/` only after a reproduction requirement is defined.

## Licensing and redistribution caution

Do not assume public availability means redistribution is permitted. Record source and licensing status before adding data.

## Acquisition scripts policy

Acquisition scripts must not mutate existing raw files. They should verify hashes and refuse ambiguous overwrites.

## Corpus lock policy

Corpus locks will record file path, SHA-256, size, source, acquisition date, transcript profile, and Gematria profile.

Legacy workbook lock files live under `data/locks/legacy-workbooks/`. The raw workbook is ignored and hash-locked; only checksum and metadata files are committed.

Legacy Pastebin lock files live under `data/locks/legacy-pastebins/`. The raw local TXT is ignored and hash-locked; only checksum and metadata files are committed.

Transcript lock files live under `data/locks/transcripts/`. Raw transcript files are ignored and hash-locked; only checksum and metadata files are committed.

## Public tutorial policy

Tutorials should teach local acquisition and lock workflows without embedding raw data. Public repositories should prefer acquisition instructions, metadata locks, and provenance notes over committed raw files.

## Stage 0D-followup alignment output policy

Transcript views, alignment-gap diagnostics, and boundary-audit files are generated outputs under `data/normalized/alignment/`. They are useful for review and corpus-policy decisions but remain ignored by Git and non-canonical until a later corpus-freeze stage explicitly promotes reviewed records.
