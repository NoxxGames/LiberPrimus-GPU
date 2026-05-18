# Generated Output Policy

## Purpose

Explain where generated outputs go and why they stay uncommitted.

## Common Generated Paths

- `experiments/results/bounded-auto-runs/`
- `experiments/results/discord-ingestion/`
- `experiments/results/discord-promotion/`
- `experiments/results/image-analysis/`
- `experiments/results/wiki-sync/`
- `data/normalized/`

## Commands

```powershell
git status --short
git check-ignore -v experiments/results/discord-promotion/stage3o/promotion_candidates.jsonl
```

## Expected Outputs

Generated outputs should be ignored or untracked but never staged.

## What Not To Commit

Candidate records, local review indexes, raw extraction JSONL, database files, and bulk generated
tables.

## Troubleshooting

If generated output needs a public summary, create a short research-log entry rather than
committing the full dump.
