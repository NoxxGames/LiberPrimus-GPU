# Troubleshooting

## Purpose

Fix common local setup, data, and validation issues.

## Common Checks

```powershell
git status --short
git remote -v
.\.venv\Scripts\python.exe -m libreprimus.cli smoke
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

## Missing Raw Data

Many CLIs support `--allow-missing` for raw-data-free validation. Missing raw data should not block
CI unless a stage explicitly requires local review.

## Generated Output Appears In Git Status

Check ignore rules:

```powershell
git check-ignore -v experiments/results/discord-promotion/stage3o/promotion_candidates.jsonl
git check-ignore -v experiments/results/image-transforms/stage3p/review_index.html
git check-ignore -v experiments/results/image-transforms/stage3p/contact_sheets/example.jpg
```

If an ignored Stage 3P transform run leaves local images or HTML under `experiments/results/`, do
not stage them. Re-run the transform command only after confirming raw page images remain ignored.

## Image Transform Run Is Slow

Stage 3P uses bounded review previews for large images. Do not switch to full-resolution derived
image generation unless a future stage explicitly budgets and scopes that output. Original image
hashes remain anchored by the Stage 3K lock records.

## Wiki Publish Fails

Validate local Wiki source first:

```powershell
.\scripts\github\validate-wiki-source.ps1
```

If the Wiki remote is unavailable, record the failure in `docs/github/wiki-publish-report.md`.

## Solve Claims

Do not treat terminal output, Discord claims, local review indexes, or generated candidates as solve
evidence. A solve requires a reproducible manifest, pinned corpus, matching output, tests, and
review.
