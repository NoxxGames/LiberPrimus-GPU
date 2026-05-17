# Stage 3H reset/advance ablation

## Initial state

- Branch: `main`
- Local HEAD: `d54084466992d1828fc9967399653f83c71b82f4`
- origin/main: `d54084466992d1828fc9967399653f83c71b82f4`
- Local equals origin/main: true
- Latest CI observed: run `25995088383`, success
- Stage 3E queue present: true
- Reset/advance item present: true (`stage3e_reset_advance_ablation_v1`)
- Expected reset/advance candidate count: `64`
- Stage 3G summary present: true
- Input slice loader present: true
- Scoring calibration present: true
- Generated outputs staged: `0`
- Raw files staged: `0`
- Root Deep Research source file present: true, untracked and must not be staged
- Research report staged: `0`
- Unexpected tracked changes: none before Stage 3H edits

## Phase 1 output directory

- Created ignored Stage 3H output directory: `experiments/results/bounded-auto-runs/stage3h/`
- Generated output ignore checks:
  - `candidate_records.jsonl`: ignored
  - `top_candidates.jsonl`: ignored
  - `negative_control_records.jsonl`: ignored
  - `summary.json`: ignored

## Phase 2 queue

- Created `experiments/queues/stage3h-bounded-cpu-queue.yaml`.
- Main item: `stage3h_reset_advance_ablation_v1`.
- Candidate count verified by formula: `8 * 4 * 2 = 64`.
- Negative-control item present: `stage3h_family_specific_negative_controls_v1`, count `100`.
- Stage 3E reset/advance item was updated from dry-run-only to runnable through the Stage 3H executor.
- All Stage 3H queue items pass the standing operator policy.

## Phase 3 reset/advance state machine

- Added `python/libreprimus/bounded_execution/reset_advance.py`.
- Reset modes: `none`, `word`, `clause`, `line`.
- Advance modes: `runes_only`, `token_break_preserving`.
- Missing metadata returns explicit deferral reasons.
- Flat token-break fallback warning is supported.

## Phase 4 transform adapters

- Added `python/libreprimus/bounded_execution/reset_advance_ablation.py`.
- Added `python/libreprimus/bounded_execution/prime_stream_variants.py`.
- Vigenere, `prime_minus_one`, `prime_mod29`, and `prime_gap` adapters are implemented.
- Candidate count before metadata deferrals: `64`.

## Phase 5 negative controls

- Added `python/libreprimus/bounded_execution/negative_controls.py`.
- Implemented deterministic `rune_shuffle_same_length`, `rune_freq_preserving_shuffle`, `separator_randomised_variant`, and `wrong_mapping_variant` controls.
- Expected control count for the Stage 3H run: `100`.
- No external data is used.

## Phase 6 CLI

- Added `libreprimus bounded-run run-reset-advance-ablation`.
- `libreprimus bounded-run summary` prints Stage 3H counts and top reset/advance fields.
- `libreprimus bounded-experiment run-all` can dispatch the Stage 3H reset/advance item.

## Phase 7 local run

- Executed `stage3h_reset_advance_ablation_v1`.
- Input slice: `stage3a-page-candidate-018-reviewable-slice`.
- Input length: `87`.
- Metadata available: word `true`, clause `true`, line `true`, token breaks `true`.
- Expected candidates: `64`.
- Executed candidates: `64`.
- Deferred candidates: `0`.
- Negative controls: `100`.
- Top candidate: `prime_minus_one:offset=1`, reset `line`, advance `runes_only`.
- Top score: `6.817909`.
- Calibrated confidence label: `noisy`.
- Generated outputs staged: `0`.
- Solve claim: `0`.

## Phase 8 tests

- Added Stage 3H tests for state-machine behaviour, transform adapters, negative controls, CLI execution, output schema, and queue policy.
- Targeted Stage 3H pytest result: `17 passed`.
- Targeted Ruff result: pass.

## Phase 9 docs

- Created Stage 3H architecture, experiment, scoring, research, and CLI docs.
- Updated README, STATUS, ROADMAP, EXPERIMENTS, RESULTS_SCHEMA, TESTING, AGENTS, CIPHER_CATALOG, and tutorials.
- Reinforced that Stage 3H top candidates and controls are leads only, not solve evidence.

## Phase 10 validation

- Ruff: pass.
- Pytest: `612 passed`.
- Smoke CLI: pass.
- Consistency suite: `276` pass, `0` fail.
- `scripts/ci/run-consistency-checks.ps1`: pass.
- `scripts/ci/verify-public-docs-status.ps1`: `11` pass.
- `scripts/ci/verify-lock-hashes.ps1`: pass.
- `scripts/ci/validate-workflow-static.ps1`: `13` pass.
- Generated outputs staged: `0`.
- Raw files staged: `0`.
- Research report staged: `0`.

## Phase 11 GitHub issue

- Created issue: `https://github.com/NoxxGames/LiberPrimus-GPU/issues/26`.
- Issue title: `Stage 3H: reset advance ablation`.
- The issue will be closed after commit, push, and pushed CI verification.

## CI follow-up

- First pushed CI run `25997334094` failed in `tests/python/test_stage3h_output_schema.py` because the test used ignored local corpus-candidate metadata absent from GitHub-hosted raw-data-free CI.
- Fixed the test to use synthetic inline token records, matching the Stage 3H CI-safe fixture pattern.
- Targeted rerun for the fixed test passed locally.
