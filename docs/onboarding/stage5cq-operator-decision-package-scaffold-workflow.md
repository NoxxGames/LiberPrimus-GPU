# Stage 5CQ Operator-Decision Package Scaffold Workflow

Stage 5CQ is a metadata-only review-integration stage. It consumes the Stage 5CP `accept_with_warnings` review of Stage 5CO, preserves the Stage 5CO real approval-readiness and activation-transition records, restores strict `codex-output` completion-summary handoff discipline, and creates a scaffold for a future operator-decision package.

It does not make the operator decision. It does not create real operator approval, Deep Research acceptance, combined-gate validation, activation-decision, active planning input, byte streams, or token-block execution.

## Inputs

- `data/token-block/stage5co-*`
- `data/token-block/stage5cm-*`
- `data/token-block/stage5ck-*`
- `data/token-block/stage5ci-*`
- `data/token-block/stage5cg-*`
- `data/token-block/stage5ce-*`
- `data/token-block/stage5cc-*`
- `data/token-block/stage5bd-*`
- Stage 5CP review context as compact metadata only.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5cq
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5cq
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5cq-summary
```

Focused validators are available for Stage 5CP findings, the operator-decision package scaffold, real-record blockers, combined-gate status, activation nonauthorization, Stage 5CO preservation, prior-stage preservation, sidecar gates, handoff restoration, and credential-redaction policy.

## Boundaries

Stage 5CQ requires:

- `operator_decision_package_status: scaffold_only`
- `real_approval_records_created: false`
- `real_deep_research_acceptance_records_created: false`
- `combined_approval_gate_satisfied_now: false`
- `activation_decision_valid_now: false`
- `active_planning_input_authorized_now: false`
- `active_planning_input_selected_now: false`
- `stage5bd_run_plan_id_count: 10`
- `active_lineage_record_count: 8`
- no-active, no-byte, and no-execution gates closed.

Generated diagnostics stay ignored under `experiments/results/token-block/stage5cq/`. The local Codex completion summary stays ignored at `codex-output/stage5cq-codex-completion.md`; `codex_output/` must remain absent and unused.
