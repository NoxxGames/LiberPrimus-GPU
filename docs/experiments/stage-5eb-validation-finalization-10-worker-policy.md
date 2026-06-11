# Stage 5EB - Validation Finalization and 10-Worker Policy

Stage 5EB is validation infrastructure, not a cryptanalytic experiment.

It records the final local validation policy before the third Source Browser number-fact review batch:

- local staged-validation defaults/caps are 10 workers and 10 pytest workers;
- full serial pytest is not a default completion requirement and is available only through `full-serial-rare`;
- current-stage registry final commit and CI status are recorded through external post-push handoff, not self-referential fields in the same commit;
- generic stage aliases such as `stage-5eb`, `stage5eb`, `5eb`, and `eb` route to the same token-block validators;
- pytest shard summaries include test files, estimated weights, and rerun commands;
- failing-slice helpers support rerunning the failing subset before rerunning full parallel validation;
- Source Browser number-fact overlay cache reuse is recorded as a reviewability/performance boundary.

Stage 5EB keeps number-fact review batch 3 deferred to Stage 5EC. It does not add source-lock evidence, overlays, direct number-fact backfill, route extraction, byte streams, execution, CUDA, scoring, benchmarks, canonical corpus activation, page-boundary finalisation, or solve claims.

Primary commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5eb
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5eb
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5eb-summary
.\scripts\ci\run-stage-validation.ps1 -Stage stage5eb -Profile stage-fast
.\scripts\ci\run-stage-validation.ps1 -Stage stage5eb -Profile full-parallel -Workers 10 -PytestWorkers 10
```
