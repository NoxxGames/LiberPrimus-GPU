# Stage 3Q Discord Review Bundles

Stage 3Q adds privacy-preserving Discord review-bundle generation.

The goal is to make the admin-provided local Discord HTML archive usable for focused review without committing or uploading raw logs.

## Added Capabilities

- Redacted message stream generation from Stage 3N/3O records.
- Topic classifier for source links, cuneiform/base-60, page-art dots, number squares, cookies/hashes, number theory, Vigenere/literature, Gematria/rune counts, visual clues, OutGuess/audio, solved-history notes, debunks, tools, and open leads.
- Review lead builder with redacted summaries and suggested next actions.
- Markdown topic shards under ignored output paths.
- Local HTML review index.
- Aggregate-only committed YAML summary.

## Boundaries

Stage 3Q does not:

- publish raw Discord logs
- commit message bodies or usernames
- call Discord APIs
- scrape Discord
- run AI/ML
- execute extracted methods
- use CUDA
- claim a solve

## Local Output

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review build-bundles `
  --ingestion-dir experiments/results/discord-ingestion/stage3n `
  --promotion-dir experiments/results/discord-promotion/stage3o `
  --raw-dir third_party/LiberPrimusDiscordChats `
  --out-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate-out data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing `
  --allow-warnings
```

Generated shards and indexes remain ignored. The committed aggregate is safe high-level metadata only.
