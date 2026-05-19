# Stage 4A Follow-Up Static Site Privacy And Wiki Development Log

## Initial State

- Starting commit: `1bd7ad73c2cfa6467e11f6c1a2f7cc6e812c4625`.
- Branch: `main`.
- Local `HEAD` equalled `origin/main`.
- Latest known CI after Stage 4A: run `26069247521`, passed.
- Generated Stage 4A site was present under `experiments/results/discord-full-review/stage4a/site/`.
- GitHub Wiki was enabled but the Wiki git remote returned `Repository not found`.

## Changes

Updated the Stage 4A static-site generator to emit:

- `robots.txt`
- `SITE_PRIVACY_NOTICE.md`
- `SFTP_UPLOAD_CHECKLIST.md`
- `.htaccess.example`
- `site_manifest.json`
- `site_manifest.md`

Added noindex metadata to generated HTML pages and strengthened validation to require privacy files,
site manifests, noindex metadata, and consistent manifest counts.

Added CLI options:

- `--emit-noindex`
- `--emit-robots`
- `--emit-site-manifest`

Updated docs, tutorials, wiki-source, and Wiki publish reporting.

## Local Rebuild

Reran:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review build `
  --discord-dir third_party/LiberPrimusDiscordChats `
  --lp-pages-dir third_party/LiberPrimusPages `
  --out-dir experiments/results/discord-full-review/stage4a `
  --privacy-mode redacted_public `
  --include-lp-page-gallery `
  --emit-noindex `
  --emit-robots `
  --allow-warnings
```

Build counts remained:

- Discord HTML files: `43`
- Total bytes: `465853032`
- Channels: `43`
- Channel shards: `1327`
- Topic shards: `12`
- LP page images: `58`

Generated outputs remain ignored.

## Wiki Diagnosis

Reran:

```powershell
gh repo view NoxxGames/LiberPrimus-GPU --json hasWikiEnabled,isPrivate,url
git ls-remote https://github.com/NoxxGames/LiberPrimus-GPU.wiki.git
.\scripts\github\sync-tutorials-to-wiki.ps1 --Publish --Repo NoxxGames/LiberPrimus-GPU
```

Result:

- Wiki enabled: true.
- Remote accessible: false.
- Publish attempted: true.
- Publish succeeded: false.
- Failure: `remote: Repository not found.` and `Wiki remote is not accessible: https://github.com/NoxxGames/LiberPrimus-GPU.wiki.git`.

## Validation

- Focused follow-up tests: passed.
- Focused ruff: passed.
- Stage 4A build validation: passed.
- Wiki source validation and dry-run sync: passed.

No raw Discord logs, raw LP page images, generated site files, channel shards, topic shards, copied
images, thumbnails, archives, SQLite outputs, CUDA changes, canonical corpus activation,
page-boundary finalization, or solve claims were committed.
