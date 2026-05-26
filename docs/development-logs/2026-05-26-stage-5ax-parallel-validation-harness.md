# Stage 5AX Parallel Validation Harness

Stage 5AX inserted local validation-speed infrastructure before bounded token-block preflight design.

Implemented `python/libreprimus/parallel_validation/` with command models, plan generation, pytest-xdist detection, deterministic sharded fallback, subprocess execution, scheduler safety checks, result aggregation, Stage 5AX summary generation, and record validation.

Added the `libreprimus parallel-validation` CLI with `build-stage5ax-plan`, `run-stage5ax-pytest`, `run-stage5ax-parallel-validation`, `build-stage5ax-summary`, `validate-stage5ax`, and `summary`.

Created Stage 5AX CI/project-state schemas and compact records under `data/ci/` and `data/project-state/`. Generated logs and JSON/JSONL reports remain ignored under `experiments/results/ci/parallel-validation/stage5ax/`.

Added opt-in PowerShell and shell wrappers under `scripts/ci/`. Existing serial CI remains the conservative default; the new harness is for local fast validation unless a later stage explicitly changes CI policy.

Local run summary: 10 parallel-safe commands, 6 serial commands, 1 blocked command, 16 requested/used validation workers, 16 requested/used pytest workers, pytest mode `shard`, xdist unavailable locally, shard fallback used, and 0 failed commands.

Guardrails preserved: no token experiments, variant byte streams, DWH/hash search, decode attempt, OCR, AI/ML interpretation, LLM/vision token reading, semantic image interpretation, hidden-content image forensics, stego, CUDA execution/source modification, cryptanalytic benchmark, scored experiment, generated-output commit, method-status upgrade, canonical-corpus activation, page-boundary finalisation, or solve claim.

Stage 5AW selected bounded token-block preflight as Stage 5AX, but the user inserted validation infrastructure first. The selected next stage is Stage 5AY - bounded token-block preflight manifest design without execution.

Validation status:

- Stage 5AX parallel validation records validate with 10 parallel-safe commands, 6 serial commands, and 1 blocked command.
- Local Stage 5AX parallel run passed with 16 validation workers, 16 pytest workers, pytest mode `shard`, xdist unavailable, sharded fallback used, 870 pytest files, and 0 failed commands.
- Full serial pytest passed: 1862 tests.
- Ruff, smoke, state-drift, consistency, token-block Stage 5AW validation, strict doc-staleness, path sanitisation, research synthesis, public-doc status, lock hashes, workflow static validation, wiki-source validation, and tutorial wiki dry-run passed.
- `scripts/ci/run-parallel-validation.ps1` passed. Shell wrapper validation was skipped because local `bash` resolves to WSL and no WSL distribution is installed.
