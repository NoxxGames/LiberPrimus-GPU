# Stage 2C-followup-5 Remote Blob Consistency

## Status

Remote repository verification and raw URL trust-boundary hardening.

## Goal

Determine whether externally observed flattened workflow and Git attributes
files reflect malformed remote Git blobs or stale raw URL views, and add
verification tooling that uses Git blobs as the primary source of truth.

## Result

The current `origin/main` Git blobs and GitHub API contents for
`.github/workflows/ci.yml` and `.gitattributes` are readable multi-line files.
The latest CI run before this stage was green. No CI workflow or Git attributes
content repair was necessary.

Stage 2C-followup-5 added remote Git blob verifier scripts for PowerShell and
shell users. The verifier fetches the remote, checks `git show` blobs first,
optionally reports GitHub API and raw URL line counts, and treats raw URL
mismatches as warnings when the fetched Git blob is valid.

Local validation passed with Ruff clean and `260` Python tests passing.

## Non-goals

No Stage 2D implementation, unsolved-page search, scoring, CUDA implementation,
canonical corpus activation, or page-boundary finalization was added.
