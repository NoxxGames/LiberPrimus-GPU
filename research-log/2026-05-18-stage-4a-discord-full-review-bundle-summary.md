# Stage 4A Discord Full Review Bundle Summary

## Scope

Stage 4A built a privacy-preserving full Discord review bundle for Deep Research from local ignored
Discord HTML exports and local ignored Liber Primus page images.

This was not a Discord scrape, live API task, AI summarisation task, OCR task, image-derived cipher
execution, CUDA task, canonical-corpus activation, page-boundary finalization, or solve claim.

## Generated Output

- Bundle root: `experiments/results/discord-full-review/stage4a/`
- Static site: `experiments/results/discord-full-review/stage4a/site/index.html`
- SFTP root: `experiments/results/discord-full-review/stage4a/site/`
- Deep Research manifest: `experiments/results/discord-full-review/stage4a/deep_research_bundle_manifest.yaml`
- Optional upload archive: `experiments/results/discord-full-review/stage4a/liberprimus-discord-review-site.zip`

All generated bundle outputs remain ignored and uncommitted.

## Local Build Counts

- Discord HTML files processed: `43`
- Total bytes processed: `465853032`
- Channels: `43`
- Largest channel part count: `573`
- Redacted messages: `520009`
- Channel shards: `1327`
- Topic shards: `12`
- Public links: `57969`
- Image references: `51025`
- Attachment references: `11383`
- Method claims: `41059`
- Numeric claims: `520009`
- Visual claims: `33209`
- Debunk records: `4010`
- LP page images included in generated gallery: `58`
- LP page thumbnails generated: `58`

## Committed Aggregate Records

- `data/observations/discord/stage4a-full-review-aggregate.yaml`
- `data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml`

The aggregate records contain counts, generated paths, source directory references, and privacy
flags only. They do not contain raw messages, usernames, user IDs, message IDs, private URLs, raw
Discord HTML, copied LP page images, thumbnails, or generated site content.

## Validation

- `libreprimus discord-full-review validate`: passed.
- `libreprimus research-synthesis validate`: passed.
- `libreprimus consistency check-state-drift`: passed.
- `libreprimus consistency check-all --allow-warnings`: passed with `505` checks.
- `pytest -q tests/python`: `901` passed.
- `ruff check python/libreprimus tests/python`: passed.
- `scripts/ci/run-consistency-checks.ps1`: passed, including a raw-data-free synthetic Stage 4A build.

## Privacy And Safety

- Raw Discord HTML committed: `false`.
- Raw message bodies committed: `false`.
- Usernames committed: `false`.
- User IDs committed: `false`.
- Message IDs committed: `false`.
- Private Discord URLs committed: `false`.
- Raw LP page images committed: `false`.
- Generated static site committed: `false`.
- Solve claim: `false`.
