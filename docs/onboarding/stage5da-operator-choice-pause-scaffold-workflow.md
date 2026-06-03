# Stage 5DA Operator Choice / Pause Scaffold Workflow

Stage 5DA records the post-review pause point after Stage 5CY and Stage 5CZ. It is metadata-only: it creates a scaffold for a future explicit operator choice or an explicit pause, but it does not select either path.

Use these source records first:

- `data/project-state/stage5da-summary.yaml`
- `data/project-state/stage5da-next-stage-decision.yaml`
- `data/project-state/stage5da-stage5cz-findings-integration.yaml`
- `data/token-block/stage5da-operator-choice-pause-decision-scaffold.yaml`
- `data/token-block/stage5da-operator-choice-pause-nonselection-proof.yaml`
- `data/token-block/stage5da-explicit-pause-nonactivation-proof.yaml`
- `data/token-block/stage5da-real-record-creation-blocker.yaml`

The scaffold preserves the exact six Stage 5CS options, keeps `selected_option_id: null`, records `explicit_pause_selected_now: false`, preserves Stage 5BD run-plan IDs, and keeps active-lineage paths unchanged. The no-active, no-byte-stream, and no-execution gates remain closed.

Validate the records with:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5da
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5da
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5da-summary
```

Ignored diagnostics under `experiments/results/token-block/stage5da/` and the local completion summary `codex-output/stage5da-codex-completion.md` are not source truth and must not be committed. The deprecated `codex_output` root must remain absent.

Stage 5DB is the next review prompt. After Stage 5DB, the project should require an explicit operator choice, an explicit pause, or a human stop; more generic preflight layers remain blocked unless a concrete defect is found.
