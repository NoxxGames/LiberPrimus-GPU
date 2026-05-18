# GitHub Wiki Mirror

The GitHub Wiki is a mirror of repository tutorials. The repository files under `tutorials/` are the source of truth.

Stage 3O generates wiki source pages under `docs/wiki-source/`:

- `Home.md`
- `_Sidebar.md`
- one page per tutorial Markdown file

Use the validation script before publishing:

```powershell
.\scripts\github\validate-wiki-source.ps1
```

Generate and validate the mirror without touching the Wiki remote:

```powershell
.\scripts\github\sync-tutorials-to-wiki.ps1 --DryRun
```

Publish, when the Wiki remote is available:

```powershell
.\scripts\github\sync-tutorials-to-wiki.ps1 --Publish --Repo NoxxGames/LiberPrimus-GPU
```

The temporary `.wiki-worktree/` directory is ignored and must not be committed. Wiki pages must not contain raw Discord logs, raw corpus dumps, generated result dumps, or solve claims.
