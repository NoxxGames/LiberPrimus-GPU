# Stage 4I scorer consolidation and calibration

Date: 2026-05-18

## Scope

Stage 4I consolidates existing scoring and calibration behavior into durable contracts and records. Scoring remains a triage aid only; this stage does not create a new scoring model, run unsolved-page campaigns, use CUDA, process raw data, activate the canonical corpus, finalize page boundaries, or make solve claims.

## Phase log

- Phase 0 initial state: local `main` and `origin/main` both at `4fe0fb58dcd32691d0fe9ebe8a37f7fb70374e95`; latest CI passed in run `26112396272`; scoring, CPU batch, Stage 3C calibration summary, and CUDA parity contract inputs are present; no raw or generated files are staged.
- Phase 1 directories: confirmed `data/scoring/` exists for committed scoring policy records; created local ignored `experiments/results/scoring-consolidation/stage4i/` output area; generated outputs remain covered by the repository result-output ignore policy.
- Phase 2 schemas: added scorer, score-summary, confidence-label, compatibility-map, calibration-profile, and calibration-report schemas. They require `solve_claim=false`, `trusted_as_canonical=false`, and `cuda_used=false`, and keep confidence labels in a finite closed set that cannot imply solved plaintext.
- Phase 3 implementation: added `libreprimus.scoring_consolidation` with scorer inventory, confidence-label records, legacy compatibility mapping, Stage 3C calibration-profile extraction, calibration-report building from method ledgers, CPU batch score-summary compatibility, export, summary, and validation helpers. CPU batch scoring now carries Stage 4I scorer/profile metadata while preserving legacy label information.
- Phase 4 CLI: added `libreprimus scoring` commands for consolidation, validation, report output, and CPU batch compatibility checks.
- Phase 5 local run: ran `libreprimus scoring consolidate`, validation, report, and CPU batch compatibility checks. The run wrote 3 scorer records, 9 confidence-label records, 11 compatibility mappings, 1 calibration profile, and 1 calibration report; positive/null/negative controls are available; CPU batch compatibility is true; generated outputs remain ignored.
- Phase 6 tests: added Stage 4I schema, confidence-label, scorer-inventory, compatibility-map, calibration-profile, CPU-batch scoring compatibility, CLI, and ignore-policy tests. Focused Stage 4I tests passed (`14 passed`) and Ruff passed on the new package, CLI, and tests.
- Phase 7 research synthesis: updated the staged plan, stage summaries, method-family status, method-retirement ledgers, research-synthesis validation guardrails, and state-drift checks for Stage 4I complete and Stage 4J next. CUDA remains deferred and now depends on CPU batch plus scoring parity contracts.
- Phase 8 documentation: added scoring contract, calibration report, confidence-label, score-record policy, scoring/CUDA parity, Stage 4I experiment/research, and scoring CLI docs; updated STATUS, ROADMAP, README, AGENTS, CUDA notes, experiment/schema/testing/catalog docs, architecture/onboarding docs, tutorials, and wiki-source.
- Phase 9 consistency integration: updated PowerShell and POSIX consistency runners to perform Stage 4I scoring consolidation in a temporary directory, validate committed scoring records, and check CPU batch score compatibility without requiring raw data.
- Phase 10 validation: scoring validation passed with 3 scorer records, 9 confidence labels, 11 compatibility mappings, 1 calibration profile, and 1 calibration report; CPU batch compatibility is true. Research synthesis, state drift, consistency, smoke, Ruff, full pytest (`1008 passed`), public docs, lock hashes, workflow static checks, wiki-source validation, and wiki dry-run sync all passed. Generated scoring consolidation outputs and raw paths remain unstaged.
