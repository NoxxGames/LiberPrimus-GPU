# Stage 5CO Real Approval-Record Readiness Workflow

Use this workflow when reviewing Stage 5CO real approval-readiness transition metadata.

Stage 5CO is metadata-only. It packages the future path for real operator approval, real Deep Research activation acceptance, combined-gate validation, and activation-decision review, but it creates none of those real records now. Treat all Stage 5CO outputs as readiness and transition-planning records, not approval or execution authority.

## Required Checks

- Start from `data/project-state/stage5co-summary.yaml`.
- Confirm `stage5cn_verdict: accept_with_warnings`.
- Confirm real approval, real Deep Research acceptance, combined gate satisfaction, activation decision validity, active input authorization, active input selection, byte-stream generation, and execution are all false.
- Confirm `data/token-block/stage5co-current-missing-requirements-register.yaml` still lists the missing real records.
- Confirm `data/token-block/stage5co-stage5bd-plan-preservation.yaml` keeps 10 Stage 5BD run-plan IDs unchanged.
- Confirm `data/token-block/stage5co-active-lineage-preservation.yaml` keeps 8 active lineage records and the corrected Stage 5AW path.
- Confirm `data/source-harvester/stage5co-credential-redaction-policy-preservation.yaml` records no credential values.
- Confirm generated diagnostics remain ignored under `experiments/results/token-block/stage5co/`.
- Confirm `codex-output/stage5co-codex-completion.md` is ignored and `codex_output/` is absent.

## CLI

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5co
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5co-summary
```

Run focused validators when reviewing a specific boundary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-approval-readiness-package
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-real-operator-readiness
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-real-deep-research-readiness
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-real-combined-gate-readiness
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-activation-transition-plan
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-current-missing-requirements
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-real-record-blocker
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5co-sidecar-gates
```

Next stage: Stage 5CP Deep Research review of Stage 5CO, without execution.
