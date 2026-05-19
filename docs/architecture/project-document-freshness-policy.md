# Project Document Freshness Policy

Persistent documentation is part of the architecture. Stale current-state claims can make Codex and contributors plan against obsolete assumptions.

## Required Updates

Every future stage must check and update relevant `.md` and `.txt` files when any of these change:

- stage status;
- roadmap or next-stage direction;
- experiment queue or method-family status;
- method retirement or reopening;
- raw/generated data policy;
- CLI behaviour or command surface;
- source-of-truth hierarchy or onboarding maps;
- Deep Research reports or user direction that changes the plan;
- schema, result-record, or output-family behaviour.

At minimum, check `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `CIPHER_CATALOG.md`, `docs/roadmap/staged-plan.md`, tutorials, and `docs/wiki-source`.

If no documentation needs updates, the stage final report must state why.

## Stage 3Z Onboarding Maps

Stage 3Z adds the onboarding maps under `docs/onboarding/`. These maps are public current-state navigation aids:

- `start-here.md`
- `source-of-truth-map.md`
- `codex-navigation-map.md`
- `deep-research-handoff-map.md`
- `contributor-module-map.md`
- `newcomer-task-lanes.md`
- `private-generated-data-map.md`

Update these maps when the source-of-truth hierarchy, private/generated paths, module layout, Deep Research handoff flow, or newcomer task lanes change.

## Direction-Change Checklist

When project direction changes:

1. Update `docs/roadmap/staged-plan.md`.
2. Add or update a record in `data/research/project-direction-change-records-v0.yaml`.
3. Update `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` if public/current state changes.
4. Update relevant reference docs, tutorials, and `docs/wiki-source/**`.
5. Run `libreprimus research-synthesis validate` and `libreprimus consistency check-state-drift`.

## Stage 4B Source-Lock And Observation Updates

When source-lock, visual-observation, negative-control, or disabled-manifest records change, update the matching reference docs, staged plan, research-synthesis ledgers, `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `CIPHER_CATALOG.md`, and tutorials/wiki-source where public workflow guidance changes.

Stage 4B records are durable context but not solve evidence. Future doc updates must preserve the distinction between public source-lock targets, review-only observations, disabled experiment manifests, and generated ignored diagnostics.

## Required Doc Update Matrix

- Stage status changes: `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, staged plan.
- Experiment queue changes: `EXPERIMENTS.md`, staged plan, relevant manifest docs.
- Method family retired/reopened: method-retirement ledger, `CIPHER_CATALOG.md`, staged plan.
- Data policy or private/generated paths change: private/generated data map, `.gitignore`, `DATASET.md` if applicable.
- CLI behavior changes: CLI reference docs, tutorials, command-surface tests.
- Deep Research handoff changes: Deep Research handoff map, staged plan, direction-change records.

## Historical References

Historical stage wording is allowed in `docs/development-logs/**`, `research-log/**`, and clearly archival sections. Operational docs must not describe old stages as current.

## Validation

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```
