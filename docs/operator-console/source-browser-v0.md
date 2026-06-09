# Operator Console Source Browser v0

Stage 5DQ adds the Liber Primus Operator Console v0 Source Browser as local review infrastructure. The browser indexes committed metadata records, shows source-lock and candidate context, and provides explicit navigation to local paths, image paths, document paths, URLs, and the local `ChatGPT-ContextFile.md` when those references are present.

The Source Browser is not a puzzle runner. It does not run route extraction, OCR, image forensics, AI interpretation, scoring, DWH/hash search, byte-stream generation, CUDA, or source files. Missing local paths are review warnings because many referenced third-party files are intentionally ignored and not present on every checkout.

Stage 5DR refines the Source Browser GUI. The detail panel can be hidden or shown from `View -> Show Details Panel` or `Toggle Details`, and renders structured read-only tabs for overview, media/files, number facts, warnings/links, and the raw record preview. A follow-up usability fix moves that detail panel to the right side of the table, keeps the category list/table/details panes resizable, makes row clicks select the full row, wraps detail-panel text without horizontal scrolling, and applies explicit dark tab/scrollbar styling.

Stage 5DS adds loadability coverage for the expanded Music / Ouroboros / token-block static source-lock addendum. The browser loads the new compact metadata as review-only Music, source-lock, candidate, warning, and number-fact entries; it still does not execute audio, open raw files automatically, infer image/text content, or promote candidates to experiment seeds.

Stage 5DT adds number-fact card reviewability. Existing number facts are normalized into read-only cards with explicit source path, value, operation/expression when available, verification state, review state, enrichment flags, and source-lock warnings. Value-only facts are displayed as enrichment-needed instead of silently looking complete; entries with zero extracted facts are displayed as not reviewed unless a future overlay explicitly records a reviewed-none-found state.

Stage 5DU adds community visual/red-heading/negative-space source-lock metadata and a review-only overlay collection for selected number facts. The overlays make candidate facts easier to inspect in the details panel, but they do not rewrite historical source-lock records, validate visual intent, select a target, or authorize route execution.

Stage 5DV repairs Source Browser responsiveness and path hygiene before the first number-fact review batch. Table cells use compact text/count display, path resolution is cached, raw previews and thumbnails are lazy/cached in the details panel, and search text is precomputed. Path collection is key-aware and source-root-aware: bare filenames such as `0.png`, `messages.txt`, or `google_doc_1.png` are labels unless a path-bearing key or explicit `source_root` resolves them. If `relative_path` and `file_name` are both present, the explicit relative path wins. Missing root-level basename duplicates are suppressed when a rooted canonical path is present.

Stage 5DW implements the first high-signal source-lock number-fact review batch. It adds 37 review-only NumberFactCard overlays for 20 selected source-lock/candidate records and supports overlay-only fact cards, so entries with zero extracted number facts can display reviewed facts without mutating their historical source-lock records.

Blank table status values are displayed as `unspecified`. This means the source record did not contain `source_status`, `status`, `ready_state`, or `review_state`; it does not mean the record is incomplete, and the GUI does not rewrite source-lock records to invent statuses.

## Components

- `python/libreprimus/operator_console/`: shared console settings, optional GUI entrypoint, styles, resources, and CLI registration.
- `python/libreprimus/operator_console/source_browser/`: source index loading, normalization, filters, manual entries, overrides, tombstones, path aliases, column profiles, Qt table/detail widgets, context-file helpers, and validation.
- `data/operator-console/source-browser/`: committed scaffolds for manual entries, manual overrides, tombstones, saved filters, path aliases, column profiles, number-fact card config, review states, enrichment overlays, and review batches.
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

Stage 5DT number-fact cards are display and review scaffolding only. Overlay files may enrich review state later, but they must not rewrite the original source-lock records. The filters `needs:fact-enrichment`, `not-reviewed:number-facts`, `rich:number-facts`, `canonical-verification:number-facts`, and `quarantined:number-facts` help operators find review work without executing any route.

Stage 5DU overlays are review-only enrichments for community visual-route candidate facts. They must stay `usable_for_decision_now=false`, cannot be used as route seeds or proof, and must not be treated as image-forensic or OCR evidence.

Stage 5DV path policy records live in `data/operator-console/source-browser/path-canonicalization-policy.yaml`, `performance-policy.yaml`, and `cache-policy.yaml`. The canonical LP page image root remains `third_party/CiadaSolversIddqd_v2/liber-primus__images--full`; this spelling matches the current local source root and must not be silently changed.

Stage 5DW overlays live in `data/operator-console/source-browser/number-fact-overlays/stage5dw-review-batch-001-high-signal-overlays.yaml`. Overlay-only cards are review aids loaded from committed overlay metadata; they must stay `usable_for_decision_now=false` and must not become target-priority evidence, route seeds, source-lock rewrites, byte streams, execution input, or solve claims.

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

Stage 5DT validates number-fact card reviewability through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5dt
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dt
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dt-summary
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console validate-number-fact-cards
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console number-fact-reviewability-summary
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-number-facts
```

Stage 5DU validates community visual source-lock loadability through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5du
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5du
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5du-source-browser-loadability
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5du-number-fact-cards
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5du-summary
```

Stage 5DV validates Source Browser repair through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5dv
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dv
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dv-path-canonicalization
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dv-source-browser-performance
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dv-source-browser-loadability
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-paths
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser performance-smoke
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dv-summary
```

Stage 5DW validates number-fact review batch 001 through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5dw
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dw
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5dw-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dw-review-batch-selection
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dw-number-fact-overlays
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dw-overlay-only-fact-cards
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dw-source-browser-loadability
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console validate-source-index
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-index
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-paths
```
