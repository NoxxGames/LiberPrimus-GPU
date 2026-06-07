# Operator Console Source Browser v0

Stage 5DQ adds the Liber Primus Operator Console v0 Source Browser as local review infrastructure. The browser indexes committed metadata records, shows source-lock and candidate context, and provides explicit navigation to local paths, image paths, document paths, URLs, and the local `ChatGPT-ContextFile.md` when those references are present.

The Source Browser is not a puzzle runner. It does not run route extraction, OCR, image forensics, AI interpretation, scoring, DWH/hash search, byte-stream generation, CUDA, or source files. Missing local paths are review warnings because many referenced third-party files are intentionally ignored and not present on every checkout.

## Components

- `python/libreprimus/operator_console/`: shared console settings, optional GUI entrypoint, styles, resources, and CLI registration.
- `python/libreprimus/operator_console/source_browser/`: source index loading, normalization, filters, manual entries, overrides, tombstones, path aliases, column profiles, Qt table/detail widgets, context-file helpers, and validation.
- `data/operator-console/source-browser/`: committed scaffolds for manual entries, manual overrides, tombstones, saved filters, path aliases, and column profiles.
- `.cache/operator-console/`: ignored runtime cache for the local source index, thumbnails, and logs.

## Data Model

The index is assembled from committed YAML/JSON/JSONL metadata only. Records are normalized into source-browser entries with:

- `entry_id`, `entry_type`, `category`, `title`, and `summary`
- stage and record identifiers when present
- local paths, image paths, document paths, URLs, hashes, number facts, links, and warnings
- guardrail booleans such as `solve_claim`, `execution_allowed`, and `source_lock_only`

Manual entries and overrides are optional local review aids. They are schema-validated and reject large raw blobs. They must not embed raw source bodies, raw Discord logs, image bytes, workbook dumps, or generated output bodies.

## GUI Boundary

`libreprimus operator-console run` imports PySide6 only at runtime. If GUI dependencies are absent, the command exits cleanly with the installation hint instead of failing validation imports. CI does not require PySide6.

GUI file and URL actions are explicit operator actions. The browser must not automatically follow URLs, execute local files, modify raw third-party files, or turn a reviewed observation into an execution seed.

## Validation

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console validate-source-index
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console validate-manual-entries
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console summary
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-index
```

Stage 5DQ also validates through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dq
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dq-summary
```
