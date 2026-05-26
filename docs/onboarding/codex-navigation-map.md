# Codex Navigation Map

## Stage 5AY Note

Stage 5AY is a bounded token-block preflight manifest design stage. Use `libreprimus token-block validate-stage5ay` for committed Stage 5AY records and `libreprimus parallel-validation` or `scripts/ci/run-parallel-validation.ps1` for opt-in local validation. Stage 5AZ follow-up work should review the Stage 5AY design and gates, keep the Stage 5AU filled decision template ignored, and avoid token experiments, byte-stream generation, decode attempts, hash/preimage search, OCR/AI/ML/LLM vision, image forensics, stego, CUDA, cryptanalytic benchmarks, scored experiments, or solve-claim workflows.

## Read First

For most Codex tasks, read:

1. `AGENTS.md`
2. `STATUS.md`
3. `ROADMAP.md`
4. `docs/roadmap/staged-plan.md`
5. The relevant module docs, schemas, and latest stage logs.

## Before Changing Anything

- Verify local branch, `HEAD`, `origin/main`, and latest CI with Git/GitHub tooling.
- Do not trust rendered GitHub pages, cached raw URLs, memory, or old conversation context when state matters.
- Run the task-specific validation commands before staging.
- Run `libreprimus consistency check-doc-staleness --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml --strict` when operational docs change.
- Run the Stage 5AH stage-ledger, operational-map coverage, and current/next-stage checks after current-stage updates so Stage 5AZ prompts inherit current source-of-truth labels.
- Keep raw/generated outputs unstaged.
- For Stage 5AF/5AG/5AI/5AJ/5AK source-harvester work, keep all raw harvester outputs, raw UsefulFiles/community-facts material, and generated bundle/extraction bodies local and ignored; do not use Google Drive as project storage.

## Documentation Updates

Update relevant `.md` and `.txt` files when stage status, roadmap direction, experiment priority, method-family status, data policy, CLI behavior, source-of-truth hierarchy, or schema/result families change.

If direction changes, update:

- `docs/roadmap/staged-plan.md`
- `data/research/project-direction-change-records-v0.yaml`
- `STATUS.md`
- `ROADMAP.md`
- `AGENTS.md`
- Relevant tutorials and `docs/wiki-source/**`
- `docs/onboarding/source-harvester-workflow.md`, `docs/onboarding/local-source-inventory-workflow.md`, `docs/onboarding/deep-research-bundle-workflow.md`, `docs/onboarding/deep-research-ingest-format.md`, `docs/onboarding/community-observation-ingest-workflow.md`, `docs/reference/source-harvester-cli.md`, `docs/reference/source-harvester-local-inventory-cli.md`, `docs/reference/source-harvester-curated-bundles-cli.md`, `docs/reference/source-harvester-usefulfiles-cli.md`, and `docs/reference/source-harvester-community-facts-cli.md` when source-harvester behavior changes.
- `data/project-state/stage5ah-*.yaml`, `data/project-state/stage5ap-*`, `data/project-state/stage5ar-*`, `data/project-state/stage5at-*`, `data/project-state/stage5au-*`, `data/token-block/stage5ap-*`, `data/token-block/stage5ar-*`, `data/token-block/stage5at-*`, `data/token-block/stage5au-*`, `data/stego/stage5ap-*`, `data/source-harvester/stage5ai-*`, `data/source-harvester/stage5aj-*`, `data/source-harvester/stage5ak-*`, `data/source-harvester/stage5al-*`, `data/website-ingest/stage5al/*`, `data/website-render/stage5am-*`, and `data/deep-research-export/stage5an-*` when bundle metadata, website metadata, private content metadata, token-block source-lock metadata, coordinate-lock metadata, case-review metadata, or the Stage 5AV next-stage decision change.

## Safety Rules

- Do not claim a solve.
- Do not activate the canonical corpus.
- Do not finalise page boundaries.
- Do not process raw Discord logs or raw page images unless a future stage explicitly scopes that work.
- Do not use CUDA before CPU references, stable scorer definitions, batch APIs, parity tests, and benchmarks exist.
