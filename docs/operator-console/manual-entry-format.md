# Source Browser Manual Entry Format

Manual Source Browser entries are local review notes that can supplement committed source-lock metadata. They are not source truth, not activation records, and not experiment seeds.

Manual entries live under:

```text
data/operator-console/source-browser/manual-entries/
```

Each entry is a small YAML mapping with this shape:

```yaml
record_type: source_browser_manual_entry
schema: schemas/operator-console/source-browser-manual-entry-v0.schema.json
entry_id: manual_example
created_at: "2026-06-07T00:00:00Z"
modified_at: "2026-06-07T00:00:00Z"
created_by: operator
category: Manual entries
title: Example local review note
summary: Short review note only.
entry_type: manual_note
status: review_note
trust_tier: operator_local
confidence: not_applicable
local_paths: []
image_paths: []
document_paths: []
urls: []
number_facts: []
candidate_family_links: []
warnings: []
notes: ""
solve_claim: false
execution_allowed: false
```

## Rules

- Keep entries compact and review-oriented.
- Do not paste raw source bodies, raw Discord logs, generated result records, workbook dumps, image/audio bytes, archives, or private identifiers.
- `solve_claim` must be `false`.
- `execution_allowed` must be `false`.
- Use links and file references instead of copying source content.
- If a path points into ignored third-party material, expect the source index to report that path as missing on machines that do not have the local file.

Manual overrides and tombstones have separate schemas. They target existing `entry_id` values and must not erase the underlying committed record.
