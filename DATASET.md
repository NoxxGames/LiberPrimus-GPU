# Dataset Policy

## Data policy

Data handling must protect raw evidence and preserve provenance. After Stage 3V, the canonical corpus is still inactive and page boundaries remain reviewable. Historical Stage 0D added raw transcript source classes and alignment outputs without activating canonical corpus truth.

Stage 4K adds allowlisted public source-lock snapshot metadata under
`data/locks/third-party/source-snapshots/`. These records may include URLs, canonical URLs,
retrieval status, content hashes for ignored local fetches, GitHub commit-addressed references,
source class, copyright notes, and snapshot policy. They are reproducibility metadata only and do
not make any source canonical.

Stage 4M adds image-preflight metadata records under `data/observations/visual/` and a blocked
bigram/Fibonacci-421 readiness record under `data/observations/review/`. These records may cite
local ignored page-image hashes and `data/raw/images/Fib421.jpg` metadata, but the raw images stay
ignored and uncommitted.

## Immutable raw data

`data/raw/` is immutable. Do not overwrite, normalize, crop, repair, OCR, transcribe, or deduplicate raw files in place.

## Planned source classes

Future source classes include images, transcripts, message extracts, hashes, source metadata, license notes, `legacy_analysis_workbook`, `legacy_lp2_rune_prime_value_pastebin_local_txt`, and raw transcript sources.

`legacy_analysis_workbook` is non-canonical. It may provide solved-page delta hints, Prime Sums hints, and formula inventory, but it is not canonical corpus data.

`legacy_lp2_rune_prime_value_pastebin_local_txt` is non-canonical. It contains local Pastebin vGMK330j LP2 rune rows and Gematria prime-value rows. Page boundaries are not finalized from this source.

`primary_transcript_candidate` sources are raw transcript files under review for later canonical activation. The rtkd master transcription is proposed as `rtkd-master-transcription-v0-proposed`, but it is not active canonical corpus.

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

Solved fixtures live under `data/fixtures/solved-pages/`. Fixture expected text is curated test data with source/profile provenance, not raw corpus data and not a solve claim. Generated solved-baseline reproduction outputs live under `data/normalized/solved-baselines/` and remain ignored.

## Licensing and redistribution caution

Do not assume public availability means redistribution is permitted. Record source and licensing status before adding data.

Stage 4K defaults to metadata/hash locking. Fetched public HTML/text belongs in the ignored
`third_party/SourceSnapshots/` cache unless a later explicit policy approves a small text snapshot.
Binary, image, audio, font, PDF, and archive artefacts must not be committed.

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

## Stage 0E profile source of truth

Committed profiles under `data/profiles/` are tooling source-of-truth records for Gematria, separators, and documented glyph variants. Raw transcripts remain immutable under `data/raw/`; generated corpus candidate outputs live under `data/normalized/corpus-candidates/` and remain ignored.

## Stage 1A solved fixture policy

Direct-translation fixtures use locked rtkd and scream314 sources plus Stage 0E profile hashes. The expected strings are small normalized test expectations and must not be expanded into raw transcript dumps.

## Stage 1B Atbash-Family Fixtures

Stage 1B adds committed fixture manifests under `data/fixtures/solved-pages/atbash-family-v0/`. These fixtures are curated test expectations for known solved sections, not raw corpus dumps and not new solve claims.

Generated Atbash-family reproduction outputs are written under `data/normalized/solved-baselines/atbash-family-v0/` and remain ignored. Raw transcript files and generated corpus candidate outputs remain uncommitted.

Every Stage 1B fixture records rtkd, scream314, Gematria, separator, glyph-variant, and corpus-candidate provenance. `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false` remain required.
## Stage 1C Reference And Fixture Data

Stage 1C mirrors small reference files under ignored `data/raw/reference-repos/` and commits only lock metadata under `data/locks/reference-repos/`.

`lipeeeee/gematria` is reference-only: it is not imported, executed, or copied into production code.

Vigenere fixture expected text under `data/fixtures/solved-pages/vigenere-v0/` is curated test data with locked-source provenance. Generated reproduction outputs under `data/normalized/solved-baselines/vigenere-v0/` remain ignored.

## Stage 1D Prime-Stream Fixture Data

The p56 fixture under `data/fixtures/solved-pages/prime-stream-v0/` is curated solved-baseline test data with locked-source provenance. The expected hex payload is recorded as a separate payload check and is not treated as plaintext.

Generated prime-stream reproduction outputs under `data/normalized/solved-baselines/prime-stream-v0/` remain ignored. Raw transcripts, raw mirrored references, generated corpus candidates, and solved-baseline outputs remain uncommitted.

## Stage 2A Registry And Manifest Data

The CPU transform registry under `data/transform-registry/` and solved-baseline manifests under `experiments/manifests/solved-baselines/` are committed control metadata. They do not contain raw transcript dumps.

Generated manifest-runner outputs under `experiments/results/solved-baselines/` remain ignored. Raw sources, generated corpus candidates, and generated solved-baseline outputs remain uncommitted.

## Stage 2B Result Store Outputs

Stage 2B result-store manifests under `experiments/manifests/result-store/` are committed control metadata and contain no raw transcript dumps.

Generated JSONL and SQLite result stores under `experiments/results/result-store/` are ignored. They may reference generated output paths and provenance hashes, but they must not promote raw sources, generated corpus candidates, solved-baseline outputs, or SQLite databases into Git.
