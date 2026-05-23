# Codex Navigation Map

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
- Run the Stage 5AH stage-ledger, operational-map coverage, and current/next-stage checks after Stage 5AI updates so Stage 5AJ Deep Research prompts inherit current source-of-truth labels.
- Keep raw/generated outputs unstaged.
- For Stage 5AF/5AG/5AI source-harvester work, keep all raw harvester outputs and generated bundle bodies local and ignored; do not use Google Drive as project storage.

## Documentation Updates

Update relevant `.md` and `.txt` files when stage status, roadmap direction, experiment priority, method-family status, data policy, CLI behavior, source-of-truth hierarchy, or schema/result families change.

If direction changes, update:

- `docs/roadmap/staged-plan.md`
- `data/research/project-direction-change-records-v0.yaml`
- `STATUS.md`
- `ROADMAP.md`
- `AGENTS.md`
- Relevant tutorials and `docs/wiki-source/**`
- `docs/onboarding/source-harvester-workflow.md`, `docs/onboarding/local-source-inventory-workflow.md`, `docs/onboarding/deep-research-bundle-workflow.md`, `docs/reference/source-harvester-cli.md`, `docs/reference/source-harvester-local-inventory-cli.md`, and `docs/reference/source-harvester-curated-bundles-cli.md` when source-harvester behavior changes.
- `data/project-state/stage5ah-*.yaml` and `data/source-harvester/stage5ai-*` when Stage 5AI bundle metadata or the Stage 5AJ next-stage decision change.

## Safety Rules

- Do not claim a solve.
- Do not activate the canonical corpus.
- Do not finalise page boundaries.
- Do not process raw Discord logs or raw page images unless a future stage explicitly scopes that work.
- Do not use CUDA before CPU references, stable scorer definitions, batch APIs, parity tests, and benchmarks exist.
