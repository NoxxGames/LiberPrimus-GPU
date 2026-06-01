# Stage 5CM Approval-Record Readiness Boundary Workflow

Use this workflow when inspecting historical Stage 5CM approval-readiness boundary metadata. Stage 5CO packages the future real approval transition path, Stage 5CQ scaffolds the future operator-decision package, and Stage 5CR review is next.

## Commands

```powershell
python -m libreprimus.cli token-block build-stage5cm
python -m libreprimus.cli token-block validate-stage5cm-approval-readiness-boundary
python -m libreprimus.cli token-block validate-stage5cm-fixture-real-boundary
python -m libreprimus.cli token-block validate-stage5cm-end-to-end-readiness-boundary
python -m libreprimus.cli token-block validate-stage5cm-real-approval-readiness
python -m libreprimus.cli token-block validate-stage5cm-activation-decision-gate
python -m libreprimus.cli token-block validate-stage5cm-credential-redaction-policy
python -m libreprimus.cli token-block validate-stage5cm-sidecar-gates
python -m libreprimus.cli token-block validate-stage5cm
python -m libreprimus.cli token-block stage5cm-summary
```

Run the Stage 5AX parallel wrapper with at most 8 workers:

```powershell
.\scripts\ci\run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto
```

## Rules

- Treat Stage 5CM as boundary-hardening infrastructure only.
- Do not treat fixture, template, scaffold, or review-package records as real approval records.
- Do not create real approval, real Deep Research acceptance, valid activation decisions, active planning inputs, byte streams, or execution records.
- Do not reproduce credential-like strings from ignored reports or remotes.
- Use `codex-output/` for ignored handoffs; do not create or use `codex_output/`.
