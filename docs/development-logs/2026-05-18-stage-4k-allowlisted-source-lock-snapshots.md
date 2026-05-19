# Stage 4K Allowlisted Source-Lock Snapshots

## Phase 0 - initial state

- Branch: `main`.
- Local HEAD: `41d7e210c63c7dfa7b14462c7b96d59da0b3b632`.
- `origin/main`: `41d7e210c63c7dfa7b14462c7b96d59da0b3b632`.
- Latest observed CI: passed, run `26121170481`.
- Stage 4J review records: present.
- Stage 4B source records: present.
- Stage 4E source-delta records: present.
- Stage 4F fixture records: present.
- Raw/generated staged files: 0.
- Unexpected tracked changes: none.

Initial validation passed for observation review, path sanitisation, research
synthesis, state drift, consistency, public docs, lock hashes, workflow static
checks, wiki-source validation, and tutorial-to-wiki dry run.

## Phase 1 - directories and ignore policy

- Created ignored public source snapshot cache root:
  `third_party/SourceSnapshots/`.
- Created committed source-lock metadata root:
  `data/locks/third-party/source-snapshots/`.
- Created ignored generated report root:
  `experiments/results/source-lock-snapshots/stage4k/`.
- Updated `.gitignore` with explicit exceptions for README and `.gitkeep`
  marker files only.

## Phase 2 - schemas

- Added source-lock snapshot, fetch, summary, public-source policy, and
  copyright-policy schemas.
- Schema policy rejects raw private data, binaries, images, audio, fonts,
  archives, and solve claims.
- Fetched records require content hashes; committed snapshots are restricted
  to explicit `committed_small_text_snapshot` policy.

## Phase 3 - implementation

- Added `python/libreprimus/source_lock_snapshots/` with loaders,
  allowlist filtering, snapshot policy classification, GitHub metadata helpers,
  ignored-cache fetching, copyright-policy helpers, summary/export, and
  validation.
- Build path reads committed Stage 4B, Stage 4E, Stage 4F, and Stage 4J
  records only.
- Network retrieval is gated by `--allow-network`; validation is offline.

## Phase 4 - CLI

- Added `libreprimus source-lock-snapshots build`.
- Added `libreprimus source-lock-snapshots validate`.
- Added `libreprimus source-lock-snapshots summary`.
- Added `libreprimus source-lock-snapshots list-allowlist`.

## Phase 5 - local run

- Build executed with `--allow-network`.
- Sources considered: 43.
- Unique allowlisted snapshot records: 15.
- Sources fetched into ignored cache: 1.
- GitHub commit-address locks: 8.
- Metadata-only records: 8.
- Ignored local snapshot policy records: 7.
- Committed small text snapshots: 0.
- Rejected unsafe/noisy or non-priority sources: 22.
- Duplicate sources: 6.
- Fetch failures: 6.
- Generated outputs staged: 0.
- Ignored cache staged: 0.

## Phase 6 - tests

- Added Stage 4K schema, allowlist, snapshot-policy, fetcher, GitHub metadata,
  CLI, and ignore-policy tests.
- Focused Stage 4K pytest run: 15 passed.
- Focused Stage 4K ruff run: passed.

## Phase 7 - research synthesis integration

- Added Stage 4K stage-summary record.
- Added `source_lock_snapshots` method-family and retirement records.
- Updated research-synthesis validation for Stage 4K complete and Stage 4L next.
- Updated state-drift checks for Stage 4K complete, Stage 4L next, and source-lock snapshot policy.

## Phase 8 - docs/tutorial/wiki

- Added Stage 4K source-lock snapshot docs and CLI reference.
- Updated public status, roadmap, dataset policy, experiment policy, result-schema
  policy, testing notes, cipher catalog, Stage 4B/4E/4F history docs, tutorials,
  and private/generated data map.

## Phase 9 - consistency integration

- Added Stage 4K source-lock snapshot validation to PowerShell and Bash
  consistency scripts.
- Updated state-drift checks for Stage 4K complete, Stage 4L next, and source-lock
  snapshot policy coverage.

## Phase 10 - validation

- Source-lock snapshot validation: passed.
- Observation-review path sanitisation: passed with zero findings.
- Research-synthesis validation: passed.
- State-drift validation: passed.
- Consistency check-all: passed.
- Smoke: passed.
- Ruff: passed.
- Pytest: 1041 passed.
- PowerShell consistency script: passed.
- Public-docs status, lock hashes, workflow static validation, wiki-source
  validation, and tutorial-to-wiki dry run: passed.
- Generated outputs staged: 0.
- Ignored source snapshot cache staged: 0.
- Raw external artefacts staged: 0.

## Phase 11 - GitHub issue

- Created idempotent tracking issue:
  `Stage 4K: allowlisted public source-lock snapshots` (#56).
- The issue remains open until the Stage 4K push and CI verification pass.
