# GitHub Actions CI

## Purpose

Stage 2C adds repository CI for fast, raw-data-free validation before any broader experiment scaffolding.

## Workflow File

The workflow lives at `.github/workflows/ci.yml` and runs on pushes to `main` and pull requests targeting `main`.

Stage 2C-followup keeps this file as readable multi-line YAML. Static tests reject flattened or minified workflow formatting so review diffs remain useful.

Stage 2C-followup-2 adds a raw GitHub URL verifier so maintainers can confirm the pushed workflow is also readable multi-line YAML after GitHub serves it from `main`.

## Python CI Job

The `python-ci` job runs on `ubuntu-latest` with Python 3.12. It installs the package with development dependencies, then runs:

- lock-hash validation for canonical profile/registry JSON
- `python -m ruff check python/libreprimus tests/python`
- `python -m pytest -q tests/python`
- `python -m libreprimus.cli smoke`
- transform registry validation
- solved-baseline manifest validation
- result-store manifest validation

## Optional CMake CPU Job

Stage 2C includes a CPU-only CMake smoke job on `ubuntu-latest`. It configures with `LPGPU_ENABLE_CUDA=OFF`, builds the scaffold, and runs CTest.

## What CI Checks

CI checks Python style, Python tests, CLI smoke wiring, committed profile/registry lock hashes, transform-registry metadata, solved-baseline manifests, result-store manifests, and the CPU CMake scaffold.

Static workflow tests also validate the parsed YAML structure, trigger branches, permissions, concurrency, job names, required commands, and no artifact-upload or secret usage.

## What CI Deliberately Does Not Check

CI does not run raw-data real-source smoke commands, generated result-store imports, CUDA builds, search campaigns, scoring, or long benchmarks.

## Raw-Data-Free Policy

The workflow must pass on a clean checkout without local transcript, Pastebin, workbook, or mirrored raw reference files.

## Generated-Output Policy

The workflow does not upload generated corpus, solved-baseline, result-store, SQLite, or raw-data artifacts by default.

## CUDA-Free Policy

The default workflow does not require CUDA or GPU runners. Future CUDA CI requires a separate parity-tested stage.

## Troubleshooting

If CI fails locally, run `scripts/ci/run-python-ci.ps1`, `scripts/ci/run-schema-manifest-checks.ps1`, and `scripts/ci/validate-workflow-static.ps1` on Windows, or the `.sh` equivalents on Linux. Real-source conditional tests should skip cleanly when raw files are absent.

After pushing workflow changes, run `scripts/ci/verify-remote-workflow.ps1` or `scripts/ci/verify-remote-workflow.sh` to verify the public raw workflow. This check uses `raw.githubusercontent.com` and does not require `gh`.
