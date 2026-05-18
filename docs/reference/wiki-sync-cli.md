# Wiki Sync CLI

Stage 3O adds local scripts for generating and publishing the GitHub Wiki mirror.

Validate committed wiki source:

```powershell
.\scripts\github\validate-wiki-source.ps1
```

Regenerate `docs/wiki-source/` from `tutorials/` without publishing:

```powershell
.\scripts\github\sync-tutorials-to-wiki.ps1 --DryRun
```

Publish to the GitHub Wiki remote:

```powershell
.\scripts\github\sync-tutorials-to-wiki.ps1 --Publish --Repo NoxxGames/LiberPrimus-GPU
```

The shell equivalents are:

```bash
./scripts/github/validate-wiki-source.sh
./scripts/github/sync-tutorials-to-wiki.sh --dry-run
./scripts/github/sync-tutorials-to-wiki.sh --publish --repo NoxxGames/LiberPrimus-GPU
```

Publishing uses `.wiki-worktree/`, which is ignored. If the Wiki remote is unavailable, keep `docs/wiki-source/` committed and follow the manual steps in `docs/github/wiki-publish-report.md`.
