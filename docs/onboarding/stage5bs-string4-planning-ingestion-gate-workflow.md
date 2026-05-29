# Stage 5BS String 4 Planning-Ingestion Gate Workflow

Use Stage 5BS records when reviewing whether the String 4 inactive sidecar may ever influence a future runner.

Required commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bs-planning-ingestion-gate
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bs
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bs-summary
```

Operational rule:

- Treat String 4 as `inactive_branch_context_only`.
- Treat `data/token-block/stage5bs-string4-planning-ingestion-gate.yaml` as the gate between review context and any future planning ingestion.
- Treat `data/token-block/stage5bs-future-runner-citation-policy.yaml` as fail-closed: a future runner that cannot cite the required Stage 5BO, Stage 5BQ, and Stage 5BS records must not ingest String 4.
- Keep Stage 5BD dry-run records valid unless a later explicit prompt supersedes them.
- Do not use ignored Deep Research bodies, Codex completion summaries, raw iddqd-v2/archive/Fandom files, review-pack bodies, or full String 4 bodies as source truth.

Stage 5BS is not execution permission. It does not authorize active input, dry-run ingestion now, byte-stream generation, variant materialisation, token-block execution, DWH/hash search, decode, score, OCR/AI/image/stego/audio tooling, CUDA, benchmarks, website expansion, method-status upgrades, canonical-corpus activation, page-boundary finalisation, or solve claims.
