# Stage 4H CPU batch transform API

Date: 2026-05-18

## Scope

Stage 4H extracts a CPU-only batch transform API as the future CUDA parity contract. It must preserve existing transform semantics, use synthetic or solved-baseline-safe inputs, keep generated outputs ignored, and make no solve claim, CUDA change, canonical corpus activation, or page-boundary finalization.

## Phase log

- Phase 0 initial state: local `main` and `origin/main` both at `b8929e3ff0618cad42d3773e884027565ec96f26`; latest CI passed in run `26108651366`; transform registry, solved-baseline runner, scoring package, and bounded execution package are present; raw/generated files are not staged.
- Phase 1 output policy: created local `experiments/results/cpu-batch/stage4h/` output area and confirmed the existing generated-output ignore policy covers CPU batch outputs. Raw data and third-party cache ignores remain active.
- Phase 2 schemas: added CPU batch manifest, input stream, transform candidate, result record, run summary, and CPU/CUDA parity contract schemas. The schemas require CPU-only execution, `cuda_used=false`, `no_solve_claim=true`, inactive canonical corpus, reviewable page boundaries, and uncommitted generated outputs.
- Phase 3 implementation: added `libreprimus.cpu_batch` with normalized input streams, manifest loading, registry/local transform adapters, deterministic batch runner, minimal-triage scoring adapter, parity contract record, generated-output export, committed summary export, and validation.
- Phase 4 manifests/CLI: added Stage 4H synthetic smoke, solved-baseline-style parity, and adapter-coverage manifests plus the `libreprimus cpu-batch` command group with manifest validation, run, adapter coverage, result validation, and summary commands.
- Phase 5 local run: executed the synthetic smoke batch and adapter coverage locally. It ran 6 candidates, supported 6 registry adapters, produced 6 result records, scored 6 outputs, and wrote generated outputs under ignored `experiments/results/cpu-batch/stage4h/`.
- Phase 6 tests: added Stage 4H schema, input-stream, transform-adapter, batch-runner, scoring-adapter, parity-contract, CLI, and ignore-policy tests. Focused Stage 4H tests passed and Ruff passed on the new package/tests.
- Phase 7 research synthesis: updated staged plan, stage summary records, method-family status, method-retirement records, state-drift guardrails, and research-synthesis validation for Stage 4H complete and Stage 4I next.
- Phase 8 documentation: added CPU batch architecture, CUDA parity contract, Stage 4H experiment/research, and CLI reference docs; updated STATUS, ROADMAP, README, AGENTS, CUDA notes, experiment/schema/testing/catalog docs, tutorials, wiki-source, and private/generated data map.
- Phase 9 consistency integration: added CPU batch manifest/run/adapter-coverage/result-validation checks to both PowerShell and Bash consistency scripts.
- Phase 10 validation: CPU batch manifest and result validation passed; research-synthesis validation passed; state-drift and full consistency checks passed; smoke, Ruff, and pytest passed (`994 passed`); public-doc, lock-hash, workflow-static, wiki-source, and wiki dry-run checks passed. Git safety checks confirmed generated outputs and raw paths were not staged.
- Phase 12 GitHub issue: created issue #53, `Stage 4H: CPU batch transform API`, with the pre-push validation summary.
