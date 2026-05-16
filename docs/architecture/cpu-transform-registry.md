# CPU Transform Registry

## Status

Stage 2A adds the first CPU reference transform registry for known solved-baseline reproduction.

## Purpose

The registry gives each implemented reference transform a stable ID, formula, parameter schema, implementation link, and safety metadata. It is an orchestration layer for solved fixtures, not a search engine.

## Registry Design

The committed registry lives at `data/transform-registry/cpu-reference-transforms-v0.json`, with a SHA-256 lock beside it. Registry loading validates the lock, transform IDs, alias targets, implementation imports, fixture-set paths, and safety flags.

## Transform Metadata

Each transform declares:

- `transform_id`
- `transform_version`
- `method_family`
- `aliases`
- `formula`
- `parameter_schema`
- `supports_cpu_reference=true`
- `supports_gpu=false`
- `search_enabled=false`
- `scoring_enabled=false`
- `fixture_baseline_supported`
- `implemented_module`
- `known_fixture_sets`

## Alias Handling

`phi_prime_stream` resolves to `prime_minus_one_stream`. The alias records that `phi(p)=p-1` for prime inputs and does not create a separate search family.

## Dispatch Flow

The dispatcher resolves the transform ID, validates explicit parameters, rejects search/CUDA/scoring flags, then calls the existing solved-fixture decoder. Dispatch returns normalized text, hashes, warnings, transform metadata, and hard false execution flags.

## Safety Constraints

The registry rejects transform definitions that enable search, scoring, or GPU support. Missing required parameters fail clearly. Keys, rotations, and stream positions are never inferred.

## No-Search Policy

Stage 2A does not enumerate candidate keys, rotations, offsets, or alternate transform parameters. Manifest runs use only parameters declared in fixture manifests.

## No-CUDA Policy

All registry entries are CPU reference transforms. CUDA parity and acceleration remain future work.

## Relationship To Solved Fixtures

Solved-fixture reproduction now dispatches through the registry for direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, and prime-minus-one.

## Future Extension Points

Future stages may add result stores, manifest provenance, and eventually new registered CPU transforms. Search, scoring, and CUDA must remain separate stages with tests and policy updates.

## Tests

Stage 2A tests validate registry metadata, SHA locks, alias resolution, dispatch behavior, manifest integration, and the all-known solved-baseline smoke run.
