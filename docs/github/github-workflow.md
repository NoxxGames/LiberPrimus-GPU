# GitHub Workflow

## Target Repository

The intended GitHub repository for public project infrastructure is `NoxxGames/LiberPrimus-GPU`.

If `origin` uses an older GitHub URL that resolves to that repository, it may be treated as verified. Do not overwrite a remote that resolves somewhere else.

## Push Policy

After a successful commit, push to the verified remote unless the user explicitly says not to push. Never force-push without explicit instruction.

Do not push if validation failed, raw data is staged, generated outputs are staged, or the remote cannot be verified.

## Issues

Issue creation must be idempotent. Scripts check existing open and closed issues by exact title before creating new issues.

## Wiki

Wiki pages are mirrors of repository tutorials and docs. If wiki pages and repo docs diverge, repo docs win.

Do not use the wiki for raw corpus data, generated JSONL outputs, raw transcript dumps, page images, or solve claims.
