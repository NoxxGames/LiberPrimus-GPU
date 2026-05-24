# Operational File Map

Stage 5AB added `data/project-state/operational-file-map.yaml` as the maintained lifecycle map for documents that carry current operational state. Stage 5AH updates that map for stage-ledger staleness coverage, Stage 5AI updates it for curated bundle metadata, Stage 5AJ updates it for UsefulFiles integration and extraction-fidelity policy, Stage 5AK updates it for community-facts claim curation, Stage 5AL updates it for website-ingest/Deep Research export staging, Stage 5AM updates it for the static research index renderer, and Stage 5AN updates it for the private content pack, hosted private-content library, and Stage 5AO Deep Research direction. The YAML record is the machine-readable source; this page is the human-readable guide.

## Strict Files

These files must stay aligned with `data/project-state/stage5ah-doc-staleness-source-of-truth.yaml` whenever stage status changes. The Stage 5AB source-of-truth file remains historical context only.

- `README.md`
- `STATUS.md`
- `ROADMAP.md`
- `AGENTS.md`
- `CUDA_NOTES.md`
- `docs/roadmap/staged-plan.md`
- `docs/architecture/project-state-and-source-of-truth.md`
- `docs/architecture/cuda-target-boundaries.md`
- `docs/onboarding/start-here.md`
- `docs/onboarding/source-of-truth-map.md`
- `docs/onboarding/codex-navigation-map.md`
- `docs/onboarding/operational-file-map.md`

## Current-State Files

These files may contain more historical context, but current labels and deferral claims still need review:

- `BENCHMARKS.md`
- `EXPERIMENTS.md`
- `RESULTS_SCHEMA.md`
- `TESTING.md`
- `CIPHER_CATALOG.md`
- `docs/onboarding/deep-research-handoff-map.md`
- `docs/onboarding/contributor-module-map.md`
- `docs/onboarding/private-generated-data-map.md`
- selected tutorials and wiki-source mirrors

## Historical Files

`docs/development-logs/**`, `research-log/**`, and ignored `codex-output/**` are historical or local handoff material. They may mention old current stages when clearly archival. Do not rewrite historical logs just to match current operational status.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-doc-staleness --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml --strict

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-stage-ledger-staleness `
  --expected-latest-stage "Stage 5AN" `
  --expected-next-stage "Stage 5AO"

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-operational-file-map-coverage

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-current-next-stage-consistency `
  --expected-latest-stage "Stage 5AN" `
  --expected-next-stage "Stage 5AO"
```
