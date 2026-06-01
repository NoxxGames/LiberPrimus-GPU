# Parallel Validation Workflow

Stage 5AX adds an opt-in local workflow for faster validation:

```powershell
.\scripts\ci\run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto
```

Use this during Codex implementation turns after normal targeted checks pass. Keep final git, GitHub, staging, issue, commit, push, and remote verification steps serial.

The workflow:

1. Builds `data/ci/stage5ax-parallel-validation-plan.yaml`.
2. Runs pytest through xdist or deterministic file sharding.
3. Runs read-only validation commands concurrently.
4. Writes ignored command logs under `experiments/results/ci/parallel-validation/stage5ax/`.
5. Writes compact committed summaries under `data/ci/` and `data/project-state/`.

Do not add mutating commands to the parallel-safe class. Generated-output-writing commands need isolated ignored outputs or must stay serial. Network, GitHub, commit, push, and manual operations stay serial.

Stage 5AY bounded token-block preflight design cites Stage 5AW repaired branch metadata and uses Stage 5AX as validation infrastructure only. Stage 5AZ repaired the duplicate variant-family ID; Stage 5BB uses Stage 5AX as validation infrastructure while building no-execution runner scaffold records; Stage 5BD uses it while validating no-byte-stream dry-run records. Stage 5CM sets the forward local worker cap to 8 for the wrapper and pytest-xdist, Stage 5CO preserves that cap for transition-readiness validation, and Stage 5CS preserves it for operator-decision readiness/options validation. Stage 5CT review should inspect Stage 5CS records, not generated Stage 5AX logs.
## Stage 5BD Status

Stage 5BD can be validated by the parallel-validation harness as local infrastructure only; timings are not benchmark evidence.
