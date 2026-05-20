# CPU Batch Transform API

Stage 4H defines the CPU batch transform API as the reference path for future acceleration. It is intentionally CPU-only and works from normalized token stream records, not raw Discord logs, raw page images, or unreviewed corpus material.

## Contract

The API accepts:

- CPU batch manifests under `experiments/manifests/cpu-batch/`.
- Normalized input streams with explicit token kinds, rune indices, separators, and metadata.
- Explicit transform candidates with transform family, transform ID, and parameters.

The API emits generated records under ignored `experiments/results/cpu-batch/stage4h/`:

- `result_records.jsonl`
- `summary.json`
- `adapter_coverage.json`
- `warnings.jsonl`

Committed state is aggregate-only at `data/research/stage4h-cpu-batch-api-summary.yaml`.

## Supported Stage 4H Adapters

Stage 4H supports the existing CPU reference registry transforms:

- `direct_translation`
- `reverse_gematria`
- `rotated_reverse_gematria`
- `vigenere_explicit_key`
- `prime_minus_one_stream`
- `phi_prime_stream`

It also exposes deterministic local adapters for existing bounded execution helpers where semantics are already defined:

- `caesar_shift`
- `affine_mod29`

Unsupported transforms return `adapter_missing`; they are not faked and do not fail adapter coverage unless a future manifest requires them.

## Boundaries

The API does not implement CUDA, run broad experiments, add new transform families, process raw data, activate the canonical corpus, finalize page boundaries, or make solve claims.

## Stage 4I Scoring Compatibility

Stage 4I adds the score-summary contract used by CPU batch records. CPU batch scoring now includes scorer id/version, calibration profile id, finite Stage 4I confidence labels, legacy label preservation, and explicit no-solve/CUDA flags.

Future transform adapters must keep deterministic output hashes stable before any score comparison matters.

## Stage 4O Adapter Expansion

Stage 4O adds solved-fixture-safe input stream handling and adapter expansion checks without changing transform semantics. It records `9` supported adapters, `2` missing/deferred adapters, `8` CPU-only result records, `8` parity expectation records, and `8 / 0` scoring compatible/unavailable outputs.

Stage 4O generated records remain ignored under `experiments/results/cpu-batch/stage4o/`. The committed aggregate summary is `data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml`.

New adapters must preserve existing CPU behavior, include synthetic or solved-fixture-safe tests, and produce deterministic output hashes before any future CUDA work can rely on them.

## Stage 4P Result Surface Integration

Stage 4P joins Stage 4O CPU batch result records and parity expectations into the unified result-store reporting surface when local generated records are present. It records output hashes, parity expectation references, score-summary availability, and method status for comparison only.

CPU batch outputs remain generated and ignored. The Stage 4P aggregate summary is committed under `data/research/`; it does not replace Stage 4O parity expectations or authorize CUDA work.
