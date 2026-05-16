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

## Stage 2A Guardrails

For transform-registry work, require CPU reference metadata, SHA-256 locks, alias resolution tests, manifest-runner outputs under ignored result paths, and all solved baselines passing through registry dispatch.

Prompts should state that manifest-addressable solved baselines are regression runs, not search campaigns, and that search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

## Stage 2B Guardrails

For result-store work, require JSONL and SQLite outputs to stay under ignored result directories. Require schemas, provenance capture, generated-artifact records, validation commands, and a developer log before commit.

Prompts should state that solved-baseline imports are regression evidence only, not unsolved-page experiments, and that search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

## Stage 2C Guardrails

For CI work, require `.github/workflows/ci.yml`, local reproduction scripts, static workflow tests, docs, and a developer log. CI must stay raw-data-free, CUDA-free, secret-free, and must not upload generated corpus or result artifacts by default.

Do not weaken CI by removing tests or conditional real-source skip checks just to get a green run.

## Stage 2D Guardrails

For consistency hardening work, require `libreprimus consistency check-all`, result-store consistency checks, ignored-output checks, and public status checks. Stage 2D is a hardening stage only; it does not authorize search, scoring, CUDA, canonical corpus activation, or page-boundary finalization.
