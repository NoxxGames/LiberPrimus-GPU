# Discord Full Review Site Privacy

Stage 4A follow-up hardens the generated static review site for cautious SFTP hosting.

The site remains generated output under:

```text
experiments/results/discord-full-review/stage4a/site/
```

It must not be committed. Rebuild and reupload the generated `site/` directory to apply privacy
changes.

## Generated Privacy Files

The generator emits:

- `robots.txt`: disallows all crawlers.
- `SITE_PRIVACY_NOTICE.md`: explains the redacted review-site boundary.
- `SFTP_UPLOAD_CHECKLIST.md`: lists what to upload and what not to upload.
- `.htaccess.example`: optional Apache noindex/basic-auth guidance.
- `site_manifest.json`: deterministic site counts and important paths.
- `site_manifest.md`: human-readable site manifest.

Every generated HTML page includes:

```html
<meta name="robots" content="noindex,nofollow,noarchive">
```

## Hosting Guidance

Use `redacted_public` output only. Upload only the generated `site/` contents, never
`third_party/`, raw Discord HTML, raw LP page images, or generated parent JSONL/Markdown bundles.

For public or semi-public hosting, consider noindex headers, unlisted URLs, or basic
authentication. The site is a review aid, not source truth or solve evidence.
