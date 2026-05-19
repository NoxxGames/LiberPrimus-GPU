# Static Review Site Upload

Stage 4A and its follow-up produce an SFTP-ready site at:

```text
experiments/results/discord-full-review/stage4a/site/
```

## Upload

Upload the contents of `site/`, not the parent `stage4a/` directory.

Do not upload:

- `third_party/LiberPrimusDiscordChats/`
- `third_party/LiberPrimusPages/`
- raw Discord HTML exports
- raw LP page image directories
- generated parent JSONL/Markdown bundle files unless explicitly intended
- repository root reports or local Deep Research reports

## Required Privacy Files

Confirm the upload includes:

- `index.html`
- `robots.txt`
- `SITE_PRIVACY_NOTICE.md`
- `SFTP_UPLOAD_CHECKLIST.md`
- `site_manifest.json`
- `site_manifest.md`
- `.htaccess.example`

`index.html` and generated subpages should contain `noindex,nofollow,noarchive` metadata.

## After Upload

Test:

- the root `index.html`;
- one channel part;
- one topic page;
- one index page;
- the LP page gallery;
- the site privacy notice and upload checklist.

For externally reachable hosts, consider server-level `X-Robots-Tag: noindex, nofollow, noarchive`,
basic authentication, or another access-control layer.
