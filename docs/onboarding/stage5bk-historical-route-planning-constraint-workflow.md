# Stage 5BK Historical-Route Planning Constraint Workflow

Use Stage 5BK records when a future review needs the current historical-route planning constraint layer.

Primary records:

- `data/historical-route/stage5bk-iddqd-v2-local-source-root.yaml`
- `data/historical-route/stage5bk-iddqd-v2-tree-summary.yaml`
- `data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml`
- `data/historical-route/stage5bk-historical-family-planning-status.yaml`
- `data/historical-route/stage5bk-source-gap-severity-register.yaml`
- `data/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata.yaml`
- `data/token-block/stage5bk-page49-51-string4-crosswalk.yaml`
- `data/token-block/stage5bk-token-block-lineage-preservation.yaml`
- `data/project-state/stage5bk-summary.yaml`
- `data/project-state/stage5bk-next-stage-decision.yaml`

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli historical-route validate-stage5bk
```

Stage 5BK is metadata-only. Raw iddqd-v2 files, raw archive files, Fandom page bodies, media, fonts, spreadsheets, full byte-string bodies, decoded bytes, and generated reports remain ignored and uncommitted.

The local Codex handoff root is `codex-output/`. The older `codex_output/` spelling is deprecated historical context and must not be created or used for current handoffs.
