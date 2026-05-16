# GitHub Workflow For Contributors

## Branch, Commit, Push

Work on a branch or `main` as appropriate for the repository policy. Commit only explicit files. Push after successful validation and commit when the remote is verified.

Never force-push without explicit instruction.

## Issues

Use GitHub issues for scoped work. A useful issue states context, scope, non-goals, deliverables, tests, and safety rules.

## Wiki

The GitHub wiki is a mirror for public convenience. Repository tutorials and docs are the source of truth.

## Raw Data Ban

Do not attach or commit raw corpus files, generated alignment dumps, local workbooks, or local Pastebin text.

## Pull Requests

Explain validation commands, note raw/generated exclusions, and link relevant docs or issues.

## GitHub Actions CI

Stage 2C adds `.github/workflows/ci.yml`. The workflow runs on pushes to `main` and pull requests targeting `main`.

The Python job installs Python 3.12, runs Ruff, runs pytest, and validates committed registry and manifest files. The CPU CMake smoke job builds without CUDA and without raw data.

Local reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
```

CI should not require raw data, secrets, CUDA, or generated result artifacts.
