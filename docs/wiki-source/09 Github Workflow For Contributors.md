> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# GitHub Workflow For Contributors

## Branch, Commit, Push

Work on a branch or `main` as appropriate for the repository policy. Commit only explicit files. Push after successful validation and commit when the remote is verified.

Never force-push without explicit instruction.

## Issues

Use GitHub issues for scoped work. A useful issue states context, scope, non-goals, deliverables, tests, and safety rules.

## Wiki

The GitHub wiki is a mirror for public convenience. Repository tutorials and docs are the source of truth.

Stage 3O generates Wiki source from `tutorials/`:

```powershell
.\scripts\github\validate-wiki-source.ps1
.\scripts\github\sync-tutorials-to-wiki.ps1 --DryRun
```

Do not edit only the GitHub Wiki. Update repository tutorials first, regenerate `docs/wiki-source/`, and then publish when the Wiki remote is available.

## Raw Data Ban

Do not attach or commit raw corpus files, generated alignment dumps, local workbooks, or local Pastebin text.

Stage 3K also keeps local page images under `third_party/LiberPrimusPages/` ignored. Commit only lock records, observation records, schemas, docs, tests, and source code.

Stage 3N keeps admin-provided Discord HTML logs under `third_party/LiberPrimusDiscordChats/` ignored. Commit only schemas, code, docs, tests, aggregate/redacted records, and research summaries.

Stage 3O keeps generated Discord promotion outputs under `experiments/results/discord-promotion/` ignored and commits only curated redacted promotion records.

## Pull Requests

Explain validation commands, note raw/generated exclusions, and link relevant docs or issues.

## GitHub Actions CI

Stage 2C adds `.github/workflows/ci.yml`. The workflow runs on pushes to `main` and pull requests targeting `main`.

The Python job installs Python 3.12, runs Ruff, runs pytest, and validates committed registry and manifest files. The CPU CMake smoke job builds without CUDA and without raw data.

Local reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
.\scripts\ci\run-consistency-checks.ps1
```

CI should not require raw data, secrets, CUDA, or generated result artifacts.

Stage 2D adds consistency checks for schemas, manifests, registry metadata, public docs, ignored outputs, and result-store metadata. Run them before opening a pull request that changes any of those areas.
