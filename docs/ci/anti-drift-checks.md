# Anti-Drift Checks

## Purpose

Anti-drift checks keep long-lived project context aligned with the current repository state. They exist because stale operational docs can cause contributors and Codex sessions to plan against obsolete Stage 0 or Stage 2 assumptions.

## Checked Files

The state-drift checker reviews operational and public context files, including:

- `README.md`
- `STATUS.md`
- `ROADMAP.md`
- `AGENTS.md`
- `ARCHITECTURE.md`
- `CUDA_NOTES.md`
- `RESULTS_SCHEMA.md`
- `EXPERIMENTS.md`
- `TESTING.md`
- `docs/roadmap/staged-plan.md`
- `pyproject.toml`
- `docker/README.md`

Historical records under `docs/development-logs/**` and `research-log/**` are not rewritten or failed merely for old stage references.

## What Fails

The checker fails if critical facts drift:

- Stage 3V is not recorded as complete.
- Stage 3W consolidation is not recorded in current project state.
- Stage 3X is not recorded as complete in the staged plan.
- Stage 3Y result synthesis is missing from the staged plan.
- The canonical corpus is not explicitly inactive.
- Page boundaries are not explicitly reviewable.
- CUDA is not explicitly deferred.
- No-solve-claim policy is missing.
- Raw/generated output commit policy is missing.
- Discord raw-log privacy policy is missing.
- Local page-image non-commit policy is missing.
- The staged plan omits update/direction-change policy.

It also fails stale current-state claims such as:

- "current stage is Stage 0A"
- "current stage is Stage 0D"
- "Stage 0A scaffold" in package metadata or operational current-state text
- "no result schema" after result-store schemas exist
- "Stage 3I next" after Stage 3V

## Historical References

Historical references are allowed when they are clearly phrased as history, for example:

- "implemented since Stage 0A"
- "historical Stage 0D alignment"
- archival sections in stage logs

When editing public docs, prefer "Historical Stage 0A" over a heading that could be read as current status.

## Local Use

Run the focused check:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
```

Run it with the rest of the consistency suite:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

Validate the Stage 3Y research synthesis ledgers:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```

## Safe Update Process

When a stage completes:

1. Update `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md` together.
2. Update architecture, schema, testing, and tutorial docs only where the behavior or policy changed.
3. Update `data/research/` ledgers when method-family status, retirement, Deep Research influence, or direction changes.
4. Keep generated outputs and raw data ignored.
5. Run the anti-drift and research-synthesis checks before staging.
