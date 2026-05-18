> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Local Data Policy

## Purpose

Explain how local raw material is handled safely.

## Policy

Raw material stays local and ignored. This includes Discord HTML exports, Liber Primus page images,
legacy workbooks, Pastebin drops, transcripts, generated candidates, SQLite databases, and local
review indexes.

## Commands

```powershell
git check-ignore -v third_party/LiberPrimusDiscordChats/
git check-ignore -v third_party/LiberPrimusPages/example.jpg
git check-ignore -v experiments/results/discord-ingestion/stage3n/discord_extracted_links.jsonl
```

## Expected Outputs

Each command should show the matching `.gitignore` rule.

## What Not To Commit

Do not commit raw Discord HTML, message bodies, usernames, private attachment URLs, raw page images,
generated JSONL, or SQLite databases.

## Troubleshooting

If a raw file appears in `git status --short`, stop before staging and check `.gitignore`.
