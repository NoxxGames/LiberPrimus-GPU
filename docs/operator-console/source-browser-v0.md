# Operator Console Source Browser v0

Stage 5DQ adds the Liber Primus Operator Console v0 Source Browser as local review infrastructure. The browser indexes committed metadata records, shows source-lock and candidate context, and provides explicit navigation to local paths, image paths, document paths, URLs, and the local `ChatGPT-ContextFile.md` when those references are present.

The Source Browser is not a puzzle runner. It does not run route extraction, OCR, image forensics, AI interpretation, scoring, DWH/hash search, byte-stream generation, CUDA, or source files. Missing local paths are review warnings because many referenced third-party files are intentionally ignored and not present on every checkout.

Stage 5DR refines the Source Browser GUI. The detail panel can be hidden or shown from `View -> Show Details Panel` or `Toggle Details`, and renders structured read-only tabs for overview, media/files, number facts, warnings/links, and the raw record preview. A follow-up usability fix moves that detail panel to the right side of the table, keeps the category list/table/details panes resizable, makes row clicks select the full row, wraps detail-panel text without horizontal scrolling, and applies explicit dark tab/scrollbar styling.

Stage 5DS adds loadability coverage for the expanded Music / Ouroboros / token-block static source-lock addendum. The browser loads the new compact metadata as review-only Music, source-lock, candidate, warning, and number-fact entries; it still does not execute audio, open raw files automatically, infer image/text content, or promote candidates to experiment seeds.

Blank table status values are displayed as `unspecified`. This means the source record did not contain `source_status`, `status`, `ready_state`, or `review_state`; it does not mean the record is incomplete, and the GUI does not rewrite source-lock records to invent statuses.

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

Stage 5DR adds right-click row actions and detail-panel actions for opening image viewers, files, file locations, and URLs. These are still explicit operator actions only. Image thumbnails are display/navigation aids only and do not perform OCR, image forensics, AI interpretation, stego detection, or content analysis. Archive-relative image paths such as `2014/additional images/...` are resolved against local ignored Cicada archive roots when those files are present; the GUI still does not commit or mutate those raw files.

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

Stage 5DR validates through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5dr
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dr-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr-detail-panel
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr-table-context-menu
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr-status-display
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr-image-thumbnail-actions
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr-url-file-actions
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dr-preservation
```

Stage 5DS validates source-browser loadability through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ds
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ds
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ds-source-browser-loadability
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5ds-summary
```
