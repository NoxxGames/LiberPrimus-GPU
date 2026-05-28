# Operational File Map

Stage 5AB added `data/project-state/operational-file-map.yaml` as the maintained lifecycle map for documents that carry current operational state. Stage 5AH updates that map for stage-ledger staleness coverage, Stage 5AI updates it for curated bundle metadata, Stage 5AJ updates it for UsefulFiles integration and extraction-fidelity policy, Stage 5AK updates it for community-facts claim curation, Stage 5AL updates it for website-ingest/Deep Research export staging, Stage 5AM updates it for the static research index renderer, Stage 5AN updates it for the private content pack and hosted private-content library, Stage 5AP updates it for the page 49-51 token-block source-lock, Stage 5AR updates it for original-image coordinate locking, Stage 5AT updates it for token case-review pack records, Stage 5AU updates it for review-pack v2 usability repair and Stage 5AV manual review direction, Stage 5AW updates it for decision-parser repair records, Stage 5AX updates it for parallel validation records, Stage 5AY updates it for bounded preflight design records, Stage 5AZ updates it for repaired bounded preflight manifest-integrity records, Stage 5BB updates it for no-execution runner-scaffold records, Stage 5BD updates it for no-byte-stream dry-run planning, Stage 5BF updates it for local historical-route source-lock plus Stage 5BG review planning, Stage 5BI updates it for Fandom/source-lock triage plus Stage 5BJ crosswalk closure, Stage 5BJ updates it for original/archive crosswalk closure plus Stage 5BK planning integration, and Stage 5BK updates it for historical-route planning constraints plus Stage 5BL review. The YAML record is the machine-readable source; this page is the human-readable guide.

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
  --expected-latest-stage "Stage 5BK" `
  --expected-next-stage "Stage 5BL"

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-operational-file-map-coverage

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-current-next-stage-consistency `
  --expected-latest-stage "Stage 5BK" `
  --expected-next-stage "Stage 5BL"
```
## Stage 5BF Coverage

The operational file map includes Stage 5BF archive location, inventory, trust-classification, technique-taxonomy, token-block impact, source-gap, Deep Research readiness, DWH context, guardrail, summary, CLI reference, onboarding workflow, and architecture records.

## Stage 5BI Coverage

The operational file map includes Stage 5BI Fandom page triage, item source-lock candidates, archive crosswalk candidates, media non-original policy, 2014 surface context, spreadsheet source-lock/reconciliation, source-gap, negative-control, guardrail, summary, next-stage decision, experiment note, and developer/research logs.

## Stage 5BK Coverage

The operational file map includes Stage 5BK iddqd-v2 source-root, tree, source-candidate, byte-string, transcription, translation/key-lineage, positive-control context, source-gap, planning constraint, family planning status, source-gap severity, Stage 5BJ errata, token-block constraint, guardrail, summary, next-stage decision, experiment note, CLI reference, developer log, and research log records. The local Codex completion summary under `codex-output/**` is intentionally ignored; `codex_output/**` is deprecated and must not be created for current handoffs.

## Stage 5BJ Coverage

The operational file map includes Stage 5BJ crosswalk closure plan, original/archive closure rows, exact 2014 surface source locks, Fandom page-body crosswalk records, boards-thread crosswalk records, high-priority candidate status, media-equivalence closure, source-gap updates, token-block lineage preservation, 2014 surface context closure, local archive/source-snapshot summaries, guardrails, summary, next-stage decision, experiment note, CLI reference, developer log, and research log. The local Codex completion summaries under `codex_output/**` and `codex-output/**` are intentionally ignored and are not part of committed operational state.
