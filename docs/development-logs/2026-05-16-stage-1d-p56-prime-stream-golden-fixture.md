# Stage 1D p56 Prime-Stream Golden Fixture Log

## Initial State

- Branch: `main`
- Starting commit: `53dac84921a6a471b31404f2c610c65a2b15f90b`
- Git status before changes: clean
- GitHub remote verified: `https://github.com/NoxxGames/LiberPrimus-GPU.git`
- Raw sources present: true
- Mirrored reference locks present: true
- Stage 0E profile hashes match: true
- Stage 1A/1B/1C fixture frameworks present: true
- Raw files staged: 0
- Generated outputs staged: 0
- `LiberPrimus-Research-Report.md` staged: 0
- README stale status detected: true

## Implementation

- Added `prime_minus_one_stream` fixture transform and deterministic prime utilities.
- Recorded `phi_prime_stream` as an equivalent alias for prime inputs.
- Added payload extraction and payload check results.
- Added p56 fixture manifest under `data/fixtures/solved-pages/prime-stream-v0/`.
- Added CLI commands `reproduce-prime-stream` and `stage1d-smoke`.

## Fixture Result

- p56 fixture: pass
- Prime values used: 84
- Stream values used: 84
- Cleartext-F skip count: 1
- Payload check: pass

## Validation Notes

- Generated prime-stream outputs remain ignored.
- Raw transcripts and raw mirrored references remain ignored.
- `canonical_corpus_active=false` and `page_boundaries_final=false` remain required.

## Final Validation

- Stage 1D smoke: direct `4/0/0/0`, Atbash `3/0/0/0`, Vigenere `2/0/0/0`, prime-stream `1/0/0/0`.
- p56 skip count: `1`.
- p56 prime values used: `84`.
- p56 stream values used: `84`.
- p56 payload check: `pass`.
- Pytest: `170 passed`.
- Ruff: passed.
- C++ tests: skipped, Python/docs/fixture-transform/prime-stream stage only.
- GitHub issue #5: status comment added, labels confirmed, left open.
- Git safety before commit: generated outputs ignored, raw files staged `0`, raw mirrored files staged `0`, research report staged `0`.
