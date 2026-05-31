# Stage 5CG Approval-Gate Decision Scaffold

Stage 5CG integrates the Stage 5CF Deep Research review outcome as compact metadata and creates future decision-record scaffolds without satisfying approvals.

Implemented:

- Added `python/libreprimus/token_block/stage5cg.py` for Stage 5CG record/schema generation, focused validators, aggregate validation, and summary loading.
- Added `libreprimus token-block` commands for `build-stage5cg`, focused Stage 5CG validators, `validate-stage5cg`, and `stage5cg-summary`.
- Created compact Stage 5CG records under `data/project-state/`, `data/token-block/`, `data/historical-route/`, and `data/source-harvester/`.
- Created Stage 5CG schemas under `schemas/project-state/`, `schemas/token-block/`, `schemas/historical-route/`, and `schemas/source-harvester/`.
- Added tests for schemas, CLI commands, operator/Deep Research decision scaffolds, combined approval-gate closure, Stage 5CE wording review, no-byte/no-execution gates, Stage 5BD preservation, active-lineage preservation, reviewability, and ignore policy.

Guardrails:

- Metadata only.
- Operator approval and Deep Research activation acceptance remain absent and unsatisfied.
- Stage 5CE proposal/gate design is preserved; the Stage 5CE wording warning is reviewed and not reproduced in the current committed record.
- No active planning input authorization, String 4 activation, dry-run ingestion, byte-stream generation, manifest supersession, token execution, DWH/hash search, decoding, scoring, CUDA, benchmarks, website expansion, method-status upgrade, canonical-corpus activation, page-boundary finalisation, or solve claim.
- `codex-output/` is the only local Codex handoff root; `codex_output/` remains unused.

Local validation:

- Stage 5CG focused validators: passed.
- Stage 5AX parallel validation wrapper: passed with 16 workers and 16 pytest workers; `pytest-xdist` was available locally.
- WSL/bash wrappers: not run because local `bash.exe` resolves to the WSL launcher and no WSL distributions are installed.
- Research synthesis, state drift, document staleness, Stage 5AH stage-ledger coverage, consistency `check-all`, smoke, ruff, public-doc status, lock hashes, workflow static validation, wiki-source validation, and wiki dry-run sync: passed.
- Full pytest: 2282 passed.
- Serial `scripts/ci/run-consistency-checks.ps1`: passed after Stage 5CG stage-ledger updates.

CI verification remains external until the Stage 5CG commit is pushed.
