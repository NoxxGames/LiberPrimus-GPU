# Stage 3B Lead Inspection And Scoring Refinement Developer Log

Date: 2026-05-16

## Initial State

- Branch: `main`
- Local HEAD: `3f50039eeba48ac9e3e2e94a0a59bd9309880e61`
- Origin/main: `3f50039eeba48ac9e3e2e94a0a59bd9309880e61`
- Local equals origin/main: true
- Git status at start: clean
- Latest CI status: success (`25979866099`)
- Stage 3A candidate outputs present: true
- Stage 3A top candidate file present: true
- Stage 3A summary present: true
- Stage 3A committed research summary present: true
- Generated outputs staged: 0
- Raw files staged: 0
- Research report staged: 0
- Unexpected tracked changes: none

## Phase Notes

- Stage 3B inspects generated Stage 3A candidate outputs without committing full candidate dumps.
- Minimal triage scoring may be refined, but scores remain lead triage only and cannot justify solve claims.
- New generated Stage 3B outputs remain ignored under `experiments/results/bounded-auto-runs/stage3b/`.

## Implementation Summary

- Added `libreprimus.candidate_inspection` for summary-only inspection of generated candidate records.
- Added `libreprimus candidate-inspect inspect-stage3a` and `summary`.
- Refined minimal triage scoring with length normalization, separator-aware word counts, vowel-band scoring, impossible-bigram penalties, feature explanations, confidence labels, and explicit `no_solve_claim=true`.
- Added `libreprimus bounded-run rerank` for ignored rerank outputs.
- Added reverse-direction Caesar and affine enumeration and queued `stage3b-caesar-affine-reverse-direction`.

## Local Results

- Stage 3A original top lead: `affine_mod29`, `a=25`, `b=1`, score `33.353307`.
- Stage 3A inspection label: `weak_noisy`.
- Refined rerank top lead: `affine_mod29`, `a=19`, `b=26`, score `8.040756`, label `noisy`.
- Reverse-direction top lead: `affine_mod29_reverse`, `a=26`, `a_inverse=19`, `b=20`, score `8.040756`, label `noisy`.
- Reverse-direction candidate count: `841`.
- Generated outputs staged: 0.
- No solve claim, no CUDA, no canonical corpus activation, no page-boundary finalization.

## Validation

- Ruff: pass.
- Pytest: `534 passed`.
- CLI smoke: pass.
- Consistency check-all: `216` pass, `0` fail.
- CI consistency script: pass.
- Public docs status: `11` pass.
- Lock hashes: pass.
- Workflow static validation: `13` pass.
- Generated Stage 3A and Stage 3B candidate outputs are ignored.
- Raw/generated/SQLite outputs, candidate dumps, and `LiberPrimus-Research-Report.md` are not staged.
