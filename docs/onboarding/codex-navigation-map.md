# Codex Navigation Map

## Stage 5BM Note

Stage 5BM is a metadata-only String 4 branch-crosswalk repair layer. Use `libreprimus token-block validate-stage5bm` for Stage 5BL findings integration, String 4 source restatement, primary-60 inverse policy, Stage 5AP mismatch analysis, Stage 5AW branch membership, source-gap severity updates, DWH quarantine, lineage preservation, guardrails, and Stage 5BN next-stage routing. Stage 5BN follow-up work should close the one unsupported String 4 position or prepare human-review metadata while keeping full String 4 bodies, decoded bytes, reconstructed streams, raw iddqd-v2/archive/Fandom/spreadsheet files, and generated outputs ignored.

## Stage 5BK Note

Stage 5BK is a metadata-only historical-route planning constraint layer. Use `libreprimus historical-route validate-stage5bk` for iddqd-v2 source-root/tree metadata, byte-string source locks, transcription/translation/key-lineage locks, positive-control context, planning constraints, source-gap severity, Stage 5BJ errata, token-block constraint updates, guardrails, and Stage 5BL next-stage routing. Stage 5BL follow-up work should review these planning constraints and keep raw iddqd-v2/archive/Fandom/spreadsheet files, full byte strings, decoded bytes, fonts, media, and generated outputs ignored.

## Stage 5BJ Note

Stage 5BJ is a metadata-only original/archive crosswalk closure layer. Use `libreprimus historical-route stage5bj-validate` for crosswalk closure, exact 2014 surface source locks, Fandom page-body status, boards-thread archive-equivalent context, media-equivalence closure, source-gap updates, token-block lineage preservation, guardrails, and Stage 5BK next-stage routing. Stage 5BK follow-up work should integrate these planning constraints and keep raw Fandom/archive/spreadsheet files plus full extracted surface bodies ignored.

## Stage 5BF Note

Stage 5BF is a local-only historical route source-lock layer. Use `libreprimus historical-route validate-stage5bf` for archive location, tree/inventory summaries, annual route inventory, artifact classifications, trust policy, technique taxonomy, source gaps, DWH context, guardrails, and the historical Stage 5BG review handoff. Current follow-up work should use Stage 5BJ and Stage 5BI metadata, keep raw `third_party/CicadaSolversIddqd` files ignored, and avoid token experiments, byte-stream generation, historical technique execution, PGP network verification, stego tools, decode attempts, hash/preimage search, scoring, OCR/AI/ML/LLM vision, image forensics, CUDA, cryptanalytic benchmarks, scored experiments, or solve-claim workflows.

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
- Run the Stage 5AH stage-ledger, operational-map coverage, and current/next-stage checks after current-stage updates so Stage 5BN prompts inherit current source-of-truth labels.
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
- `data/project-state/stage5ah-*.yaml`, `data/project-state/stage5ap-*`, `data/project-state/stage5ar-*`, `data/project-state/stage5at-*`, `data/project-state/stage5au-*`, `data/project-state/stage5bf-*`, `data/project-state/stage5bi-*`, `data/token-block/stage5ap-*`, `data/token-block/stage5ar-*`, `data/token-block/stage5at-*`, `data/token-block/stage5au-*`, `data/token-block/stage5bi-*`, `data/historical-route/stage5bf-*`, `data/historical-route/stage5bi-*`, `data/stego/stage5ap-*`, `data/source-harvester/stage5ai-*`, `data/source-harvester/stage5aj-*`, `data/source-harvester/stage5ak-*`, `data/source-harvester/stage5al-*`, `data/source-harvester/stage5bi-*`, `data/website-ingest/stage5al/*`, `data/website-render/stage5am-*`, and `data/deep-research-export/stage5an-*` when bundle metadata, website metadata, private content metadata, token-block source-lock metadata, coordinate-lock metadata, case-review metadata, historical-route metadata, Fandom/source-lock metadata, or next-stage decisions change.

## Safety Rules

- Do not claim a solve.
- Do not activate the canonical corpus.
- Do not finalise page boundaries.
- Do not process raw Discord logs or raw page images unless a future stage explicitly scopes that work.
- Do not use CUDA before CPU references, stable scorer definitions, batch APIs, parity tests, and benchmarks exist.
## Stage 5BF Navigation

Stage 5BF implementation is under `python/libreprimus/historical_route/`; CLI commands are documented in `docs/reference/historical-route-source-lock-cli.md`.

## Stage 5BI Navigation

Stage 5BI implementation is under `python/libreprimus/historical_route/stage5bi.py`; CLI commands are documented in `docs/reference/historical-route-source-lock-cli.md`.

## Stage 5BJ Navigation

Stage 5BJ implementation is under `python/libreprimus/historical_route/stage5bj.py`; CLI commands are documented in `docs/reference/historical-route-source-lock-cli.md`. The generated Stage 5BJ reports and local Codex completion summaries remain ignored under `experiments/results/historical-route/stage5bj/`, `codex_output/`, and `codex-output/`.

## Stage 5BK Navigation

Stage 5BK implementation is under `python/libreprimus/historical_route/stage5bk.py`; CLI commands are documented in `docs/reference/historical-route-source-lock-cli.md`. The generated Stage 5BK reports remain ignored under `experiments/results/historical-route/stage5bk/` and `experiments/results/token-block/stage5bk/`. The local completion summary is `codex-output/stage5bk-codex-completion.md`; do not create or use `codex_output/` for current handoffs.

## Stage 5BM Navigation

Stage 5BM implementation is under `python/libreprimus/token_block/stage5bm.py`; CLI commands are documented in `docs/reference/token-block-cli.md`. The generated Stage 5BM reports remain ignored under `experiments/results/token-block/stage5bm/` and `experiments/results/historical-route/stage5bm/`. The local completion summary is `codex-output/stage5bm-codex-completion.md`; do not create or use `codex_output/` for current handoffs.
