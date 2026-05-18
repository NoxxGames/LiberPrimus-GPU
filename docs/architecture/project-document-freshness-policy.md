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
- schema, result-record, or output-family behaviour.

At minimum, check `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `CIPHER_CATALOG.md`, `docs/roadmap/staged-plan.md`, tutorials, and `docs/wiki-source`.

If no documentation needs updates, the stage final report must state why.

## Historical References

Historical stage wording is allowed in `docs/development-logs/**`, `research-log/**`, and clearly archival sections. Operational docs must not describe old stages as current.

## Validation

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```
