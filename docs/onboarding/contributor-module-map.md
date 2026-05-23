# Contributor Module Map

## Module Areas

- Profiles/corpus: `python/libreprimus/profiles/`, `python/libreprimus/corpus_candidate/`, `data/profiles/`.
- Solved fixtures: `python/libreprimus/solved_fixtures/`, `data/fixtures/`.
- Transforms: `python/libreprimus/transforms/`, `data/transform-registry/`.
- Scoring: `python/libreprimus/scoring/`, `python/libreprimus/candidate_inspection/`.
- Experiments: `python/libreprimus/experiments/`, `python/libreprimus/bounded_experiments/`, `experiments/`.
- Result store: `python/libreprimus/result_store/`, `schemas/result-store/`.
- Archive/history: `python/libreprimus/history/`, `data/observations/archive/`.
- Visual/image analysis: `python/libreprimus/image_analysis/`, `python/libreprimus/image_transforms/`, `data/observations/visual/`.
- Discord: `python/libreprimus/discord_ingestion/`, `discord_promotion/`, `discord_review/`, `discord_lead_promotion/`.
- Post-Discord: `python/libreprimus/post_discord/`.
- Stego: `python/libreprimus/stego/`.
- Research synthesis: `python/libreprimus/research_synthesis/`, `data/research/`.
- Document staleness: `python/libreprimus/doc_staleness/`, `data/project-state/`, `schemas/project-state/`.
- Source harvester: `python/libreprimus/source_harvester/`, `data/source-harvester/`, `schemas/source-harvester/`.
- CUDA parity/reporting: `python/libreprimus/cuda_*`, `python/libreprimus/prime_minus_one_*`, `python/libreprimus/bounded_p56_cuda_parity/`, `cuda/`, `data/cuda/`.
- CLI: `python/libreprimus/cli.py`, `python/libreprimus/cli_commands/`.
- CI/scripts: `.github/workflows/`, `scripts/ci/`, `scripts/github/`.

## Stable Areas

Docs, schemas, record validation, test fixtures, and source-lock metadata are relatively safe when changes are narrow and validated.

## Volatile Or Risky Areas

Corpus/profile semantics, scoring, experiment execution, privacy-sensitive Discord code, generated-output policy, and CUDA are high-risk. Read the relevant docs and tests first.

Source-harvester code is high-provenance tooling. Read `docs/architecture/cicada-source-harvester.md`, `docs/architecture/local-source-lock-inventory.md`, `docs/reference/source-harvester-cli.md`, `docs/reference/source-harvester-local-inventory-cli.md`, `docs/onboarding/source-harvester-workflow.md`, and `docs/onboarding/local-source-inventory-workflow.md` before changing it. Do not make Google Drive a storage backend; manual Google/Dropbox/Colab exports belong in ignored local roots.

## Good First Areas

- Documentation fixes.
- Tests for validation code.
- Source-lock records.
- Observation records.
- Negative controls.
- Schema validation.

## Risky Areas

- Changing rune mappings or separator semantics.
- Changing scoring labels or thresholds.
- Executing new experiments.
- Touching Discord raw-log processing.
- Adding CUDA kernels.
