# Stage 4A Follow-Up Static Site Privacy And Wiki Summary

## Scope

This follow-up hardened the generated Stage 4A static review site for cautious SFTP hosting and
rechecked GitHub Wiki publishing.

It did not execute cryptanalytic experiments, promote Discord leads, ingest Deep Research results,
process new raw data, use CUDA, activate the canonical corpus, finalize page boundaries, or claim a
solve.

## Static Site Privacy

The Stage 4A generator now emits these generated site files by default:

- `site/robots.txt`
- `site/SITE_PRIVACY_NOTICE.md`
- `site/SFTP_UPLOAD_CHECKLIST.md`
- `site/.htaccess.example`
- `site/site_manifest.json`
- `site/site_manifest.md`

Every generated HTML page includes:

```html
<meta name="robots" content="noindex,nofollow,noarchive">
```

The rebuilt generated site remains ignored under:

```text
experiments/results/discord-full-review/stage4a/site/
```

## Local Rebuild

- Build rerun: true.
- Privacy mode: `redacted_public`.
- Discord HTML files processed: `43`.
- Total bytes processed: `465853032`.
- Channels: `43`.
- Channel shards: `1327`.
- Topic shards: `12`.
- Public links: `57969`.
- Image references: `51025`.
- Attachment references: `11383`.
- LP page images in generated gallery: `58`.
- Noindex metadata verified: true.
- `robots.txt` generated: true.
- Site manifest generated: true.
- SFTP checklist generated: true.

The user should reupload the contents of `experiments/results/discord-full-review/stage4a/site/`
to apply the noindex/privacy changes to the hosted copy.

## Wiki Diagnosis

- Wiki enabled: true.
- Wiki remote accessible: false.
- Publish attempted: true.
- Publish succeeded: false.
- Failure reason: `remote: Repository not found.` and `Wiki remote is not accessible: https://github.com/NoxxGames/LiberPrimus-GPU.wiki.git`.
- Likely manual fix: create an initial Wiki page in the GitHub UI, then rerun `scripts/github/sync-tutorials-to-wiki.ps1 --Publish --Repo NoxxGames/LiberPrimus-GPU`.

The repository tutorials and `docs/wiki-source/` mirror remain valid.

## Validation

- `libreprimus discord-full-review validate`: passed.
- Focused Stage 4A follow-up tests: passed.
- Wiki source validation and dry-run sync: passed.

Full validation results are recorded in the development log and final report.
