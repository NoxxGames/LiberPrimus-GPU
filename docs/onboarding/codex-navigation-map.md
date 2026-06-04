# Codex Navigation Map

## Stage 5DC Note

Stage 5DC is a metadata-only operator choice selection layer. Use `libreprimus token-block validate-stage5dc` for Stage 5DB findings integration, selected option validation for `prepare_real_operator_approval_record`, unselected-option preservation, explicit-pause nonselection, real-approval noncreation, combined-gate and activation nonauthorization, Stage 5CY/5DA/5BD preservation, active-lineage preservation, handoff continuity, credential-redaction policy, governance-scope control, and Stage 5DD next-stage routing. Treat the selected option as non-authorizing: it creates no real approval record, creates no Deep Research acceptance record, satisfies no gate, activates no input, generates no bytes, and executes nothing.

## Stage 5DA Note

Stage 5DA is a metadata-only operator choice / pause scaffold layer. Use `libreprimus token-block validate-stage5da` for Stage 5CZ findings integration, Stage 5CY preflight preservation, Stage 5CS option preservation, choice/pause nonselection, explicit-pause nonactivation, Stage 5BD plan preservation, active-lineage preservation, handoff continuity, credential-redaction policy, governance-scope control, and Stage 5DB next-stage routing. Treat the scaffold as non-authorizing: it creates no real choice/pause record, selects no option, selects no explicit pause, creates no approval records, activates no input, generates no bytes, and executes nothing.

## Stage 5CW Note

Stage 5CW is a metadata-only real-decision package preflight layer. Use `libreprimus token-block validate-stage5cw` for Stage 5CV findings integration, review-only real-decision package preflight, Stage 5CU negative-fixture preservation, Stage 5CS option preservation, preflight misuse validation, Stage 5BD plan preservation, active-lineage preservation, handoff continuity, credential-redaction policy, and Stage 5CX next-stage routing. Treat the preflight as non-authorizing: it creates no real decision package, selects no option, creates no approval records, activates no input, generates no bytes, and executes nothing.

## Stage 5BQ Note

Stage 5BQ is a metadata-only inactive-branch dry-run planning layer. Use `libreprimus token-block validate-stage5bq` for Stage 5BP findings integration, inactive String 4 planning context, dry-run constraint updates, no-active-ingestion proof, future dry-run requirements, Stage 5BD lineage preservation, DWH quarantine, guardrails, and Stage 5BR next-stage routing. Stage 5BR follow-up work should review the fail-closed planning constraints while keeping Deep Research bodies, full String 4 bodies, decoded bytes, reconstructed streams, raw iddqd-v2/archive/Fandom/spreadsheet files, generated outputs, and active manifest changes out of scope.

## Stage 5BN Note

Stage 5BN is a metadata-only String 4 unsupported-position source-gap layer. Use `libreprimus token-block validate-stage5bn` for the target record, Stage 5AW option-gap audit, local spreadsheet target-cell audit, coordinate context, source-evidence synthesis, inactive addendum, source-gap closure, DWH quarantine, lineage preservation, guardrails, and Stage 5BO next-stage routing. Stage 5BO follow-up work should review or integrate the inactive `0l` addendum while keeping full String 4 bodies, decoded bytes, reconstructed streams, raw iddqd-v2/archive/Fandom/spreadsheet files, generated outputs, and active manifest changes out of scope.

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
- Run the Stage 5AH stage-ledger, operational-map coverage, and current/next-stage checks after current-stage updates so Stage 5DD prompts inherit current source-of-truth labels.
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

## Stage 5BN Navigation

Stage 5BN implementation is under `python/libreprimus/token_block/stage5bn.py`; CLI commands are documented in `docs/reference/token-block-cli.md`. The generated Stage 5BN reports remain ignored under `experiments/results/token-block/stage5bn/` and `experiments/results/historical-route/stage5bn/`. The local completion summary is `codex-output/stage5bn-codex-completion.md`; do not create or use `codex_output/` for current handoffs.

## Stage 5BO Navigation

Stage 5BO implementation is under `python/libreprimus/token_block/stage5bo.py`; CLI commands are documented in `docs/reference/token-block-cli.md`. The generated Stage 5BO reports remain ignored under `experiments/results/token-block/stage5bo/` and `experiments/results/historical-route/stage5bo/`. The local completion summary is `codex-output/stage5bo-codex-completion.md`; do not create or use `codex_output/` for current handoffs.

## Stage 5BQ Navigation

Stage 5BQ implementation is under `python/libreprimus/token_block/stage5bq.py`; CLI commands are documented in `docs/reference/token-block-cli.md`. The generated Stage 5BQ reports remain ignored under `experiments/results/token-block/stage5bq/`. The local completion summary is `codex-output/stage5bq-codex-completion.md`; do not create or use `codex_output/` for current handoffs.

For Stage 5BU reviewability work, start with `docs/onboarding/stage5bu-lineage-path-reviewability-hardening-workflow.md` and run `token-block validate-stage5bu-lineage-paths`, `validate-stage5bu`, and the hardened `validate-stage5bs`.

For Stage 5BW inactive-sidecar planning-ingestion preflight work, start with `docs/onboarding/stage5bw-inactive-sidecar-planning-ingestion-workflow.md` and run `token-block build-stage5bw`, `validate-stage5bw`, and `stage5bw-summary`. Treat the sidecar as proposed-only and inactive.

For Stage 5BY inactive-sidecar planning-manifest scaffold work, start with `docs/onboarding/stage5by-inactive-sidecar-planning-manifest-workflow.md` and run `token-block build-stage5by`, `validate-stage5by-source-digest-uniqueness`, `validate-stage5by-sidecar-gates`, `validate-stage5by`, and `stage5by-summary`. Treat the sidecar as scaffolded inactive and no-execution only.

For Stage 5CA inactive-sidecar review-contract hardening work, start with `docs/onboarding/stage5ca-inactive-sidecar-review-contract-workflow.md` and run `token-block build-stage5ca`, the focused Stage 5CA validators, `validate-stage5ca`, and `stage5ca-summary`. Treat the sidecar as inactive review-contract metadata only.

For Stage 5CC active-planning-input preflight work, start with `docs/onboarding/stage5cc-active-planning-input-preflight-workflow.md` and run `token-block build-stage5cc`, the focused Stage 5CC validators, `validate-stage5cc`, and `stage5cc-summary`. Treat the active-planning proposal as unperformed and unauthorized; no byte-stream or execution gate opens in this stage.

For Stage 5CE proposal-package work, start with `docs/onboarding/stage5ce-active-planning-input-proposal-package-workflow.md` and run `token-block build-stage5ce`, the focused Stage 5CE validators, `validate-stage5ce`, and `stage5ce-summary`. Treat the package as review-only; future operator plus Deep Research approval is required before any activation-capable stage.

For Stage 5CG approval-gate decision-scaffold work, start with `docs/onboarding/stage5cg-approval-gate-decision-scaffold-workflow.md` and run `token-block build-stage5cg`, the focused Stage 5CG validators, `validate-stage5cg`, and `stage5cg-summary`. Treat the decision records as scaffolds only; operator approval and Deep Research acceptance remain absent and unsatisfied.

For Stage 5CI approval-record template hardening work, start with `docs/onboarding/stage5ci-approval-record-template-hardening-workflow.md` and run `token-block build-stage5ci`, the focused Stage 5CI validators, `validate-stage5ci`, and `stage5ci-summary`. Treat the operator approval, Deep Research acceptance, combined approval gate, and activation-decision records as future templates only; no actual approval, activation, active input, byte stream, or execution is authorized.

For Stage 5CK approval-record fixture-pack work, start with `docs/onboarding/stage5ck-approval-record-fixture-pack-workflow.md` and run `token-block build-stage5ck`, the focused Stage 5CK fixture validators, `validate-stage5ck`, and `stage5ck-summary`. Treat every fixture record as synthetic negative validation coverage only; no actual approval, acceptance, activation, active input, byte stream, or execution is authorized.

For Stage 5CM approval-record readiness-boundary work, start with `docs/onboarding/stage5cm-approval-record-readiness-boundary-workflow.md` and run `token-block build-stage5cm`, the focused Stage 5CM boundary validators, `validate-stage5cm`, and `stage5cm-summary`. Treat every fixture, template, scaffold, and review-package record as non-authorising unless a future real approval-record stage explicitly creates and validates real records.

For Stage 5CO real approval-readiness transition work, start with `docs/onboarding/stage5co-real-approval-record-readiness-workflow.md` and run `token-block build-stage5co`, the focused Stage 5CO readiness/preservation/gate validators, `validate-stage5co`, and `stage5co-summary`. Treat every Stage 5CO record as transition-planning metadata only; real approval, Deep Research acceptance, activation, active input, byte-stream generation, and execution remain false.

For Stage 5CQ operator-decision package scaffold work, start with `docs/onboarding/stage5cq-operator-decision-package-scaffold-workflow.md` and run `token-block build-stage5cq`, the focused Stage 5CQ findings/package/blocker/gate/preservation/handoff validators, `validate-stage5cq`, and `stage5cq-summary`. Treat every Stage 5CQ record as review-integration metadata only; operator decisions, real approval, Deep Research acceptance, activation, active input, byte-stream generation, and execution remain false.

For Stage 5CS operator-decision readiness/options work, start with `docs/onboarding/stage5cs-operator-decision-readiness-options-workflow.md` and run `token-block build-stage5cs`, the focused Stage 5CS findings/readiness/options/nonselection/blocker/gate/preservation/handoff validators, `validate-stage5cs`, and `stage5cs-summary`. Treat every Stage 5CS record as review-integration metadata only; the six decision options remain unselected, and real operator decisions, real approvals, Deep Research acceptance, activation, active input, byte-stream generation, and execution remain false.

For Stage 5CU option negative-fixture hardening work, start with `docs/onboarding/stage5cu-option-negative-fixture-hardening-workflow.md` and run `token-block build-stage5cu`, the focused Stage 5CU findings/options/fixture/misuse/nonselection/blocker/gate/preservation/handoff validators, `validate-stage5cu`, and `stage5cu-summary`. Treat every Stage 5CU record as negative validation metadata only; the six options remain unselected, and real operator decisions, real approvals, Deep Research acceptance, activation, active input, byte-stream generation, and execution remain false.

For Stage 5CW real-decision package preflight work, start with `docs/onboarding/stage5cw-real-decision-package-preflight-workflow.md` and run `token-block build-stage5cw`, the focused Stage 5CW findings/preflight/requirements/misuse/preservation/nonselection/blocker/gate/handoff validators, `validate-stage5cw`, and `stage5cw-summary`. Treat every Stage 5CW record as review-only preflight metadata; it does not create a valid real-decision package or authorize a future gate by itself.

For Stage 5DA operator choice / pause scaffold work, start with `docs/onboarding/stage5da-operator-choice-pause-scaffold-workflow.md` and run `token-block build-stage5da`, the focused Stage 5DA findings/scaffold/nonselection/pause/blocker/preservation/gate/handoff/governance validators, `validate-stage5da`, and `stage5da-summary`. Treat every Stage 5DA record as review-only scaffold metadata; it does not select an option, select an explicit pause, create a real choice/pause record, create a valid real-decision package, or authorize a future gate by itself.

For Stage 5DC operator choice record work, start with `docs/onboarding/stage5dc-operator-choice-record-workflow.md` and run `token-block build-stage5dc`, the focused Stage 5DC findings/choice/selected-option/unselected-options/pause/noncreation/gate/preservation/handoff/governance validators, `validate-stage5dc`, and `stage5dc-summary`. Treat the selected option as record-preparation metadata only; it does not create a real operator approval record or authorize approval, activation, active input, byte streams, or execution.
