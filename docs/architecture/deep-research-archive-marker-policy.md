# Deep Research Archive Marker Policy

Stage 5BD adds a policy for future repository ZIPs used in Deep Research review. ZIPs should include marker files that identify the intended repository state even when `.git/` is omitted.

Recommended generated marker files:

- `ARCHIVE_COMMIT.txt`
- `ARCHIVE_MANIFEST.json`
- `ARCHIVE_MANIFEST.sha256`
- `ARCHIVE_README.md`

The marker must include commit hash, branch, stage ID, generated timestamp, expected next stage, and manifest hash. Generated ZIPs and marker outputs remain ignored under `deep-research-repo-zips/`; only the policy, scripts, and compact metadata are committed.
