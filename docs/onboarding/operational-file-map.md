# Operational File Map

Stage 5AB added `data/project-state/operational-file-map.yaml` as the maintained lifecycle map for documents that carry current operational state. Stage 5AH updates that map for stage-ledger staleness coverage, Stage 5AI updates it for curated bundle metadata, Stage 5AJ updates it for UsefulFiles integration and extraction-fidelity policy, Stage 5AK updates it for community-facts claim curation, Stage 5AL updates it for website-ingest/Deep Research export staging, Stage 5AM updates it for the static research index renderer, Stage 5AN updates it for the private content pack and hosted private-content library, Stage 5AP updates it for the page 49-51 token-block source-lock, Stage 5AR updates it for original-image coordinate locking, Stage 5AT updates it for token case-review pack records, Stage 5AU updates it for review-pack v2 usability repair and Stage 5AV manual review direction, Stage 5AW updates it for decision-parser repair records, Stage 5AX updates it for parallel validation records, Stage 5AY updates it for bounded preflight design records, Stage 5AZ updates it for repaired bounded preflight manifest-integrity records, Stage 5BB updates it for no-execution runner-scaffold records, Stage 5BD updates it for no-byte-stream dry-run planning, Stage 5BF updates it for local historical-route source-lock plus Stage 5BG review planning, Stage 5BI updates it for Fandom/source-lock triage plus Stage 5BJ crosswalk closure, Stage 5BJ updates it for original/archive crosswalk closure plus Stage 5BK planning integration, Stage 5BK updates it for historical-route planning constraints plus Stage 5BL review, Stage 5BM updates it for String 4 branch-crosswalk repair plus Stage 5BN source-gap closure, Stage 5BN updates it for the inactive `0l` addendum plus Stage 5BO routing, Stage 5BO updates it for operator errata plus Stage 5BP review routing, Stage 5BQ updates it for inactive-branch dry-run planning plus Stage 5BR review routing, Stage 5BS updates it for closed planning-ingestion gate metadata, Stage 5BU updates it for active-lineage repair, Stage 5BW updates it for inactive-sidecar proposal metadata, Stage 5BY updates it for inactive planning-manifest scaffold records plus Stage 5BZ review routing, Stage 5CA updates it for inactive-sidecar review-contract hardening, Stage 5CC updates it for active-planning-input proposal preflight plus no-byte/no-execution transition gates, Stage 5CE updates it for review-only proposal packaging and operator/Deep Research gate design, Stage 5CG updates it for post-review approval-gate decision scaffolds, Stage 5CI updates it for approval-record template hardening and activation-decision validation preflight, Stage 5CK updates it for approval-record fixture packs plus activation-decision review packaging, Stage 5CM updates it for approval-record readiness-boundary hardening, fixture-vs-real boundary validation, credential-redaction policy, and 8-worker validation evidence, Stage 5CO updates it for real approval-readiness transition planning, Stage 5CQ updates it for operator-decision package scaffolding, Stage 5CS updates it for operator-decision readiness/options scaffolding, Stage 5CU updates it for option negative-fixture hardening, Stage 5CW updates it for review-only real-decision package preflight, Stage 5CY updates it for operator-facing option-selection decision preflight plus Stage 5CW validation-count reconciliation, Stage 5DA updates it for the operator choice / pause scaffold without selection, Stage 5DC updates it for the selected operator choice record, Stage 5DE updates it for the real operator approval preparation package, Stage 5DG updates it for the real operator approval record, Stage 5DI updates it for recent clue source-lock and pivot-readiness records, Stage 5DJ updates it for CicadaMusic source-lock and music-clue pivot-integration records, and Stage 5DK updates it for Fandom source-lock gap closure plus Page 56 hash-contract records. The YAML record is the machine-readable source; this page is the human-readable guide.

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
  --expected-latest-stage "Stage 5DK" `
  --expected-next-stage "Stage 5DL"

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-operational-file-map-coverage

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-current-next-stage-consistency `
  --expected-latest-stage "Stage 5DK" `
  --expected-next-stage "Stage 5DL"
```
## Stage 5BF Coverage

The operational file map includes Stage 5BF archive location, inventory, trust-classification, technique-taxonomy, token-block impact, source-gap, Deep Research readiness, DWH context, guardrail, summary, CLI reference, onboarding workflow, and architecture records.

## Stage 5BI Coverage

The operational file map includes Stage 5BI Fandom page triage, item source-lock candidates, archive crosswalk candidates, media non-original policy, 2014 surface context, spreadsheet source-lock/reconciliation, source-gap, negative-control, guardrail, summary, next-stage decision, experiment note, and developer/research logs.

## Stage 5BK Coverage

The operational file map includes Stage 5BK iddqd-v2 source-root, tree, source-candidate, byte-string, transcription, translation/key-lineage, positive-control context, source-gap, planning constraint, family planning status, source-gap severity, Stage 5BJ errata, token-block constraint, guardrail, summary, next-stage decision, experiment note, CLI reference, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5BM Coverage

The operational file map includes Stage 5BM Stage 5BL findings integration, review-packaging warning, String 4 source restatement, inverse policy, mismatch analysis, branch-membership, ambiguity coverage, planning constraint, source-gap severity, historical-family granularity, Stage 5BJ errata supersession, DWH quarantine, lineage preservation, future dry-run planning impact, guardrail, summary, next-stage decision, experiment note, workflow note, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5BN Coverage

The operational file map includes Stage 5BN target, source-evidence, Stage 5AW option-gap, local spreadsheet target-cell, coordinate-context, human-review manifest, proposed inactive addendum, source-gap closure, planning constraint, token-block lineage, source-gap severity, DWH quarantine, guardrail, Codex handoff, summary, next-stage decision, experiment note, workflow note, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5BO Coverage

The operational file map includes Stage 5BO decision-template correction source lock, token-case human-review errata, correction impact, inactive errata-aware option universe, String 4 after-errata branch membership, Stage 5BN addendum integration, source-gap closure, planning constraint, token-block lineage, future dry-run planning impact, source-gap severity, DWH quarantine, guardrail, Codex handoff, summary, next-stage decision, experiment note, workflow note, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5BS Coverage

## Stage 5DJ Coverage

The operational file map includes Stage 5DJ project-state, historical-route, source-harvester, token-block, schema, CLI reference, experiment note, developer log, and research log records. The local CicadaMusic raw files under `third_party/CicadaMusic/**`, generated reports under `experiments/results/token-block/stage5dj/**`, and local handoff under `codex-output/stage5dj-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5DK Coverage

The operational file map includes Stage 5DK project-state, historical-route, source-harvester, token-block, schema, CLI reference, experiment note, developer log, and research log records. Raw Fandom page bodies/images are not committed; generated reports under `experiments/results/token-block/stage5dk/**` and local handoff under `codex-output/stage5dk-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

The operational file map includes Stage 5BS reviewable stage-marker, validation-evidence, source-digest, reviewability-gap, findings-integration, planning-ingestion gate, future-runner citation policy, inactive-sidecar policy, active-ingestion blocker, no-active-ingestion proof, readiness matrix, manifest requirements, Stage 5BD preservation, active-manifest preservation, future-impact, source-gap, DWH, guardrail, Codex handoff, summary, next-stage, experiment note, workflow note, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

Historical Stage 5BQ coverage includes Stage 5BQ Stage 5BP findings integration, review-packaging warning, inactive branch planning context, operator-errata sidecar status, dry-run constraint update, no-active-ingestion proof, future dry-run requirements, active-manifest preservation, Stage 5BD lineage preservation, future planning impact, source-gap severity update, DWH quarantine, guardrail, Codex handoff, summary, next-stage decision, experiment note, workflow note, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5BJ Coverage

The operational file map includes Stage 5BJ crosswalk closure plan, original/archive closure rows, exact 2014 surface source locks, Fandom page-body crosswalk records, boards-thread crosswalk records, high-priority candidate status, media-equivalence closure, source-gap updates, token-block lineage preservation, 2014 surface context closure, local archive/source-snapshot summaries, guardrails, summary, next-stage decision, experiment note, CLI reference, developer log, and research log. The local Codex completion summaries under `codex_output/**` and `codex-output/**` are intentionally ignored and are not part of committed operational state.

Stage 5BU extends the operational file map with lineage-path erratum, path-resolution validation, summary, and workflow records.

Stage 5BW extends the operational file map with inactive-sidecar proposal, manifest-supersession preflight, active-lineage preservation, Stage 5BD plan preservation, validation-evidence, summary, and workflow records.

Stage 5BY extends the operational file map with Stage 5BX findings integration, Stage 5BW source-digest duplicate review, record-family filename-equivalence mapping, inactive planning manifest scaffold, no-execution planning-ingestion sidecar, no-active/no-byte-stream proofs, manifest-supersession carry-forward, active-lineage preservation, Stage 5BD plan preservation, validation evidence, source-digest, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CA extends the operational file map with Stage 5BZ findings integration, inactive sidecar review contract, exact future-runner citation contract, fail-closed trigger contract, activation-precondition contract, manifest-supersession preflight contract, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte-stream proofs, validation evidence, source-digest, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CC extends the operational file map with Stage 5CB findings integration, Stage 5CA contract preservation, exact fail-closed trigger and activation-precondition contracts, active-planning-input proposal preflight, no-byte-stream transition gate, no-execution transition gate, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte-stream proofs, DWH quarantine, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CG extends the operational file map with Stage 5CF findings integration, decision-scaffold metadata, Stage 5CE proposal/gate preservation, Stage 5CE wording review, no-byte-stream transition gate, no-execution transition gate, Stage 5BD plan preservation, active-lineage preservation, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CK extends the operational file map with Stage 5CJ findings integration, fixture-only future operator approval and Deep Research acceptance validation packs, activation-decision fixture pack, negative validation matrix, activation-decision review package, no-byte-stream transition gate, no-execution transition gate, Stage 5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CM extends the operational file map with Stage 5CL findings integration, approval-readiness boundary contract, fixture-vs-real record boundary, end-to-end boundary validation, real approval-readiness preflight, activation-decision gate hardening, Stage 5CK/5CI/5CG/5CE/5CC/5BD preservation, no-byte-stream transition gate, no-execution transition gate, active-lineage preservation, credential-redaction/no-secret policy, 8-worker validation evidence, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CO extends the operational file map with Stage 5CN findings integration, real approval-record readiness package, real operator approval readiness preflight, real Deep Research acceptance readiness preflight, combined-gate readiness preflight, activation-decision transition plan, future transition sequence, current missing-requirements register, real-record creation blocker, Stage 5CM/5CK/5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, credential-redaction policy preservation, review-packaging warning, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CQ extends the operational file map with Stage 5CP findings integration, reviewable stage marker, validation evidence, reviewability gap register, source-digest index, record-family filename-equivalence map, operator-decision package scaffold, operator-decision nonauthorization, combined-gate non-satisfaction, activation nonauthorization, real-record blocker, Stage 5CO/Stage 5CM/Stage 5CK/Stage 5CI/Stage 5CG/Stage 5CE/Stage 5CC/Stage 5BD preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff restoration, credential-redaction policy preservation, review-packaging warning, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CU extends the operational file map with Stage 5CT findings integration, Stage 5CS decision-options preservation, decision-option negative fixtures, real-decision negative fixtures, option-selection misuse validation, option-fixture isolation policy, Stage 5CQ/Stage 5CO/Stage 5CM/Stage 5CK/Stage 5CI/Stage 5CG/Stage 5CE/Stage 5CC/Stage 5BD preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff continuity, credential-redaction policy preservation, review-packaging warning, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CW extends the operational file map with Stage 5CV findings integration, real-decision package preflight, future real-decision package requirements, future option-selection preflight requirements, future real-record dependency preflight, preflight nonselection/nonauthorization proofs, preflight misuse validation, Stage 5CU negative-fixture preservation, Stage 5CS decision-options preservation, Stage 5CQ/Stage 5CO/Stage 5CM/Stage 5CK/Stage 5CI/Stage 5CG/Stage 5CE/Stage 5CC/Stage 5BD preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff continuity, credential-redaction policy preservation, review-packaging warning, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5CY extends the operational file map with Stage 5CX findings integration, Stage 5CW real-decision preflight preservation, operator-facing option-selection decision preflight, option-selection requirements, option-selection misuse validation, option nonselection proof, Stage 5CW validation-count reconciliation, Stage 5CW/Stage 5CU/Stage 5CS preservation, real-record blockers, combined-gate and activation nonauthorization proofs, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff continuity, credential-redaction policy preservation, governance-scope control, review-packaging warning, guardrail, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5DA extends the operational file map with Stage 5CZ findings integration, governance scope-control, operator choice / pause decision scaffold, choice/pause nonselection proof, explicit-pause nonactivation proof, real-record blocker, Stage 5CY preservation, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff policy, credential-redaction policy preservation, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5DC extends the operational file map with Stage 5DB findings integration, governance scope-control, operator choice decision record, selected-option record, unselected-options preservation, explicit-pause nonselection proof, real-approval noncreation proof, combined-gate and activation nonauthorization proofs, real-record boundary, Stage 5CY/5DA/5BD preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff policy, credential-redaction policy preservation, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5DE extends the operational file map with Stage 5DD findings integration, review-label anomaly record, governance scope-control, real operator approval preparation package, future approval-record requirements, Stage 5DC selected-option and choice preservation, unselected-options preservation, real-approval noncreation proof, combined-gate and activation nonauthorization proofs, real-record boundary, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, strict `codex-output` handoff policy, credential-redaction policy preservation, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5DG extends the operational file map with Stage 5DF findings integration, real operator approval record, operator approval scope, operator approval nonactivation proof, Stage 5DE preparation preservation, Stage 5DC choice/selected-option preservation, unselected-options preservation, Deep Research acceptance absence proof, combined-gate and activation nonauthorization proofs, real-record boundary, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte/no-execution transition gates, target-context preservation, strict `codex-output` handoff policy, credential-redaction policy preservation, summary, next-stage, workflow, developer-log, and research-log records.

Stage 5DI extends the operational file map with recent clue source-lock records, public web source locks, local iddqd-v2 and number-triangle crosswalks, route-candidate family index, pivot-readiness package, pivot-priority matrix, DWH quarantine reaffirmation, dinkus visual-marker metadata, Stage 5DG approval preservation, Stage 5BD plan preservation, active-lineage preservation, no-active/no-byte/no-execution gates, strict `codex-output` handoff policy, credential-redaction policy preservation, summary, next-stage, developer-log, experiment doc, and research-log records.
