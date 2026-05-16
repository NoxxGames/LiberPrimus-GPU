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

## Completed in Stage 0D-followup

Stage 0D-followup added transcript logical-line and rune-stream views, bounded stream-subsequence alignment, alignment-gap diagnostics, and stricter page-boundary confidence auditing.

Real-source follow-up summary: rtkd physical lines `931`, logical lines `798`, Pastebin line pairs `185`, exact matches `52`, high-confidence matches `129`, medium-confidence matches `0`, low-confidence matches `2`, no matches `2`, no-match reduction `151`, boundary candidates `74`, high/medium/low/none boundaries `50/3/21/0`, overgeneration warning `true`.

Remaining gaps: two no-match records and two low-confidence records still require review. Boundary candidates remain tentative and non-canonical.

Developer log: `docs/development-logs/2026-05-16-stage-0d-followup-alignment-gap-audit.md`.

## Completed in Stage 0E

Stage 0E added frozen tooling profiles, corpus schemas, and an rtkd master corpus v0 candidate generator.

Profile hashes: Gematria `93577209028c964523068b5975180e05bda5b1a07b2675d4e35d03d6d164c5c2`; glyph variants `5acae61c4ea2aa9f2f2fb76bdcafb7ed9c6504bd98caf29590a95d7d43271d6d`; separator grammar `303f3062ad8b41bf84ab068f2fd6601b1efb3291872d53956669ea3dd7d88e3c`.

Real-source candidate summary: physical lines `931`, logical lines `1729`, tokens `22382`, rune tokens `15933`, separator tokens `5795`, page candidates `74`, warnings `311`, `canonical_corpus_active=false`.

Developer log: `docs/development-logs/2026-05-16-stage-0e-gematria-separators-corpus-candidate.md`.

## Completed in Stage 1A

Stage 1A added solved-page golden fixture schemas, direct-translation fixture manifests, a direct-translation decoder, span selectors, reproduction CLI commands, tests, docs, and developer logs.

Real-source fixture summary: fixtures `4`, pass/fail/pending/skipped `4/0/0/0`, direct translation implemented `true`, `canonical_corpus_active=false`.

Developer log: `docs/development-logs/2026-05-16-stage-1a-direct-translation-golden-fixtures.md`.

## Completed in Stage 1B

Stage 1B added CPU-only reverse Gematria and rotated reverse Gematria fixture reproduction.

Real-source fixture summary: Atbash-family fixtures `3`, pass/fail/pending/skipped `3/0/0/0`, direct regression `4/0/0/0`, `canonical_corpus_active=false`.

Implemented fixture methods: `reverse_gematria` and `rotated_reverse_gematria`. Vigenere, prime streams, generic affine search, scoring, and CUDA remain unimplemented.

Developer log: `docs/development-logs/2026-05-16-stage-1b-atbash-family-golden-fixtures.md`.

## Completed in Stage 1C

Stage 1C mirrored and locked additional reference-source files, added CPU-only explicit-key Vigenere fixture reproduction, and added Vigenere known-solved fixtures.

Reference mirror summary: files attempted `9`, locked `9`, failed `0`; scream314 method notes `10`; lipeeeee tooling notes `32`.

Real-source fixture summary: Vigenere fixtures `2`, pass/fail/pending/skipped `2/0/0/0`, direct regression `4/0/0/0`, Atbash regression `3/0/0/0`, `canonical_corpus_active=false`.

Implemented fixture method: `vigenere_explicit_key`. Key search, p56 prime streams, generic affine/shift search, scoring, and CUDA remain unimplemented.

Developer log: `docs/development-logs/2026-05-16-stage-1c-vigenere-golden-fixtures.md`.

## Completed in Stage 1D

Stage 1D added CPU-only p56 prime-minus-one / phi-prime known-solved fixture reproduction and payload preservation checks.

Real-source fixture summary: prime-stream fixtures `1`, pass/fail/pending/skipped `1/0/0/0`, direct regression `4/0/0/0`, Atbash regression `3/0/0/0`, Vigenere regression `2/0/0/0`, `canonical_corpus_active=false`.

Payload check result: p56 hex block `pass`.

Implemented fixture method: `prime_minus_one_stream`, with `phi_prime_stream` as an equivalent alias for prime inputs. Generic prime-stream search, affine/shift search, scoring, and CUDA remain unimplemented.

Developer log: `docs/development-logs/2026-05-16-stage-1d-p56-prime-stream-golden-fixture.md`.

## Next prompt recommendation

Stage 2A - build the CPU transform registry and manifest-addressable solved-baseline runner, registering direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, and prime-minus-one as CPU reference transforms only.
