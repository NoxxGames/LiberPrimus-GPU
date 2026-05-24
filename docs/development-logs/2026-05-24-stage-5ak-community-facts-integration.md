# Stage 5AK Community Facts Integration

Date: 2026-05-24

Stage 5AK integrated the local `third_party/UsefulFilesAndIdeas/community-facts/` folder after Stage 5AJ. The folder was treated as local ignored source material only.

Implementation added community-facts inventory, ordered attachment indexing, claim-record, correction-log, arithmetic-preflight, private Deep Research addendum, guardrail, next-stage decision, summary, and validation support to `libreprimus source-harvester`.

Local results:

- files inventoried: 11
- attachments indexed: 10
- claim records: 12
- correction records: 4
- clue-category records: 15
- arithmetic preflight records: 16
- arithmetic verified/error: 15/1
- private Deep Research-ready bundles: 10
- public website-ready bundles: 0
- selected next stage: Stage 5AL - Deep Research source inventory and reliability prompt

Guardrails held: no network fetch, live scrape, online clone, Google Drive storage, Deep Research execution, OCR, AI/ML interpretation, image forensics, stego/audio execution, hypothesis generation/execution, CUDA execution, CUDA source modification, kernels, benchmarks, scored experiments, website expansion, method-status upgrade, corpus activation, page-boundary finalisation, raw/generated publication, or solve claim.

Validation:

- `libreprimus source-harvester validate-stage5ak`: passed
- strict doc staleness: passed
- path sanitisation: passed
- research synthesis: passed
- state drift: passed
- consistency check-all: passed
- smoke: passed
- ruff: passed
- pytest: 1699 passed
- `scripts/ci/run-consistency-checks.ps1`: passed
- public docs, lock hashes, workflow static, wiki-source validation, and wiki dry-run: passed

Notes:

- `scripts/ci/run-consistency-checks.sh` was updated with the same Stage 5AK checks; local `bash -n` could not run because only the Windows WSL shim is installed and no WSL distribution is configured.
- Generated community-facts reports and private Deep Research body files remain ignored under `experiments/results/source-harvester-community-facts/stage5ak/`, `experiments/results/research-bundles/stage5ak/`, and `research-inputs/stage5ak/`.
