# Stage 5CG Approval-Gate Decision Scaffold

Stage 5CG is not an experiment. It is a metadata-only integration stage that consumes the Stage 5CF review of Stage 5CE and prepares future decision-record scaffolds.

Committed outputs:

- Stage 5CF findings integration, validation evidence, source-digest index, reviewability gap register, record-family equivalence map, summary, and next-stage records.
- Stage 5CE proposal-package preservation, Stage 5CE gate-design preservation, Stage 5CC contract preservation, Stage 5CE wording review, operator decision scaffold, Deep Research decision scaffold, combined approval-gate scaffold, active-planning-input decision scaffold, no-active-ingestion proof, no-byte/no-execution transition gates, Stage 5BD plan preservation, active-lineage preservation, and sidecar blocker records.
- DWH/source-gap/guardrail records and Codex handoff policy records.

The stage keeps `approval_gate_satisfied_now=false`, `activation_authorized_now=false`, `active_planning_input_authorized_now=false`, `string4_active_input_allowed=false`, `string4_dry_run_ingestion_allowed_now=false`, `manifest_supersession_performed=false`, and `execution_allowed=false`.

Ignored diagnostics are under `experiments/results/token-block/stage5cg/`. The local Codex handoff is `codex-output/stage5cg-codex-completion.md` and is not committed.
