# Stage 4L - reviewed observation promotion ledger

## Phase 0 - initial state

- Branch: `main`.
- Local HEAD: `55554f5d6a2cc8738f8e9d70a3347f1d9f0d83e0`.
- `origin/main`: `55554f5d6a2cc8738f8e9d70a3347f1d9f0d83e0`.
- Local equals origin/main: true.
- Latest CI before Stage 4L: run `26123716595`, success.
- Stage 4J review records present: true.
- Stage 4K source-lock records present: true.
- Disabled manifests present: true.
- Raw/generated staged: 0.
- Unexpected tracked changes: none.
- Existing untracked ignored/generated result directories and one unrelated third-party note were left untouched.

## Phase 1 - output dirs

- Created `experiments/results/observation-promotion/`.
- Created `experiments/results/observation-promotion/stage4l/`.
- Added `.gitignore` rules so generated observation-promotion reports remain ignored while README and `.gitkeep` marker files can be committed.

## Phase 2 - schemas

- Added reviewed observation promotion ledger schema.
- Added observation promotion readiness and blocker schemas.
- Added manifest-readiness record and summary schemas.
- Schemas keep `execution_enabled=false` and `solve_claim=false`; blocked,
  deferred, quarantined, and rejected records require blockers.

## Phase 3 - implementation

- Added `python/libreprimus/observation_promotion/` with loaders, promotion
  gates, blocker records, ledger builder, manifest readiness records, export,
  summary, and validation.
- The evaluator links Stage 4J decisions to Stage 4K source-lock records where
  possible and preserves review-only observations as blocked, deferred,
  source-reference-only, quarantined, or control-only.
- Cuneiform and dot observations remain blocked or quarantined unless future
  reviewed coordinates and accepted readings exist.
- Cookie, stego/audio, and image-artifact paths remain blocked or deferred by
  their documented Stage 4G/4F/4E constraints.

## Phase 4 - CLI

- Added `libreprimus observation-promotion build`.
- Added `libreprimus observation-promotion validate`.
- Added `libreprimus observation-promotion summary`.

## Phase 5 - local run

- Build executed with `--allow-warnings`.
- Reviewed observations loaded: 96.
- Ledger records created: 96.
- Readiness records created: 96.
- Blocker records created: 109.
- Manifest readiness records created: 12.
- Ready for manifest: 0.
- Ready as control-only: 17.
- Source-reference-only: 14.
- Blocked/deferred/quarantined/rejected: 47 / 2 / 15 / 1.
- Cuneiform ready/deferred/blocker: 0 / 0 / 5.
- Dot ready/quarantined/blocker: 0 / 15 / 15.
- Cookie ready/blocked: 0 / 3.
- Stego/audio ready/deferred/blocker: 0 / 0 / 10.
- Generated outputs staged: 0.
- Raw staged: 0.

## Phase 6 - tests

- Added Stage 4L schema, promotion-gate, blocker, manifest-readiness, CLI, and
  ignore-policy tests.
- Focused Stage 4L pytest run: 13 passed.
- Focused Stage 4L ruff run: passed.

## Phase 7 - research synthesis integration

- Added Stage 4L stage-summary record.
- Added `observation_promotion_ledger` method-family and retirement records.
- Updated research-synthesis validation for Stage 4L complete and Stage 4M next.
- Updated state-drift checks for Stage 4L complete, Stage 4M next, and promotion-ledger policy.
- Research-synthesis validation passed.
- State-drift validation passed.

## Phase 8 - docs/tutorial/wiki

- Added Stage 4L promotion ledger, readiness policy, blocker taxonomy,
  manifest-readiness, research, and CLI reference docs.
- Updated STATUS, ROADMAP, AGENTS, README, staged plan, schema/testing/experiment
  docs, observation policy docs, onboarding state, tutorials, and wiki-source
  mirrors.

## Phase 9 - consistency integration

- Added Stage 4L observation-promotion validation to PowerShell and Bash
  consistency scripts.
- Updated state-drift checks for Stage 4L complete, Stage 4M next, and promotion
  ledger policy coverage.

## Phase 10 - validation

- Observation-promotion validation: passed.
- Path sanitisation: passed.
- Research-synthesis validation: passed.
- State-drift validation: passed.
- Full consistency validation: passed.
- Smoke validation: passed.
- Ruff: passed.
- Pytest: 1054 passed.
- PowerShell consistency script: passed.
- Public docs status, lock hashes, workflow static validation, wiki-source
  validation, and wiki dry run: passed.
- Generated outputs staged: 0.
- Raw staged: 0.
