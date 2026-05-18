# Docker

## Purpose

This directory is reserved for future documented, reproducible container recipes.

## Current Status

Docker is not the primary supported path after Stage 3V. Current validation is based on local Python/CMake commands and GitHub Actions raw-data-free CI. Stage 3W does not add container automation.

## What Belongs Here

Future container files may be added only when they reproduce existing local validation without weakening raw-data, generated-output, CUDA, or solve-claim policy.

## What Does Not Belong Here

Do not commit large images, downloaded installers, secrets, generated build artefacts, raw data, generated experiment outputs, SQLite databases, or extracted payloads.

## Codex Modification Policy

Codex may edit documentation here. Do not add Docker build implementation unless a future stage explicitly scopes it.
