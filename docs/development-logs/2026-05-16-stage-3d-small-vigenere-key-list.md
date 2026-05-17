# Stage 3D Small Vigenere Key List Developer Log

Date: 2026-05-16

## Initial State

- Branch: `main`
- Local HEAD: `ae8884fc1a6c0833c523c90a3be827b85beb074a`
- Origin/main: `ae8884fc1a6c0833c523c90a3be827b85beb074a`
- Local equals origin/main: true
- Git status summary: clean
- Latest CI status: `completed/success`, run `25981059857`
- Stage 3C queue present: true
- Stage 3C key-list item present: true
- Declared key count: `4`
- Stage 3C calibration outputs present locally: true
- Bounded execution package present: true
- Vigenere transform implementation present: true
- Generated outputs staged: `0`
- Raw files staged: `0`
- Research report staged: `0`

## Output Directory

Created the local ignored output path `experiments/results/bounded-auto-runs/stage3d/`. The broad `experiments/results/**` ignore rule covers Stage 3D generated outputs, including local candidate records and summaries.

## Implementation

Added bounded explicit-key Vigenere execution for the Stage 3D four-key queue item. The runner:

- loads exactly `LIBER`, `PRIMUS`, `DIVINITY`, and `CICADA` from the committed queue;
- rejects key mutation or expansion;
- checks the candidate count against `candidate_count_upper_bound`;
- reuses the Stage 3A reviewable input-slice loader;
- applies decrypt-subtract Vigenere over Gematria index values;
- applies Stage 3C calibrated scoring and crib checks;
- writes generated candidate outputs only to ignored result paths.

## Local Run

The Stage 3D run executed four candidates for input slice `stage3a-page-candidate-018-reviewable-slice`, input length `87`.

- Top key: `LIBER`
- Top score: `6.298395`
- Calibrated confidence label: `noisy`
- Generated outputs staged: `0`
- Solve claim: `false`

## Validation Notes

Stage 3D tests cover exact key-list loading, key expansion rejection, Gematria key mapping, four-candidate execution, output schemas, CLI execution, ignored outputs, queue candidate count, and policy blocking when declared keys exceed candidate bounds.

Local validation:

- `ruff check python/libreprimus tests/python`: pass
- `pytest -q tests/python`: `556 passed`
- `libreprimus.cli smoke`: pass
- `libreprimus.cli consistency check-all --allow-warnings`: `239/239` pass
- `scripts/ci/run-consistency-checks.ps1`: pass
- `scripts/ci/verify-public-docs-status.ps1`: pass
- `scripts/ci/verify-lock-hashes.ps1`: pass
- `scripts/ci/validate-workflow-static.ps1`: pass

Git safety:

- Raw files staged: `0`
- Generated outputs staged: `0`
- SQLite files staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`
- Stage 3D candidate outputs remain ignored by `.gitignore`.

CI status is recorded after commit, push, and post-push verification.
