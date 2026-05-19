# Local Data Policy

## Purpose

Explain how local raw material is handled safely.

## Policy

Raw material stays local and ignored. This includes Discord HTML exports, Liber Primus page images,
legacy workbooks, Pastebin drops, transcripts, generated candidates, SQLite databases, and local
review indexes. Stage 4E also uses `third_party/CicadaSolversIddqd/` as an ignored local cache for
public `cicada-solvers/iddqd` source-delta work; only its README and `.gitkeep` are intended for Git.

The current private/generated path map is `docs/onboarding/private-generated-data-map.md`.

## Commands

```powershell
git check-ignore -v third_party/LiberPrimusDiscordChats/
git check-ignore -v third_party/LiberPrimusPages/example.jpg
git check-ignore -v third_party/CicadaSolversIddqd/example.jpg
git check-ignore -v experiments/results/discord-ingestion/stage3n/discord_extracted_links.jsonl
git check-ignore -v experiments/results/source-delta/stage4e/source_delta_report.json
```

## Expected Outputs

Each command should show the matching `.gitignore` rule.

## What Not To Commit

Do not commit raw Discord HTML, message bodies, usernames, private attachment URLs, raw page images,
generated JSONL, or SQLite databases. Do not commit downloaded `cicada-solvers/iddqd` images, audio,
fonts, archives, blobs, or cloned repository contents.

## Troubleshooting

If a raw file appears in `git status --short`, stop before staging and check `.gitignore`.
