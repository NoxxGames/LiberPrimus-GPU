# Stage 2A CPU Transform Registry Log

## Initial State

- Branch: `main`
- Starting commit: `71506da4b1f11a5574062ce06ce599b3f4f38310`
- Git status before changes: clean
- GitHub remote verified: `https://github.com/NoxxGames/LiberPrimus-GPU.git`
- Raw sources present and ignored: true
- Mirrored reference locks present: true
- Stage 0E profile hashes match: true
- Fixture sets present: direct, Atbash-family, Vigenere, prime-stream
- Expected solved fixture pass count: `10`
- Raw files staged: 0
- Generated outputs staged: 0
- `LiberPrimus-Research-Report.md` staged: 0
- README stale status detected: true, corrected during Stage 2A

## Public Status Cleanup

- README now reports Stage 2A registry/manifest runner complete.
- STATUS, ROADMAP, and CIPHER_CATALOG were updated for Stage 2A.
- Current solved-baseline counts remain direct `4`, Atbash-family `3`, Vigenere `2`, prime-stream `1`.

## Registry And Manifest Directories

- Added `data/transform-registry/`.
- Added `experiments/manifests/solved-baselines/`.
- Added ignored generated output area `experiments/results/solved-baselines/stage2a/`.
- Generated manifest-runner outputs remain ignored.

## Transform Registry Metadata

- Registry path: `data/transform-registry/cpu-reference-transforms-v0.json`.
- Registry SHA-256: `32e449b0a0f02cd1180767625474f0cfe2d988a26b13fd37741b7aa31023595e`.
- Registered transforms: `direct_translation`, `reverse_gematria`, `rotated_reverse_gematria`, `vigenere_explicit_key`, `prime_minus_one_stream`, `phi_prime_stream`.
- Alias: `phi_prime_stream -> prime_minus_one_stream`.
- Search, CUDA, and scoring are all disabled.

## Python Implementation

- Added `python/libreprimus/transforms/` registry models, loader, validator, metadata helpers, and dispatcher.
- Integrated solved-fixture reproduction with registry dispatch.
- Added registry metadata fields to solved-fixture reproduction records.
- Added `python/libreprimus/solved_baselines/` manifest loader, runner, exporter, summary loader, and validation helpers.

## Manifests

- Added schema `schemas/corpus/solved-baseline-run-manifest-v0.schema.json`.
- Added five manifests under `experiments/manifests/solved-baselines/`.
- All-known manifest expects 10 fixtures and 10 passes.

## Smoke Result

- Stage 2A smoke: pass.
- Fixture groups: `4`.
- Fixture pass/fail/pending/skipped: `10/0/0/0`.
- Direct/Atbash/Vigenere/prime pass counts: `4/3/2/1`.
- `search_performed_any=false`, `cuda_used_any=false`, `scoring_used_any=false`.
- Generated outputs path: `experiments/results/solved-baselines/stage2a/`.

## Validation Notes

- Pytest: `188 passed`.
- Ruff: passed.
- Registry validation: passed.
- Manifest validation: passed.
- Stage 2A real-source smoke: pass, `10/0/0/0`.
- C++ tests are skipped unless C++ files change; this is a Python/docs/registry/manifest-runner stage.
- Generated outputs, raw files, and `LiberPrimus-Research-Report.md` must remain unstaged.

## GitHub Issue

- Issue #5 found: true.
- URL: `https://github.com/NoxxGames/LiberPrimus-GPU/issues/5`.
- Status comment added: true.
- Closed: false, because generic affine/shift search, scoring, CUDA parity, and broader result-store work remain open.
- Labels updated: true.
