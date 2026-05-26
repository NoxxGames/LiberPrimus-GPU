# Token Case Review Pack V2 CLI

Stage 5AU extends `libreprimus token-block` with local-only review-pack repair commands.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block audit-stage5at-review-pack-usability
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5au-crop-geometry-policy
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5au-review-pack-v2
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5au-review-pack-v2
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5au-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5au
```

The build command reads ignored original page images for deterministic crop generation and writes the review pack under `human-review-packs/stage5au/token-case-review-v2/`. Validation works from committed metadata and the local ignored pack. No command performs OCR, AI/ML interpretation, LLM/vision token reading, semantic image interpretation, hash/preimage search, decode attempts, CUDA, benchmarks, or scored experiments.

Stage 5AV later consumes a filled local `decision-template.yaml` from this pack using `docs/reference/token-case-decision-integration-cli.md`. The filled template remains ignored and only compact metadata is committed.
