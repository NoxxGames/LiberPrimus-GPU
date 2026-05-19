# Stage 4A Follow-Up Static Site Privacy And Wiki

This follow-up hardens the generated Stage 4A static review site for cautious SFTP hosting and
rechecks GitHub Wiki publishing.

## Scope

The follow-up adds generated privacy files, noindex metadata, crawler disallow output, deterministic
site manifests, stronger validation, upload documentation, and Wiki publishing diagnosis. It does
not change research conclusions, promote Discord leads, process new data, execute experiments, use
CUDA, activate the canonical corpus, finalize page boundaries, or claim a solve.

## Generated Site Contract

The site generator now emits:

- `robots.txt`
- `SITE_PRIVACY_NOTICE.md`
- `SFTP_UPLOAD_CHECKLIST.md`
- `.htaccess.example`
- `site_manifest.json`
- `site_manifest.md`

The root index, channel pages, topic pages, index pages, and LP gallery include
`noindex,nofollow,noarchive` metadata by default.

## Wiki Diagnosis

The repository reports Wiki support as enabled, but the Wiki git remote still returns
`Repository not found`. The publish script was attempted and failed for that reason. The local
`docs/wiki-source/` mirror remains valid; manual Wiki initialization in the GitHub UI is still the
likely recovery path.
