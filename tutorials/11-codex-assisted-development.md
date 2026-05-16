# Codex-Assisted Development

## AGENTS.md

`AGENTS.md` tells Codex the non-negotiable project rules: no solve claims, no raw-data edits, no generated-output commits, explicit staging, tests, logs, and GitHub push policy.

## Safe Prompts

Ask Codex for scoped stages. Include non-goals, stop conditions, validation commands, and staging rules.

## Review Generated Changes

Review code, docs, tests, Git status, and generated files before committing. Treat terminal output as a check, not as evidence.

## Avoid Raw-Data Commits

Before any commit, check staged files for `data/raw/`, generated JSONL, `.venv`, build outputs, and wiki worktrees.

## Require Tests And Logs

Each ingestion, alignment, or project-management stage should update a developer log and run focused tests or dry runs.

For solved-fixture stages, require source/profile SHA-256 provenance, non-canonical flags, generated-output ignore checks, and a developer log before commit.
## Prompting For Stage 1B-Style Work

When asking Codex to add solved-fixture baselines, require explicit provenance, fixture hashes, no generated-output commits, and no search behavior unless a later stage explicitly asks for it.

For Atbash-family work, require declared rotations in fixture manifests and direct-regression tests so existing solved baselines do not regress.
## Stage 1C Guardrails

For Vigenere fixture work, keep keys explicit in fixture manifests, avoid key search, and keep generated solved-baseline outputs ignored. Do not commit mirrored raw reference files, and do not import or copy external tooling code.

## Stage 1D Guardrails

For p56 prime-stream work, require explicit stream parameters, no offset or direction search, payload checks separate from plaintext, and regression checks for direct, Atbash-family, and Vigenere fixtures.
