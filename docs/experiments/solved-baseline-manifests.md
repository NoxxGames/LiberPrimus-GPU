# Solved-Baseline Manifests

## Purpose

Solved-baseline manifests describe regression runs for known solved fixtures. They prove the current CPU reference transforms still reproduce locked expectations before any future experiment work.

## Manifest Schema

The schema is `schemas/corpus/solved-baseline-run-manifest-v0.schema.json`. It requires registry ID and SHA-256, fixture groups, expected counts, output path, provenance, and hard false flags for canonical corpus activation, search, CUDA, and scoring.

## All-Known Solved Baseline Manifest

`experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml` runs all current solved fixture groups:

- direct translation: 4 expected passes
- Atbash-family: 3 expected passes
- explicit-key Vigenere: 2 expected passes
- prime-minus-one: 1 expected pass

## Fixture Group Manifests

Separate manifests exist for each fixture set:

- `direct-translation-v0.yaml`
- `atbash-family-v0.yaml`
- `vigenere-v0.yaml`
- `prime-stream-v0.yaml`

## Generated Outputs

Generated Stage 2A outputs are ignored under `experiments/results/solved-baselines/stage2a/`:

- `manifest_run_records.jsonl`
- `summary.json`
- `warnings.jsonl`

## Reproducibility Metadata

Run records include manifest ID/SHA-256, registry ID/SHA-256, fixture group ID, transform ID, canonical transform ID, fixture ID, status counts, and `search_performed=false`, `cuda_used=false`, and `scoring_used=false`.

## Not A Search Campaign

The manifest runner does not infer parameters or enumerate search spaces. It runs known fixture baselines only.

## Stage 2A Smoke

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-baseline stage2a-smoke `
  --manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml `
  --out-dir experiments/results/solved-baselines/stage2a `
  --allow-warnings
```

## Future Relation To Experiment Manifests

Stage 2B should add result-store and run-record infrastructure before unsolved-page search campaigns are introduced.
