

## Stage 6H Operational Files

- `data/project-state/stage6h-summary.yaml`: Stage 6H repair/source-lock summary.
- `data/token-block/stage6h-stage6i-manifest-input-addendum.yaml`: explicit Stage 6I handoff input addendum.
- `data/operator-console/source-browser/number-fact-overlays/stage6h-dot-angle-right-triangle-source-lock-overlays.yaml`: required review-only Source Browser overlays.
- `data/token-block/stage6h-future-diagnostic-registry.yaml`: disabled future diagnostics.
- `codex-output/stage6h-codex-completion.md`: ignored local completion handoff path after Stage 6H.

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
  --expected-latest-stage "Stage 6H" `
  --expected-next-stage "Stage 6I"

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-operational-file-map-coverage

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-current-next-stage-consistency `
  --expected-latest-stage "Stage 6H" `
  --expected-next-stage "Stage 6I"
```

## Stage 5EC Coverage

The operational file map includes Stage 5EC number-fact review batch 003, triangle/Page32/token-static/music/self-reference NumberFactCard overlay collection records, review-batch result records, Source Browser loadability evidence, Stage 5EB validation-policy preservation, Stage 5DX/5DW/5DV/5DU preservation, Stage 5DG/5BD/active-lineage preservation, closed-gate proofs, developer log, experiment note, and research log. Stage 5EC reviews 20 selected source-lock entries and adds 25 review-only overlays. Stage 5EC performs no historical source-lock rewrite, source-lock evidence update, direct source-record fact backfill, target selection, route extraction, byte-stream generation, OCR/image/audio/stego/native/VM/CUDA/scoring/benchmark work, activation, or solve claim. Generated diagnostics, raw third-party files, local GUI caches, and local `codex-output/**` handoffs remain ignored.

## Stage 5ED Coverage

The operational file map includes Stage 5ED number-fact review batch 004, DiskCipher/visual-method/route-context NumberFactCard overlay collection records, review-batch result records, Source Browser loadability evidence, Stage 5EC overlay preservation, Stage 5EB validation-policy preservation, older preservation records, closed-gate proofs, developer log, experiment note, and research log. Stage 5ED reviews 20 selected source-lock entries and adds 25 review-only overlays. Stage 5ED performs no historical source-lock rewrite, source-lock evidence update, direct source-record fact backfill, target selection, route extraction, byte-stream generation, OCR/image/audio/stego/native/VM/CUDA/scoring/benchmark work, activation, or solve claim. Generated diagnostics, raw third-party files, local GUI caches, and local `codex-output/**` handoffs remain ignored.

## Stage 5EB Coverage

The operational file map includes Stage 5EB validation finalization, parallel-worker policy, serial-pytest policy, current-stage registry finalization, generic stage-wrapper repair, doc-tier policy, pytest shard/rerun policy, Source Browser cache-reuse evidence, Stage 5EA preservation, active-lineage preservation, closed-gate proofs, developer log, experiment note, and research log. Stage 5EB performs no number-fact review batch, source-lock evidence update, overlay creation, route extraction, byte-stream generation, execution, or solve claim. Generated validation diagnostics, raw third-party files, local GUI caches, and local `codex-output/**` handoffs remain ignored.

## Stage 5DZ Coverage

The operational file map includes Stage 5DZ Triangle/Page32 bounded-findings source-lock records, Page32 and PDD153 review summaries, Source Browser overlay and review-batch result records, Source Browser loadability evidence, ChatGPT context update evidence, preservation records, closed-gate proofs, developer log, experiment note, and research log. Stage 5DZ source-locks assistant/operator bounded findings for PDD153 triangle and Page32. Stage 5DZ does not select a target. Stage 5DZ does not execute routes or produce route streams. Stage 5DZ does not generate byte streams. Stage 5DZ does not perform image forensics/OCR. Stage 5DZ does not accept a solve claim. Number-fact review batch 3 is deferred to Stage 5EA. Raw third-party files, generated diagnostics, and local `codex-output/**` handoffs remain ignored.

## Stage 5DY Coverage

The operational file map includes Stage 5DY validation profile, parallel policy, consistency policy, stage-isolation, non-mutating validator, shared-schema, preservation, closed-gate, developer log, experiment note, and research log records. Stage 5DY records the Stage 5DX validation tooling problems, but it does not perform number-fact batch 3 or rewrite historical source-lock records. Generated validation diagnostics, raw third-party files, local GUI caches, and local `codex-output/**` handoffs remain ignored.

## Stage 5DX Coverage

The operational file map includes Stage 5DX visual/red-heading/transform number-fact overlay collection records, review-batch results, Source Browser loadability evidence, preservation records, closed-gate proofs, developer log, and research log. Historical source-lock records are not rewritten; raw third-party files, generated diagnostics, local GUI caches, and local `codex-output/**` handoffs remain ignored.

## Stage 5DV Coverage

The operational file map includes Stage 5DV Source Browser performance/path-canonicalization repair summaries, path/performance/cache policies, validation cases, ChatGPT context hardening, preservation records, closed-gate proofs, developer log, experiment note, and research log. Raw third-party files, generated diagnostics, local GUI caches, thumbnails, and local `codex-output/**` handoffs remain ignored.

## Stage 5DT Coverage

The operational file map includes Stage 5DT NumberFactCard configuration, review states, overlay scaffold, review-batch plan, reviewability audit, GUI summary, preservation records, closed-gate proofs, developer log, experiment note, and research log. Raw third-party files, generated diagnostics, local GUI caches, and local `codex-output/**` handoffs remain ignored.

## Stage 5DS Coverage

The operational file map includes Stage 5DS expanded Music/Ouroboros/token-block static source-lock metadata, source-browser loadability, ChatGPT context update, preservation records, closed-gate proofs, experiment note, developer log, and research log. Raw `third_party/CicadaMusic/**` files and local `codex-output/**` handoffs remain ignored.
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

## Stage 5DL Coverage

The operational file map includes Stage 5DL project-state, historical-route, source-harvester, token-block, schema, CLI reference, experiment note, and developer log records. Raw local NumberTriangleStuff, DiskCipherStuff, RedditStuff, and koan-page files are not committed; generated reports under `experiments/results/token-block/stage5dl/**` and local handoff under `codex-output/stage5dl-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5DM Coverage

The operational file map includes Stage 5DM project-state, historical-route, source-harvester, token-block, schema, experiment note, developer log, and research-log records. Raw local visual sources and web bodies are not committed; generated reports under `experiments/results/token-block/stage5dm/**` and local handoff under `codex-output/stage5dm-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5DN Coverage

The operational file map includes Stage 5DN project-state, historical-route, source-harvester, token-block, schema, experiment note, and developer log records. Raw local DiskCipher source files are not committed; generated reports under `experiments/results/token-block/stage5dn/**` and local handoff under `codex-output/stage5dn-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5DO Coverage

The operational file map includes Stage 5DO project-state, historical-route, source-harvester, token-block, schema, experiment note, and developer log records. Raw local NumberFacts/PotentialHint source files are not committed; generated reports under `experiments/results/token-block/stage5do/**` and local handoff under `codex-output/stage5do-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5DP Coverage

The operational file map includes Stage 5DP project-state, historical-route, source-harvester, token-block, schema, experiment note, and developer log records. Raw local RedditStuff source files are not committed; generated reports under `experiments/results/token-block/stage5dp/**` and local handoff under `codex-output/stage5dp-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5DQ Coverage

The operational file map includes Stage 5DQ project-state, operator-console package, Source Browser config, schema, CLI reference, experiment note, and developer log records. Runtime caches under `.cache/operator-console/**`, GUI thumbnails/logs, generated diagnostics, and local handoff under `codex-output/stage5dq-codex-completion.md` are intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

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

<!-- BEGIN stage5ef -->
## Stage 5EF Operational Map Amendment

Stage 5EF records current-truth, doc update-policy, context-pack, plan-mode, drift-audit, automation-template,
advisory-hook, and skill-readiness files in `data/project-state/operational-file-map.yaml`.
<!-- END stage5ef -->

<!-- BEGIN stage5eg -->
## Stage 5EG Operational Map Note

Stage 5EG adds `.codex/` project-local hook and agent declarations plus daily doc-staleness automation docs. Hooks are declared only until operator trust.
<!-- END stage5eg -->

<!-- BEGIN stage5ei -->
## Stage 5EI Operational Map Update

Use `data/project-state/current-stage-state.yaml` for latest/next-stage truth. Stage 5EI is complete and Stage 6 is the next routed readiness stage. Older examples that mention Stage 5EI as batch 006 are historical and must not be used as current routing.
<!-- END stage5ei -->

<!-- stage6:start -->
## Stage 6 Operational Map Update

Stage 6 records live under `data/project-state/stage6-*`, `data/source-harvester/stage6-*`, `data/token-block/stage6-*`, and `data/historical-route/stage6-*`. Generated completion handoff remains ignored under `codex-output/stage6-codex-completion.md`.
<!-- stage6:end -->

<!-- stage6b:start -->
## Stage 6B Operational Files

Stage 6B operational records live under `data/project-state/stage6b-*`, `data/token-block/stage6b-*`, and `data/source-harvester/stage6b-*`. Hook reports are ignored local output under `experiments/results/doc-drift/` and must not be staged.
<!-- stage6b:end -->

<!-- stage6c:start -->
## Stage 6C Operational Files

Stage 6C primary records live under `data/project-state/`, `data/historical-route/`, `data/token-block/`, `data/source-harvester/`, and `data/operator-console/source-browser/number-fact-overlays/`. The local handoff lives under ignored `codex-output/`.
<!-- stage6c:end -->

<!-- stage6d:start -->
## Stage 6D Operational Files

Stage 6D primary records live under `data/project-state/`, `data/historical-route/`, `data/token-block/`, `data/source-harvester/`, and `data/operator-console/source-browser/number-fact-overlays/`. Hook/automation reports under `experiments/results/doc-drift/` and the completion handoff under `codex-output/` are ignored local outputs.
<!-- stage6d:end -->

<!-- stage6e:start -->
## Historical Stage 6E Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6E classified all stale-current warning-domain findings into named buckets, installed bounded report-only preprompt doc-staleness advisory behavior, source-locked finite bridge facts, superseded the stale Stage 6B Stage 6C token-block projection precondition, and built Stage 6F source-root/probe traceability inputs.

Stage 6E did not create a final Stage 7 manifest, finalize an archive-run contract, create a result archive, run probes, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6e:end -->

<!-- stage6f:start -->
## Historical Stage 6F Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6F repaired malformed/stale current mirrors, added file-content validators for high-risk docs, preserved Stage 6E source-lock payloads through a supersession layer, added preflight self-report exclusion, verified report-only hook behavior where local launcher tests can support it, recorded the Ciada/Cicada source-root alias policy, crosslinked the dju-bei backlog gap, and installed strict Codex acceptance criteria.

Stage 6F did not create a final Stage 7 manifest, finalize an archive-run contract, create result archives, run probes, add new theory records, add overlays, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6f:end -->

<!-- stage6g:start -->
## Stage 6G Operational Files

- `data/project-state/stage6g-summary.yaml`: Stage 6G repair summary.
- `data/token-block/stage6g-stage6h-manifest-input-addendum.yaml`: Stage 6H source-lock/readiness handoff addendum.
- `docs/onboarding/codex-acceptance-criteria.md`: reusable Codex acceptance criteria.
- `codex-output/stage6g-codex-completion.md`: ignored local completion handoff path after Stage 6G.
<!-- stage6g:end -->
