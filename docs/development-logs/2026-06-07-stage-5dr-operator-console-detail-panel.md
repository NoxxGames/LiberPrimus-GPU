# Stage 5DR - Operator Console Detail Panel

Stage 5DR refines the local Operator Console Source Browser GUI without puzzle execution.

Implemented changes:

- moved the details panel into a resizable right-side pane next to the source table;
- added `View -> Show Details Panel`, a toolbar `Toggle Details` action, and a detail-panel hide button;
- replaced the YAML-only detail panel with read-only tabs for overview, media/files, number facts, warnings/links, and raw record preview;
- added image thumbnails that open the existing image viewer on explicit click;
- added file, file-location, URL, path-copy, URL-copy, and hash-copy controls;
- added a table row context menu for details, image viewer, first file/location, first URL, and copy actions;
- changed blank status display to `unspecified` with a tooltip/legend explaining that no source-status field was present.

Follow-up usability repair:

- resolved archive-relative image paths such as `2014/additional images/...` against local ignored Cicada archive roots before showing the image viewer;
- made table clicks select the full row, so clicking any field updates the detail panel;
- kept the category list, table, and detail pane in a horizontal splitter with real resize behavior;
- wrapped detail-panel text and media/file rows to avoid horizontal scrolling for details;
- changed white panel borders and tab backgrounds to mid-grey/dark styling and added lower-contrast dark scroll bars.

Preserved boundaries:

- no route extraction, OCR, image forensics, AI interpretation, scoring, DWH/hash search, byte-stream generation, CUDA, website expansion, target selection, active ingestion, or solve claim;
- no committed source-lock record semantics were rewritten;
- manual entry, override, and tombstone semantics remain unchanged;
- `codex-output/stage5dr-codex-completion.md` is the ignored handoff summary path, and `codex_output` remains unused.

Validation added:

- `token-block build-stage5dr`
- `token-block validate-stage5dr`
- `token-block stage5dr-summary`
- focused Stage 5DR detail-panel, context-menu, status-display, thumbnail-action, URL/file-action, and preservation validators
- Qt-offscreen tests for detail-panel rendering and table interactions
