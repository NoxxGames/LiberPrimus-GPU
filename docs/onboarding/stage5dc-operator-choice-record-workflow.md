# Stage 5DC Operator Choice Record Workflow

Stage 5DC records the explicit operator choice `prepare_real_operator_approval_record`. It is metadata-only: it creates a valid operator choice/pause decision record, but it does not create a real approval record or open any approval, activation, byte-stream, or execution gate.

## Source Records

- `data/project-state/stage5dc-summary.yaml`
- `data/project-state/stage5dc-next-stage-decision.yaml`
- `data/project-state/stage5dc-stage5db-findings-integration.yaml`
- `data/token-block/stage5dc-operator-choice-decision-record.yaml`
- `data/token-block/stage5dc-selected-option-record.yaml`
- `data/token-block/stage5dc-unselected-options-preservation.yaml`
- `data/token-block/stage5dc-explicit-pause-nonselection-proof.yaml`
- `data/token-block/stage5dc-real-approval-noncreation-proof.yaml`
- `data/token-block/stage5dc-combined-gate-non-satisfaction-proof.yaml`
- `data/token-block/stage5dc-activation-decision-nonauthorization-proof.yaml`

## Validation

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5dc
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dc
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dc-summary
```

Focused validators cover Stage 5DB findings, selected-option semantics, the five unselected options, explicit-pause nonselection, real-approval noncreation, combined-gate non-satisfaction, activation nonauthorization, Stage 5CY/5DA/5BD preservation, active-lineage preservation, sidecar gates, handoff continuity, governance-scope control, and credential-redaction policy.

Ignored diagnostics under `experiments/results/token-block/stage5dc/` and the local completion summary `codex-output/stage5dc-codex-completion.md` are not source truth and must not be committed. The deprecated `codex_output` root must remain absent.

Stage 5DD is the next review prompt. Before any future real operator approval record stage, Stage 5DD should review the selected-option record, noncreation proofs, closed gates, Stage 5BD preservation, and active-lineage preservation.
