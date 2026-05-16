# Testing

## Test policy

Tests protect reproducibility and prevent false-positive drift.

## Unit tests

Unit tests cover small deterministic functions and placeholder status in Stage 0A.

## Integration tests

Integration tests will later cover manifest execution and result writing.

## Golden tests

Golden tests will later reproduce known solved-page behavior from locked fixtures. None are included in Stage 0A.

Stage 0B adds conditional real-workbook tests that run only when the ignored legacy workbook is locally present.

## Property tests

Property tests will later check transform invariants, inverse behavior, and edge cases.

Synthetic workbook parser tests cover inventory, solved-delta extraction, modulo validation, Prime Sums booleans, formula inventory, deterministic output, and CLI behavior.

## Fuzz tests

Fuzz tests will later target parsers, manifest loading, corpus normalization, and transform composition.

## CPU/GPU parity tests

Every CUDA kernel must match a CPU reference implementation across representative inputs and edge cases.

## Manifest determinism tests

Manifests must replay to the same outputs under pinned inputs and fixed seeds.

## Documentation consistency tests

Documentation checks should verify core policy statements such as raw-data immutability and Stage 0A restrictions.

Legacy workbook tests include p56 prime-minus-one first-delta checks, Welcome `DIVINITY` delta checks, and direct-page zero-delta checks for solved fixture hints.

Legacy Pastebin tests include first-pair prime validation, empty-pair preservation, Parable anchor detection, page-boundary non-finalization, and local-real-file conditional tests.

Stage 0D tests cover rtkd parser preservation, scream314 reference parsing, signature indexing, Pastebin-to-transcript alignment, tentative page-boundary candidates, glyph variant `ᛂ`, CLI commands, and real-source conditional smoke checks.

## Stage 0A smoke tests

Stage 0A includes C++ and Python smoke tests only.

## Stage 0B workbook tests

Stage 0B parser tests are Python-only. CUDA and C++ behavior are unchanged.

## Stage 0C Pastebin tests

Stage 0C parser tests are Python-only. They verify that prime values are converted to decimal indices and that generated records remain non-canonical.

## Stage 0D alignment tests

Stage 0D parser and alignment tests are Python-only. They assert no canonical boundary activation, no canonical trust flag, raw glyph preservation, and timing metadata presence.

## Stage 0D-P documentation and GitHub checks

Stage 0D-P validates tutorial, issue seed, wiki source, and GitHub script existence. GitHub helper scripts support dry runs before mutating labels, issues, or wiki pages.

## Stage 0D-followup parser, alignment, and boundary tests

Stage 0D-followup tests cover transcript physical/logical/stream views, bounded stream-subsequence matching, gap diagnostics, stricter boundary confidence auditing, CLI commands, and real-source conditional smoke checks. Tests assert that empty-pair-only and word-length-only evidence cannot create high-confidence boundaries, all boundaries keep `canonical_page_boundary=false`, and all alignment records remain non-canonical.

## Stage 0E profile and corpus candidate tests

Stage 0E tests validate Gematria profile invariants, glyph variant profile policy, separator grammar rules, corpus tokenization, JSON schemas, synthetic candidate generation, real-source conditional generation, and CLI commands.

## Stage 1A solved fixture tests

Stage 1A tests validate fixture schemas, direct-translation decoding, span selection, provenance validation, synthetic reproduction, real-source conditional reproduction, and solved-fixture CLI commands. They assert that direct fixtures do not use Atbash, Vigenere, prime streams, search, or CUDA.
## Stage 1B Tests

Stage 1B adds tests for reverse Gematria and rotated reverse Gematria formulas, explicit rotation validation, fixture schema compatibility, synthetic Atbash-family reproduction, direct-fixture regression, CLI smoke behavior, and real-source conditional reproduction.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
```

C++ tests are not required for Stage 1B unless C++ files change.
## Stage 1C Tests

Stage 1C tests cover reference mirroring metadata, reference-method extraction, explicit-key Vigenere key conversion, subtract decryption, key-advance rules, fixture-declared cleartext-F pass-through, fixture schema validation, synthetic reproduction, CLI commands, and real-source conditional reproduction.

The Stage 1C smoke keeps Stage 1A direct and Stage 1B Atbash-family fixtures as regressions.

## Stage 1D Tests

Stage 1D tests cover deterministic prime generation, prime-minus-one / phi-prime equivalence, stream advancement rules, cleartext-F skip handling, payload hash checks, fixture schema validation, synthetic reproduction, CLI commands, and real-source conditional reproduction.

The Stage 1D smoke keeps Stage 1A direct, Stage 1B Atbash-family, and Stage 1C Vigenere fixtures as regressions. C++ tests are not required for Stage 1D unless C++ files change.

## Stage 2A Tests

Stage 2A tests cover transform registry metadata, SHA-256 locks, alias resolution, CPU dispatch, manifest schema validation, synthetic solved-baseline runner outputs, CLI commands, and real-source conditional smoke checks.

The Stage 2A smoke reproduces 10 known solved fixtures through registry dispatch. C++ tests are not required for Stage 2A unless C++ files change.

## Stage 2B Tests

Stage 2B tests cover result-store JSON schemas, JSONL sink determinism, SQLite table creation and duplicate handling, provenance capture, solved-baseline import, CLI commands, and real-source conditional smoke checks.

The Stage 2B smoke imports the Stage 2A all-known solved-baseline run into generated JSONL and SQLite result stores. C++ tests are not required for Stage 2B unless C++ files change.

## Stage 2C Tests

Stage 2C adds static workflow tests and CI script tests. They verify `.github/workflows/ci.yml` runs on push and pull requests, uses Python 3.12, runs Ruff and pytest, validates the transform registry and committed manifests, avoids secrets and artifact uploads, and keeps scripts raw-data-free.

Local CI reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
.\scripts\ci\validate-workflow-static.ps1
```

The GitHub Actions workflow also includes a CPU-only CMake smoke job with CUDA disabled.

Stage 2C-followup extends workflow tests to parse YAML with PyYAML, validate trigger and job structure, and reject flattened/minified workflow files.

Stage 2C-followup-2 adds post-push remote workflow verification scripts and strengthens static tests with an explicit minified workflow rejection sample.

Stage 2C-followup-3 adds `.gitattributes` static tests and canonical lock-hash line-ending tests. CI now verifies lock hashes before Python tests.

Stage 2C-followup-4 adds public documentation status tests for README, STATUS, and ROADMAP. These tests allow historical stage mentions but reject stale top-level current-status and next-milestone language.
