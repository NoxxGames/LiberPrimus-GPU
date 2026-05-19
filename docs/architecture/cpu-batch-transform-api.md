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
