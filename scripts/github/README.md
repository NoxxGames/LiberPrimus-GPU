# GitHub Scripts

These PowerShell scripts support public project bootstrap.

- `verify-github-remote.ps1` checks `gh` auth, target repository reachability, and local `origin` compatibility.
- `create-labels.ps1` creates or updates labels from `docs/github/labels.json`.
- `create-issues.ps1` creates issues from `docs/github/issues/` without duplicating exact titles.
- `publish-wiki.ps1` publishes `docs/github/wiki-pages/` into the GitHub wiki.
- `validate-wiki-source.ps1` validates the Stage 3O tutorial-backed Wiki source under `docs/wiki-source/`.
- `sync-tutorials-to-wiki.ps1` regenerates `docs/wiki-source/` from `tutorials/` and can publish to the GitHub Wiki when the remote is available.

Scripts must not print secrets, change repository visibility, force-push, or stage raw/generated data in the main repository.
