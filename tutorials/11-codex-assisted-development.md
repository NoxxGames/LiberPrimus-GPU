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

## Stage 2E Guardrails

For exploratory dry-run planner work, require `libreprimus experiment validate-exploratory`, `libreprimus experiment dry-run`, and the full consistency suite. Stage 2E may estimate bounded candidate counts, but it must not enumerate candidate plaintexts or execute unsolved-page searches.

## Stage 2F Guardrails

For bounded CPU execution work, require `libreprimus execution validate`, `libreprimus execution run`, and blocked unsolved manifest tests. Stage 2F may run synthetic and solved-fixture-only manifests, but it must not execute unsolved pages, search, candidate generation, scoring, CUDA, canonical corpus activation, or page-boundary finalization.

## Stage 2G Guardrails

For proposal workflow work, require `libreprimus proposal validate`, `libreprimus proposal review-packet`, and approval-gate tests. Stage 2G must not create approved records automatically, execute proposals, generate candidates, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Stage 2H Guardrails

For approval-gated execution work, require `libreprimus approval-execution validate`, `libreprimus approval-execution run`, and blocked no-op real-proposal tests. Stage 2H may run approved synthetic and solved-control requests only; it must not commit approved unsolved-page approval records or enable search, candidate generation, scoring, CUDA, canonical corpus activation, or page-boundary finalization.

## Stage 2I Guardrails

For the first real approval packet, require `libreprimus approval-readiness validate`, `libreprimus approval-readiness packet`, and tests proving no execution runner is called. Stage 2I proposals remain pending and unapproved; generated readiness packets must not include raw unsolved text or candidate plaintext.

## Stage 2J Guardrails

For bounded auto-run policy work, require `libreprimus bounded-experiment validate-policy`, `validate-queue`, `check-queue`, and `run-all` against the Stage 2J queue. Policy-passing bounded local CPU items do not require per-experiment approval, but over-budget, CUDA/GPU, cloud, paid-service, generated-output-commit, canonical-corpus, page-boundary, and solve-claim actions still require explicit instruction or remain blocked. If a policy-passing queue item has no safe executor, record an explicit deferred result instead of generating candidate plaintexts or solve evidence.

## Stage 3A Guardrails

For minimal bounded executor work, require `libreprimus bounded-run run-caesar-affine`, `bounded-run summary`, schema validation, and generated-output ignore checks. Full candidate outputs must remain ignored. Committed notes may summarize run ID, candidate count, top score, and transform parameters only. Minimal triage scores and top-k records are leads, not solve evidence.

## Stage 3B Guardrails

For lead inspection and scoring refinement work, require `libreprimus candidate-inspect inspect-stage3a`, `bounded-run rerank`, reverse-direction bounded-run smoke when implemented, schema or summary validation, and generated-output ignore checks. Full candidate outputs must not be committed. Research logs may summarize scores, qualitative labels, and transform parameters only, and must not claim a solve.

## Stage 3C Guardrails

For scoring calibration work, require `libreprimus scoring calibrate`, `scoring calibration-summary`, schema validation, null-control determinism tests, crib-check tests, and generated-output ignore checks. Do not tune scoring around one candidate, do not use external services or large dictionaries, and do not treat crib hits or positive-control-like labels as solve evidence.

## Stage 3D Guardrails

For bounded Vigenere key-list work, require `libreprimus bounded-run run-vigenere-key-list`, `bounded-run summary`, exact key-count tests, key-expansion rejection tests, calibrated scoring checks, and generated-output ignore checks. The Stage 3D key list is explicit-list only; do not infer keys, mutate keys, search key lengths, use CUDA, or commit candidate dumps.
