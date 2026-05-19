# Discord Full Review CLI

The Stage 4A commands are exposed through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review --help
```

## Build

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review build `
  --discord-dir third_party/LiberPrimusDiscordChats `
  --lp-pages-dir third_party/LiberPrimusPages `
  --out-dir experiments/results/discord-full-review/stage4a `
  --privacy-mode redacted_public `
  --include-lp-page-gallery `
  --emit-noindex `
  --emit-robots `
  --emit-site-manifest `
  --allow-warnings
```

`build` reads ignored local inputs and writes ignored generated outputs. It does not call Discord,
scrape the web, run OCR, or execute experiments.

Privacy hardening is enabled by default. The build writes `robots.txt`, noindex metadata on HTML
pages, `SITE_PRIVACY_NOTICE.md`, `SFTP_UPLOAD_CHECKLIST.md`, `.htaccess.example`, and site manifest
files under the generated `site/` directory.

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review validate `
  --results-dir experiments/results/discord-full-review/stage4a
```

Validation checks that required bundle files exist, privacy files exist, noindex metadata is present
on generated HTML pages, site manifest counts match the summary, and generated text does not contain
obvious raw usernames, user IDs, message IDs, or private Discord-hosted URLs.

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review summary `
  --results-dir experiments/results/discord-full-review/stage4a
```

The summary command prints aggregate counts only. It does not print raw messages.

## Output Policy

All generated Stage 4A outputs remain under `experiments/results/discord-full-review/stage4a/` and
must remain ignored. Commit only code, schemas, aggregate summaries, documentation, tests, and
summary research logs.
