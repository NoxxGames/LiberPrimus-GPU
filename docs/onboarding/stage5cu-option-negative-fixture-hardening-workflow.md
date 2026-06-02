# Stage 5CU Option Negative-Fixture Hardening Workflow

Use Stage 5CU records when reviewing whether the Stage 5CS six-option operator-decision scaffold is protected against accidental misuse. They are review metadata only.

Stage 5CU consumes the Stage 5CT `accept_with_warnings` review outcome. It preserves the Stage 5CS readiness package and unselected six-option scaffold, records the stale Stage 5CS ignored completion-summary warning as non-authoritative process context, and creates adversarial negative fixtures proving scaffolds, readiness packages, templates, fixtures, and review packages cannot satisfy real operator-decision or approval gates.

Run:

```powershell
python -m libreprimus.cli token-block build-stage5cu
python -m libreprimus.cli token-block validate-stage5cu-stage5ct-findings
python -m libreprimus.cli token-block validate-stage5cu-decision-options-preservation
python -m libreprimus.cli token-block validate-stage5cu-decision-option-negative-fixtures
python -m libreprimus.cli token-block validate-stage5cu-real-decision-negative-fixtures
python -m libreprimus.cli token-block validate-stage5cu-option-selection-misuse
python -m libreprimus.cli token-block validate-stage5cu-options-nonselection
python -m libreprimus.cli token-block validate-stage5cu-real-record-blocker
python -m libreprimus.cli token-block validate-stage5cu-combined-gate
python -m libreprimus.cli token-block validate-stage5cu-activation-nonauthorization
python -m libreprimus.cli token-block validate-stage5cu-stage5cs-preservation
python -m libreprimus.cli token-block validate-stage5cu-prior-stage-preservation
python -m libreprimus.cli token-block validate-stage5cu-sidecar-gates
python -m libreprimus.cli token-block validate-stage5cu-handoff-continuity
python -m libreprimus.cli token-block validate-stage5cu
python -m libreprimus.cli token-block stage5cu-summary
```

Expected review facts:

- Decision options remain `6`, all unselected, with `selected_option_id: null`.
- Decision-option negative fixtures count is `41`.
- Option-selection misuse rows count is `13`.
- Real-decision negative fixture target classes count is `10`.
- Stage 5BD run-plan IDs remain `10`.
- Active-lineage records remain `8`.
- No-active, no-byte, and no-execution gates remain closed.
- `codex-output/stage5cu-codex-completion.md` is local and ignored; `codex_output/` must not be used.

The next recommended stage is Stage 5CV Deep Research review of this metadata package. Stage 5CU does not select an option, create real operator decisions or approvals, authorize active planning input, activate String 4, generate bytes, execute token-block work, run DWH/hash search, decode, score, run CUDA, benchmark, publish website content, or make solve claims.
