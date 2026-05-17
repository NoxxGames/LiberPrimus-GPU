# Stage 3C Scoring Calibration And Null Controls Developer Log

Date: 2026-05-16

## Initial State

- Branch: `main`
- Local HEAD: `12285bdc914768519730ed70ab84d41cc726b459`
- Origin/main: `12285bdc914768519730ed70ab84d41cc726b459`
- Local equals origin/main: true
- Git status at start: clean
- Latest CI status: success (`25980639992`)
- Stage 3A outputs present: true
- Stage 3B outputs present: true
- Scoring modules present: true
- Solved fixtures present: true
- Generated outputs staged: 0
- Raw files staged: 0
- Research report staged: 0
- Unexpected tracked changes: none

## Phase Notes

- Stage 3C calibrates scoring before any wider transform family expansion.
- Positive controls use existing solved fixture expected plaintext and safe synthetic readable controls.
- Null and negative controls are deterministic and local.
- Crib checks are tiny transparent weak features only.
- Generated calibration JSON and JSONL outputs remain ignored.
- No solve claim, CUDA, canonical corpus activation, or page-boundary finalization is made.

## Implementation Summary

- Added scoring-control, calibration-summary, and crib-check schemas.
- Added `data/scoring/cribs-tiny-v0.txt` and deterministic `data/scoring/null-control-policy-v0.yaml`.
- Added positive-control loading from solved fixtures, deterministic null controls, synthetic negative controls, crib checks, calibration thresholds, and candidate reclassification.
- Added `libreprimus scoring calibrate`, `crib-check`, and `calibration-summary`.
- Added `experiments/queues/stage3c-bounded-cpu-queue.yaml` for a conservative Stage 3D tiny explicit-key Vigenere preview and an over-budget blocked control.

## Local Calibration Result

- Positive controls: `12`.
- Null controls: `250`.
- Negative controls: `4`.
- Stage 3 candidate records calibrated: `3`.
- Positive-control score range: `4.806942` to `29.310739`.
- Null-control score range: `1.163663` to `11.299382`.
- Negative-control score range: `-21.268966` to `0.560659`.
- Stage 3A top classification: `noisy`.
- Stage 3B reverse top classification: `noisy`.
- Recommended next step: Stage 3D small Vigenere known-motif key-list preview with calibrated scoring.

## Focused Validation

- Stage 3C tests: `11` passed.
- Focused Ruff check: pass.
- Stage 3C queue policy check: one policy pass, one intentional over-budget block.

## Full Validation

- Ruff: pass.
- Pytest: `545` passed.
- CLI smoke: pass.
- Consistency check-all: `231` pass, `0` fail.
- CI consistency script: pass.
- Public docs status: `11` pass.
- Lock hashes: pass.
- Workflow static validation: `13` pass.
- Generated calibration outputs are ignored.
- Raw/generated/SQLite outputs and `LiberPrimus-Research-Report.md` are not staged.

## GitHub Issue

- Issue: `https://github.com/NoxxGames/LiberPrimus-GPU/issues/21`
- Comment added with calibration counts, classifications, next stage, and validation results.
