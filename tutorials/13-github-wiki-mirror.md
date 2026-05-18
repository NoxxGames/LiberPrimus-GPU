# GitHub Wiki Mirror

## Purpose

Mirror repository tutorials into GitHub Wiki pages for public browsing.

## Source Of Truth

Repository files under `tutorials/` are source of truth. Wiki pages are generated mirrors.

## Commands

```powershell
.\scripts\github\validate-wiki-source.ps1
.\scripts\github\sync-tutorials-to-wiki.ps1 --DryRun
```

Publishing, when the Wiki remote is available:

```powershell
.\scripts\github\sync-tutorials-to-wiki.ps1 --Publish --Repo NoxxGames/LiberPrimus-GPU
```

## Expected Outputs

`docs/wiki-source/` contains `Home.md`, `_Sidebar.md`, and mirrored tutorial pages.

## What Not To Commit

Do not commit `.wiki-worktree/` or generated sync reports unless copied into a docs report.

## Troubleshooting

If the Wiki remote is not initialized or inaccessible, keep `docs/wiki-source/` and the publish
report current, then publish manually later.
