# Discord Full Review Bundle

Stage 4A builds a privacy-preserving full-channel review bundle from local Discord HTML exports.
It is a generated research handoff layer, not a public raw-log dump and not experiment evidence.

## Inputs

- `third_party/LiberPrimusDiscordChats/`: ignored local Discord HTML exports.
- `third_party/LiberPrimusPages/`: ignored local Liber Primus page images for gallery generation.

Both input directories remain local and uncommitted. Stage 4A reads them only to create redacted,
generated review material under ignored output paths.

## Generated Outputs

The Stage 4A bundle is written under:

```text
experiments/results/discord-full-review/stage4a/
```

The generated `site/` subdirectory is SFTP-ready and contains `index.html`, channel pages, topic
pages, index pages, CSS, and an LP page gallery. Generated JSONL, Markdown shards, copied page
images, thumbnails, contact sheets, and zip archives are ignored and must not be committed.

Stage 4A follow-up adds generated site privacy files inside `site/`: `robots.txt`,
`SITE_PRIVACY_NOTICE.md`, `SFTP_UPLOAD_CHECKLIST.md`, `.htaccess.example`, `site_manifest.json`,
and `site_manifest.md`. Every generated HTML page includes noindex metadata by default.

## Privacy Boundary

Default mode is `redacted_public`. Usernames, user IDs, message IDs, avatar URLs, and private
Discord-hosted URLs are removed or redacted. Public external links and research-relevant text are
preserved where safe.

The bundle preserves chronology through redacted streams and channel shards. Topic pages and indexes
are secondary views and do not delete messages from the chronological layer.

## Use

Use this bundle when preparing Deep Research context or a private static review site. Do not hand
off raw Discord exports, private attachments, copied LP page images outside the generated site, or
large unredacted generated dumps.

If an older copy of the generated site has already been uploaded, rebuild Stage 4A and reupload the
contents of `experiments/results/discord-full-review/stage4a/site/` to apply noindex, robots, and
privacy notice updates.
