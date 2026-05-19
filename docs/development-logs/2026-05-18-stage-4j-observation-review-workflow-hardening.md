# Stage 4J observation review workflow hardening

Date: 2026-05-18

## Scope

Stage 4J hardens observation review, promotion gates, quarantine policy,
documentation freshness, and local-path sanitisation. It does not run
experiments, process raw data, use CUDA, activate the canonical corpus, finalize
page boundaries, or make solve claims.

## Phase log

- Phase 0 initial state: local `main` and `origin/main` both at `05849075dacc9c0aad4a95cb9d46abda6404e2ef`; latest CI passed in run `26115239182`; Stage 4I scoring records and observation records are present. Stale text was found in README and source-of-truth docs, and absolute local paths were found in the Stage 4G cookie refresh summary.
- Phase 1 directories: created `data/observations/review/` and local ignored `experiments/results/observation-review/stage4j/`; generated outputs remain covered by the repository result-output ignore policy.
- Phase 2 schemas: added observation review state, decision, promotion, quarantine, summary, and policy schemas. They require no-solve and noncanonical defaults, and keep seed promotion behind explicit review/promotion gates.
- Phase 3 implementation: added `libreprimus.observation_review` with committed-record loaders, review-state helpers, decision builder, promotion gates, quarantine records, path sanitisation, export, summary, and validation helpers.
- Phase 4 CLI: added `libreprimus observation-review` commands for build, validate, summary, and path checks.
- Phase 5 local run: built 96 review decisions, 96 promotion gate records, 23 quarantine records, and a committed summary. The run accepted 20 source references as metadata, rejected 1 cookie exact-pack result, deferred 13 items, quarantined 6 items, preserved 17 negative-control decisions, and promoted 0 items to manifests.
- Phase 6 tests: added Stage 4J schema, state-machine, promotion-gate, quarantine, path-sanitisation, doc-freshness, CLI, and ignore-policy tests. Focused Stage 4J pytest passed with 18 tests.
- Phase 7 research synthesis: updated the staged plan, stage summary records, method-family status, and method-retirement ledger. Stage 4J is complete, observation review is infrastructure, CUDA remains deferred, and Stage 4K allowlisted public source-lock snapshots is next.
- Phase 8 documentation: added observation review workflow, state-machine, promotion policy, negative-control policy, path-sanitisation, research, and CLI docs. Updated operational docs, scoring/visual policy docs, tutorials, and Wiki-source mirrors.
- Phase 9 consistency: added observation-review validation and path checks to both CI consistency scripts and extended state-drift checks for Stage 4J/4K freshness plus unsafe absolute local path detection.
- Phase 10 validation: observation-review validation, path sanitisation, research-synthesis validation, state-drift, full consistency, smoke, ruff, pytest, CI consistency scripts, public-docs status, lock hashes, workflow static checks, Wiki validation, and Wiki dry-run sync passed locally. Full pytest reported 1026 passed.
- Phase 11 GitHub issue: created issue 55, `Stage 4J: observation review workflow hardening`, and added a pre-push validation summary comment.
