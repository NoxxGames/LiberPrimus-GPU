# Stage 3G p56-local prime offset sweep

## Initial state

- Branch: `main`
- Local HEAD: `0be72ce439c9dd0abaed561a73dadc08cce44d8c`
- origin/main: `0be72ce439c9dd0abaed561a73dadc08cce44d8c`
- Local equals origin/main: true
- Latest CI observed: run `25994048099`, success
- Stage 3E queue present: true
- p56 offset item present: true (`stage3e_prime_minus_one_offsets_v1`)
- Expected p56 candidate count: `256`
- Mersenne item already present: false
- Prime-stream code present: true, solved-fixture scoped
- Input slice loader present: true
- Scoring calibration present: true
- Generated outputs staged: `0`
- Raw files staged: `0`
- Root Deep Research source file present: true, untracked and must not be staged
- Research report staged: `0`
- Unexpected tracked changes: none before Stage 3G edits

## Phase 1 output directory

- Created ignored Stage 3G output directory: `experiments/results/bounded-auto-runs/stage3g/`
- Generated Stage 3G output ignore check: true via existing `experiments/results/**` rule

## Phase 2 Mersenne backlog addition

- Added `stage3i_mersenne_prime_stream_tiny_v1` to `experiments/queues/stage3e-method-backlog.yaml`
- Added matching queue item to `experiments/queues/stage3e-bounded-cpu-queue.yaml`
- Candidate count verified: `192`
- Implementation status: `needs_executor`
- Execution disabled / dry-run-only: true

## Phase 3 prime offset executor

- Added `python/libreprimus/bounded_execution/prime_offset_sweep.py`
- Prime generator: deterministic, reuses existing solved-fixture prime helper
- Offset sweep: offsets `0..63`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`
- Expected candidates: `256`
- Supported candidates before run: `256`
- Deferred candidates before run: `0`

## Phase 4 CLI

- Added `libreprimus bounded-run run-prime-offset-sweep`
- `bounded-run summary` prints Stage 3G prime fields
- `bounded-experiment run-all` dispatches `stage3e_prime_minus_one_offsets_v1` to the Stage 3G executor when policy passes

## Phase 5 local experiment run

- Command: `libreprimus bounded-run run-prime-offset-sweep --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage3e-bounded-cpu-queue.yaml --item-id stage3e_prime_minus_one_offsets_v1 --out-dir experiments/results/bounded-auto-runs/stage3g --top-k 25 --allow-warnings`
- Run ID: `stage3g-stage3e_prime_minus_one_offsets_v1-20260517T150902Z`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Executed: true
- Expected candidates: `256`
- Executed candidates: `256`
- Deferred candidates: `0`
- Top offset/direction/reset: `29` / `reverse` / `line`
- Top score: `1.36709`
- Top calibrated confidence label: `inconclusive`
- Generated outputs staged: `0`
- Research summary: `research-log/2026-05-16-stage-3g-p56-local-prime-offset-sweep-summary.md`

## Phase 6 tests

- Added Stage 3G prime executor, CLI, output, Mersenne backlog, and queue integration tests.
- Updated Stage 3E count/support tests for the Mersenne item and Stage 3G runnable p56 executor.
- Focused pytest result: `24 passed`
- Focused ruff result: passed

## Phase 7 docs

- Created Stage 3G experiment, research, and CLI docs.
- Created Mersenne/perfect-number stream probe documentation.
- Updated public status, testing, result schema, cipher catalog, tutorials, and AGENTS guardrails.
- No solve claim reinforced: true
