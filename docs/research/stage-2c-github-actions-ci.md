# Stage 2C GitHub Actions CI

## Status

Complete. Stage 2C adds raw-data-free GitHub Actions CI and local reproduction scripts. Stage 2C-followup-2 adds raw remote workflow verification so the GitHub-served `main` workflow can be checked after push without relying on `gh`.

## Stage Goal

Add CI for Python tests, Ruff, schema/manifest validation, package smoke commands, and CPU-only CMake smoke checks without requiring raw data, CUDA, secrets, generated outputs, or solve claims.

## Inputs

- Stage 2A CPU transform registry.
- Stage 2A solved-baseline manifests.
- Stage 2B result-store manifest and schemas.
- Existing Python and CMake test scaffolds.

## Workflow Design

The workflow runs on pushes and pull requests targeting `main`. The Python job installs Python 3.12 and runs Ruff, pytest, CLI smoke, transform-registry validation, solved-baseline manifest validation, and result-store manifest validation.

The CMake job builds and tests the CPU scaffold with CUDA disabled.

Stage 2C-followup reformatted the workflow into readable multi-line YAML and added static parsing/formatting tests. The tests reject flattened workflow files and validate the parsed trigger/job structure.

Stage 2C-followup-2 confirmed the local and remote raw workflow were already multi-line at the start of the task and added reusable scripts to repeat that remote check after future pushes.

Stage 2C-followup-3 fixed the Linux CI lock mismatch by repairing `.gitattributes`, normalizing canonical profile/registry JSON locks to LF bytes, and adding lock-hash validation to CI.

## Local Scripts

Local reproduction scripts live under `scripts/ci/` for PowerShell and shell users. They split Python checks from schema/manifest validation so contributors can rerun targeted checks.

Stage 2C-followup adds `validate-workflow-static` scripts for PowerShell and shell users. Stage 2C-followup-2 adds `verify-remote-workflow` scripts that fetch the public raw workflow URL and do not require `gh`. Stage 2C-followup-3 adds canonical lock verification scripts.

## Validation Result

Local validation runs Ruff, pytest, Python smoke, registry validation, solved-baseline manifest validation, result-store manifest validation, the PowerShell CI scripts, shell syntax checks, and local CMake CPU smoke where the host toolchain supports it.

## What This Stage Proves

Stage 2C proves the repository has repeatable CI gates for raw-data-free Python validation, manifest/schema sanity, and CPU scaffold build coverage.

## What This Stage Does Not Prove

It does not run real-source smoke commands, unsolved-page experiments, search, scoring, CUDA kernels, GPU parity, or benchmark campaigns.

## Next Stage

Recommended next work: Stage 2D CI-gated schema/docs consistency checks and manifest/result-store validation hardening before bounded CPU exploratory experiment scaffolding.
