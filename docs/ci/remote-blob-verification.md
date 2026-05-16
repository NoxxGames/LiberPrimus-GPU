# Remote Blob Verification

Stage 2C-followup-5 added remote blob verification for files where line-oriented
format matters, especially `.github/workflows/ci.yml` and `.gitattributes`.

## Trust Order

Use this order when remote views disagree:

1. `git fetch` plus `git show origin/main:<path>` is the authoritative remote
   Git blob check.
2. GitHub API contents are a useful independent check of the same blob.
3. `raw.githubusercontent.com` is useful for public diagnostics, but may be
   cached or stale.

If the Git blob and GitHub API agree, a raw URL mismatch should be treated as a
warning and investigated, not as proof that the repository blob is malformed.

## Local Commands

PowerShell:

```powershell
.\scripts\ci\verify-remote-git-blobs.ps1 -Remote origin -Branch main -CheckRawUrl -CheckGitHubApi
```

Shell:

```sh
scripts/ci/verify-remote-git-blobs.sh --remote origin --branch main --check-raw-url --check-github-api
```

The scripts do not require `gh`. They fail if the fetched remote Git blobs are
flattened, minified, missing required CI commands, or missing required Git
attribute rules. Raw URL and API line count differences are reported separately.

## Expected Checks

- Workflow blob has more than 25 lines.
- `.gitattributes` blob has more than 10 lines.
- Workflow first line does not contain `name: CI on:`.
- `.gitattributes` first line does not contain the entire attributes file.
- Workflow includes Ruff, pytest, smoke, registry validation, solved-baseline
  manifest validation, and result-store manifest validation.
- `.gitattributes` includes LF rules for JSON, YAML, shell scripts, and SHA lock
  files.
