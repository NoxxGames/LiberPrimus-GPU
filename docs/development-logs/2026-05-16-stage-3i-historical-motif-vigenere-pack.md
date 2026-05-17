# Stage 3I Historical Motif Vigenere Pack

Date: 2026-05-16

## Initial State

- Branch: `main`
- Local HEAD: `a78da4e7ebf629716ab69ccb10adf0dbb8bf8d26`
- Origin `main`: `a78da4e7ebf629716ab69ccb10adf0dbb8bf8d26`
- Local equals origin/main: `true`
- Latest CI: `25997591959`, success
- Stage 3E queue present: `true`
- Historical key-pack item present: `true`
- Declared key count: `14`
- Reset modes: `none`, `line`
- Advance modes: `runes_only`, `token_break_preserving`
- Expected candidates: `56`
- Stage 3F Vigenere key-pack executor present: `true`
- Scoring calibration present: `true`
- Generated outputs staged: `0`
- Raw files staged: `0`
- Root Deep Research source file present: `true`, untracked and intentionally unstaged
- Research report staged: `0`

## Output Directory

- Created ignored local output area: `experiments/results/bounded-auto-runs/stage3i/`.
- Existing repository ignore policy covers generated Stage 3I candidate outputs through `experiments/results/**`.

## Executor Support

- Reused the Stage 3F Vigenere key-pack executor.
- Generalized it from the LP evidence item to a small allow-list of bounded key-pack queue items.
- Added support for `stage3e_vig_history_key_pack_v1`.
- Preserved explicit key-list enforcement, reset/advance validation, calibrated scoring, and no-solve-claim safety flags.
- Added `evidence_family=historical_motif_key_pack` to candidate identity fields for the historical pack.

## Queue Update

- Updated `stage3e_vig_history_key_pack_v1` from `needs_executor` to `runnable_now`.
- Added the same safe reviewable-slice selector metadata used by Stage 3F.
- Set output policy to `experiments/results/bounded-auto-runs/stage3i`.
- Kept the candidate count at `56`.

## Local Run

- Command: `libreprimus bounded-run run-vigenere-key-pack --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage3e-bounded-cpu-queue.yaml --item-id stage3e_vig_history_key_pack_v1 --out-dir experiments/results/bounded-auto-runs/stage3i --top-k 25 --allow-warnings`
- Run ID: `stage3i-stage3e_vig_history_key_pack_v1-20260517T173351Z`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Expected candidates: `56`
- Executed candidates: `56`
- Deferred candidates: `0`
- Top key: `SELFRELIANCE`
- Top reset mode: `line`
- Top advance mode: `runes_only`
- Top score: `6.988031`
- Top calibrated confidence label: `noisy`
- Generated outputs staged: `0`
- Solve claim: `false`

## Research Summary

- Wrote `research-log/2026-05-16-stage-3i-historical-motif-vigenere-pack-summary.md`.
- The committed summary records only key/mode/score metadata and interpretation.
- Full candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3i/`.

## Tests And Documentation

- Added Stage 3I tests for historical key-pack validation, synthetic CLI execution, output identity fields, generated-output ignore policy, and count drift blocking.
- Updated Stage 3E executor-support tests because the historical Vigenere pack is now runnable.
- Created docs:
  - `docs/experiments/stage-3i-historical-motif-vigenere-pack.md`
  - `docs/research/stage-3i-historical-motif-vigenere-pack.md`
  - `docs/reference/historical-vigenere-key-pack-cli.md`
- Updated README, STATUS, ROADMAP, EXPERIMENTS, RESULTS_SCHEMA, TESTING, AGENTS, CIPHER_CATALOG, and tutorials.
- Added the future visual numeric observation registry note for base-60 or cuneiform-like numbers, binary dot patterns, symmetry/asymmetry, and page imagery.
- Targeted tests passed: `22 passed`.
- Ruff passed for `python/libreprimus` and `tests/python`.

## Validation

- Ruff: passed.
- Pytest: `622 passed`.
- Smoke: passed.
- Consistency suite: `279` checks passed.
- CI consistency script: passed.
- Public docs status: `11` passed.
- Lock hash verification: passed.
- Workflow static validation: `13` passed.

## GitHub Issue

- Created issue: `https://github.com/NoxxGames/LiberPrimus-GPU/issues/27`.
- Issue title: `Stage 3I: historical motif Vigenere key pack`.
- The issue will be closed after commit, push, and pushed CI verification.
