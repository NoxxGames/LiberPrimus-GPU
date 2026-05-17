# Stage 3F evidence-key Vigenere pack

## Initial state

- Branch: main
- Local HEAD: 1c5e6c197876cbaa720d9271293f6ef7a489eacd
- origin/main: 1c5e6c197876cbaa720d9271293f6ef7a489eacd
- Local equals origin/main: true
- Latest CI observed: run 25993173229, success
- Stage 3E queue present: true
- Target item present: true (`stage3e_vig_lp_evidence_pack_v1`)
- Declared key count: 12
- Declared reset modes: none, line
- Declared advance modes: runes_only, token_break_preserving
- Expected candidate count: 48
- Stage 3D Vigenere executor present: true
- Input slice loader present: true
- Scoring calibration present: true
- Generated outputs staged: 0
- Raw files staged: 0
- Root Deep Research source file present: true, untracked and must not be staged
- Research report staged: 0
- Unexpected tracked changes: none before Stage 3F edits

## Phase 1 output directory

- Created ignored Stage 3F output directory: `experiments/results/bounded-auto-runs/stage3f/`
- Generated Stage 3F output ignore check: true via existing `experiments/results/**` rule

## Phase 2 executor

- Added `python/libreprimus/bounded_execution/vigenere_key_pack.py`.
- Key validation: 12 declared LP evidence keys only.
- Candidate count validation: `12 * 2 * 2 = 48`.
- Reset modes implemented: `none`, `line`.
- Advance modes implemented: `runes_only`, `token_break_preserving`.
- Missing line metadata behavior: defer line-reset candidates with `line_reset_metadata_missing`.
- Missing token-break metadata behavior: execute flat mode with `token_break_metadata_missing_flat_mode_used`.
- Stage 3E target queue item marked `runnable_now` for the Stage 3F executor; historical Vigenere remains deferred.

## Phase 3 CLI

- Added `libreprimus bounded-run run-vigenere-key-pack`.
- Updated bounded run summary output with expected/executed/deferred counts, key count, reset modes, and advance modes.
- Updated `bounded-experiment run-all` to run only `stage3e_vig_lp_evidence_pack_v1` when policy passes.

## Phase 4 local run

- Command: `libreprimus bounded-run run-vigenere-key-pack --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage3e-bounded-cpu-queue.yaml --item-id stage3e_vig_lp_evidence_pack_v1 --out-dir experiments/results/bounded-auto-runs/stage3f --top-k 25 --allow-warnings`
- Run ID: `stage3f-stage3e_vig_lp_evidence_pack_v1-20260517T143322Z`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Expected candidates: `48`
- Executed candidates: `48`
- Deferred candidates: `0`
- Top key/modes: `EMERGE`, reset `none`, advance `runes_only`
- Top score: `6.800831`
- Calibrated confidence label: `noisy`
- Solve claim: `false`
- Generated outputs staged: `0`

## Phase 5 tests

- Added Stage 3F executor, CLI, output, and queue-integration tests.
- Targeted pytest result: `34 passed` across Stage 3F, Stage 3E support/dry-run, and public-doc consistency tests.
- Ruff targeted result: passed.

## Phase 6 docs

- Created docs:
  - `docs/experiments/stage-3f-evidence-key-vigenere-pack.md`
  - `docs/research/stage-3f-evidence-key-vigenere-pack.md`
  - `docs/reference/vigenere-key-pack-cli.md`
- Added summary-only research log:
  - `research-log/2026-05-16-stage-3f-evidence-key-vigenere-pack-summary.md`
- Updated README, STATUS, ROADMAP, experiment docs, schema docs, testing docs, AGENTS, cipher catalog, and tutorials.
- No solve claim reinforced: true.

## Phase 7 validation

- Ruff: passed.
- Pytest: `581 passed`.
- Smoke: passed.
- Consistency: `269 passed`.
- CI consistency script: passed.
- Public docs status: `11 passed`.
- Lock hashes: passed.
- Workflow static validation: `13 passed`.

## Phase 8 GitHub issue

- GitHub issue created: `https://github.com/NoxxGames/LiberPrimus-GPU/issues/24`
- Summary comment added: true.
- Issue left open pending post-push CI observation.
