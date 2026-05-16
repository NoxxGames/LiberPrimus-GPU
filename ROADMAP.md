# Roadmap

## Phase 0A - Project bootstrap

Create repository structure, documentation, toolchain scripts, C++ smoke build, optional CUDA smoke build, Python package, and smoke tests.

## Phase 0B - Source mirroring and corpus locks

Mirror source archives, pin SHA-256 locks, define canonical transcript/versioning policy, and freeze Gematria profile metadata without cryptanalysis.

Stage 0B legacy workbook ingestion is completed as a separate non-canonical legacy-source step. Canonical corpus mirroring remains future work.

## Phase 0C - Source archive mirroring, transcript locks, and Gematria profile freeze

Mirror primary source archives, pin SHA-256 locks, define canonical transcript/versioning policy, and freeze Gematria profile metadata without implementing unsolved-page cryptanalysis.

Stage 0C local legacy Pastebin ingestion is completed as a separate non-canonical legacy-source step.

## Phase 0D - Align legacy Pastebin line-pairs

Align legacy Pastebin line-pairs with primary transcript/page-image sources and infer tentative page boundaries with confidence labels.

Stage 0D transcript alignment and policy scaffolding is completed, with significant unmatched regions documented.

## Phase 0D-P - Public docs, wiki, and issue bootstrap

Add public tutorials, GitHub issue templates, issue seeds, wiki source pages, project-management scripts, and push workflow documentation.

## Phase 0D-followup - Resolve transcript-alignment gaps

Resolve transcript-alignment gaps, ambiguous page-boundary candidates, and glyph-variant evidence before corpus freeze.

Stage 0D-followup added transcript views, bounded stream-subsequence matching, gap diagnostics, and boundary confidence auditing. It reduced real-source no-match records from `153` to `2`, but two low-confidence records and boundary overgeneration still require human review.

## Phase 0D-followup-2 - Inspect remaining unmatched spans, if needed

If the remaining ambiguous records block corpus policy work, manually inspect unmatched spans, compare alternate transcript segmentation, and decide whether rtkd logical views or Pastebin source structure should drive LP2 alignment.

## Phase 0E - Freeze Gematria profile and separator grammar

Freeze Gematria profile and separator grammar, then create canonical corpus v0 candidate records with page-boundary candidates preserved as non-final metadata.

Stage 0E generated frozen Gematria, separator, and glyph variant profiles plus an inactive rtkd master v0 corpus candidate.

## Phase 1A - Solved-page golden fixture framework

Implement solved-page golden fixture framework and reproduce direct-translation solved pages using Stage 0E profiles and corpus candidate records. Do not add brute-force search.

Stage 1A added direct-translation solved fixtures for four known direct sections and a reproduction CLI. Generated solved-baseline outputs remain ignored.

## Phase 1B - Reverse Gematria / Atbash-family reproduction

Reproduce clearly documented reverse Gematria or Atbash-family solved pages using the Stage 1A fixture framework. Do not add brute-force search.

Stage 1B added reverse Gematria and rotated reverse Gematria known-solved fixtures. The direct fixture regression still passes.

## Phase 1C - Explicit-key Vigenere solved-page reproduction

Reproduce documented Vigenere solved pages with explicit locked-source keys and skip rules only where the locked references support them. Do not add key search.

Stage 1C added reference-source locks and explicit-key Vigenere solved fixtures for `DIVINITY` and `FIRFUMFERENFE`. Direct and Atbash-family regressions still pass. No key search was added.

## Phase 1D - p56 prime-minus-one / phi-prime reproduction

Reproduce p56 An End only if locked references and fixture spans support the prime-minus-one / phi-prime method. Preserve payload checks and do not add search.

Stage 1D added a p56 prime-minus-one known-solved fixture with a passing payload hash check. Direct, Atbash-family, and Vigenere regressions still pass. No prime-stream search was added.

## Phase 2A - CPU transform registry foundation

Register solved-baseline CPU reference transforms for manifest-addressable runs: direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, and prime-minus-one. Do not start search campaigns yet.

Stage 2A added `cpu-reference-transforms-v0`, registry dispatch, solved-baseline run manifests, and an all-known solved-baseline runner with 10 passing known fixtures. Search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

## Phase 2B - Experiment result store and run-record foundation

Add durable JSONL/SQLite result sinks, run-record schemas, manifest provenance, solved-baseline result import, and validation before unsolved-page search campaigns begin.

Stage 2B added result-store schemas, JSONL and SQLite sinks, provenance capture, a solved-baseline import manifest, result-store CLI commands, and generated result-store validation. It imports the Stage 2A all-known solved-baseline run with pass/fail/pending/skipped `10/0/0/0`. Search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

## Phase 2C - CI and safe experiment scaffolding

Add GitHub Actions CI for Python tests, ruff, schema validation, and CPU-only smoke commands, or add bounded CPU experiment-manifest scaffolding only after result-store validation. Do not jump directly to CUDA or unsolved-page search.

Stage 2C added GitHub Actions CI and local CI reproduction scripts. The workflow runs raw-data-free Python checks, schema/manifest validation, and a CPU-only CMake smoke job with CUDA disabled. It does not upload generated artifacts or run search/scoring.

Stage 2C-followup hardened the workflow with readable multi-line YAML, static YAML structure checks, and local workflow validation scripts.

Stage 2C-followup-2 added post-push raw GitHub workflow verification scripts and `gh` PATH troubleshooting while keeping the workflow raw-data-free, CUDA-free, secret-free, and artifact-upload-free by default.

Stage 2C-followup-3 repaired Git attributes, normalized canonical profile/registry JSON locks to LF bytes, and added lock-hash verification to prevent Windows/Linux SHA drift.

Stage 2C-followup-4 updated public README/STATUS/ROADMAP status text and added CI-covered tests to prevent stale top-level public status and next-milestone drift.

Stage 2C-followup-5 added remote Git blob verification for the CI workflow and `.gitattributes`, documenting that fetched Git blobs and GitHub API contents outrank potentially cached raw URL views.

## Stage 2D - CI-gated schema and docs hardening

Add schema/docs consistency checks and harden manifest/result-store validation before first bounded CPU exploratory experiment scaffolding.

Stage 2D added a raw-data-free consistency package, CLI commands, CI scripts, workflow gates, and tests covering registry, manifest, schema, docs, ignored-output, and result-store consistency.

## Stage 2E - CPU experiment manifest scaffold and dry-run planner

Design CPU exploratory experiment manifests and a dry-run planner for bounded baseline transforms without executing unsolved-page search campaigns.

## Phase 1 - Corpus and known-solution reproduction

Load locked corpus data and reproduce known solved-page behavior before new search work.

## Phase 2 - CPU cryptanalysis workbench

Implement CPU reference transforms, scorers, manifest runner, result sink, and null controls.

## Phase 3 - GPU prototype

Add CUDA kernels only for tested CPU reference transforms and prove parity.

## Phase 4 - Full experiment engine

Support branching search, structured result review, resumable runs, and manifest determinism.

## Phase 5 - Serious search campaigns

Run bounded, reviewed campaigns with pinned data and clear stop conditions.

## Phase 6 - Advanced methods

Evaluate statistical, language-model-assisted, or search-prior methods only after baseline controls exist.

## Phase 7 - Publication and reproducibility

Prepare reproducible reports, source citations, data locks, and review notes.
