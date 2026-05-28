# Stage 5BJ Original-Archive Crosswalk Closure

Implemented Stage 5BJ as a conservative metadata-only closure layer over Stage 5BI crosswalk candidates.

Work completed:

- Added `libreprimus historical-route stage5bj-build`, `stage5bj-validate`, and `stage5bj-summary`.
- Added Stage 5BJ schemas for crosswalk closure, exact 2014 surface source locks, Fandom page-body crosswalks, boards-thread crosswalk, high-priority candidate status, media equivalence, source-gap updates, token-block lineage preservation, local archive inspection, source snapshot inspection, summary, and next-stage decision.
- Generated committed YAML metadata under `data/historical-route/`, `data/token-block/`, `data/source-harvester/`, and `data/project-state/`.
- Wrote local ignored generated reports and extracted-surface bodies under `experiments/results/historical-route/stage5bj/`.
- Added ignored local completion summaries under `codex_output/stage5bj-completion-summary.md` and `codex-output/stage5bj-completion-summary.md`.
- Added tests for schemas, crosswalk closure, exact surfaces, page-body and boards gaps, media policy, token-block lineage, source-gap updates, guardrails, summary, CLI, and completion-summary ignore policy.

Local results:

- Stage 5BI crosswalk candidates consumed: 12.
- Stage 5BJ closure rows: 12.
- Exact 2014 surface targets: 3.
- Exact 512-hex surfaces locked: 3.
- Surface source files found: 3.
- Page-body crosswalk rows: 7.
- Boards thread found: true.
- Media-equivalence rows: 8.
- Source gaps closed/carried/new: 4 / 3 / 2.

Validation:

- `libreprimus historical-route stage5bj-validate`: passed.
- `libreprimus historical-route stage5bj-summary`: passed.
- `libreprimus historical-route stage5bi-validate`: passed.
- `libreprimus historical-route validate-stage5bf`: passed.
- `libreprimus token-block validate-stage5bd`: passed.
- `python -m pytest -q tests/python`: 2012 passed.
- `ruff check python/libreprimus tests/python`: passed.
- `scripts/ci/run-consistency-checks.ps1`: passed.
- `scripts/ci/run-consistency-checks.sh`: passed through Git Bash with repo venv Python and a temp root outside the repository.
- Public docs status, lock hashes, workflow static validation, wiki source validation, and wiki dry run: passed.

Validation fixes made:

- Updated the consistency wrappers so Stage 5S temp integration validates against committed passed Stage 5R parity metadata rather than a synthetic skipped-CUDA Stage 5R temp record.
- Fixed the bash wrapper Stage 5AL temp variable typo.
- Relaxed Stage 5AM temp summary upload-instruction detection to compare against the rendered manifest root instead of the default repo-relative export root, preserving committed default behavior while allowing temp validation.

Guardrails:

- No token-block execution was performed.
- No real token-block byte streams were generated.
- No 2014 surfaces were combined with page 49-51.
- No DWH/hash/preimage search was performed.
- No decode attempt was performed.
- No stego/audio/image/OCR/AI/CUDA/benchmark/scoring work was performed.
- No raw Fandom/archive/spreadsheet files were committed.
- No full extracted 2014 surface bodies were committed.
- No solve claim was made.

Next selected stage: Stage 5BK - Historical-route planning constraint integration, without execution.
