# Stage 5BK Historical-Route Planning Constraint Integration

Implemented Stage 5BK as a metadata-only historical-route planning constraint layer.

Work completed:

- Added `libreprimus historical-route` Stage 5BK locate, inventory, source-lock, planning-constraint, token-block impact, summary, validate, and alias commands.
- Added Stage 5BK schemas for iddqd-v2 source-lock addenda, planning constraints, token-block constraint updates, source-harvester policy records, summary, and next-stage decision records.
- Generated committed YAML metadata under `data/historical-route/`, `data/token-block/`, `data/source-harvester/`, and `data/project-state/`.
- Wrote ignored generated reports under `experiments/results/historical-route/stage5bk/` and `experiments/results/token-block/stage5bk/`.
- Wrote the local ignored Codex handoff at `codex-output/stage5bk-codex-completion.md` and did not create `codex_output/`.
- Added focused Stage 5BK tests for schemas, iddqd-v2 source root, byte strings, String 4 crosswalk, transcription/key lineage, planning constraints, guardrails, CLI, and ignore policy.

Local results:

- iddqd-v2 source root found: true.
- selected source path: `third_party/CiadaSolversIddqd_v2`.
- iddqd-v2 file count: 309.
- iddqd-v2 tree digest: `e9184492a54a437dd955fecc4c344cd662889d172ab8e8a89eb34b629247ad8b`.
- byte strings: 4.
- exact 512-hex strings: 4.
- String 1-3 Stage 5BJ crosswalks: 3.
- String 4 page49-51 crosswalk created: true.
- transcription locks: 2.
- translation/key-lineage records: 4.
- positive-control context records: 11.
- historical family planning statuses: 9.
- source-gap severity records: 7.
- Stage 5BJ errata warnings: 1.

Guardrails:

- No token-block execution was performed.
- No real token-block byte streams were generated.
- No 2014 surfaces were combined with page 49-51.
- No DWH/hash/preimage search was performed.
- No decode attempt was performed.
- No stego/audio/image/OCR/AI/CUDA/benchmark/scoring work was performed.
- No raw iddqd-v2, Fandom, archive, spreadsheet, media, font, full surface, decoded byte, or generated output files were committed.
- No method-status upgrade, website publication, canonical corpus activation, page-boundary finalisation, or solve claim was made.

Validation completed:

- `historical-route validate-stage5bk`: passed.
- Stage 5AX parallel validation wrapper with 16 workers and xdist: passed.
- Full serial `pytest -q tests/python`: 2047 passed.
- `ruff check python/libreprimus tests/python`: passed.
- PowerShell consistency wrapper: passed.
- Git Bash consistency wrapper with workspace venv Python: passed.
- Public-docs, lock-hash, workflow-static, wiki-source, and tutorial-to-wiki dry-run checks: passed.

Next selected stage: Stage 5BL - Deep Research review of historical-route planning constraints and iddqd-v2 source-lock integration, without execution.
