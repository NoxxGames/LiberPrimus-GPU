# Public Docs Status Checks

## Purpose

Stage 2C-followup-4 adds raw-data-free tests that keep public status text aligned with the actual project state.

## Checked Files

- `README.md`
- `STATUS.md`
- `ROADMAP.md`

## Policy

The public README must put the current project state near the top of the file. Historical stage sections may remain, but stale top-level current-status or next-milestone text must be removed when a stage completes.

README, STATUS, and ROADMAP must remain readable multi-line Markdown. They must not be collapsed into single-line blobs.

## Local Check

```powershell
.\scripts\ci\verify-public-docs-status.ps1
```

Linux:

```bash
bash scripts/ci/verify-public-docs-status.sh
```

The check is also covered by the normal Python test suite.
