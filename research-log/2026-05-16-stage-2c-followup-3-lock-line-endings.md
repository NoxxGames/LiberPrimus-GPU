# Stage 2C-followup-3 Lock Line Endings

## Status

CI failure fix for Linux SHA-256 lock mismatches.

## Goal

Make profile and registry lock validation deterministic across Windows and Linux by repairing Git attributes, normalizing canonical JSON files to LF bytes, regenerating lock metadata, and adding CI checks that fail on drift.

## Result

The previous CI failure was caused by CRLF-generated locks for JSON files that GitHub Actions checked out with LF bytes. Stage 2C-followup-3 switches those locks to LF canonical bytes and adds explicit verification scripts and tests.

Local validation passed with `247` Python tests, Ruff, lock verification, registry/manifest validation, Python smoke, and CMake CPU smoke with CUDA disabled.

## Non-goals

No unsolved-page search, scoring, CUDA implementation, canonical corpus activation, or page-boundary finalization was added.
