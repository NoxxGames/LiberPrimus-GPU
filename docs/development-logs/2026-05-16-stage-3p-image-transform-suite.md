# Stage 3P Image Transform Suite Development Log

Date: 2026-05-16

## Scope

Stage 3P adds deterministic local image-transform tooling for Liber Primus page depictions. It generates derived review images, contact sheets, metrics, candidate review flags, and a local visual review index under ignored paths.

The stage does not use OCR, AI/ML image interpretation, OpenCV, CUDA, Discord processing, image-derived cipher execution, canonical corpus activation, page-boundary finalization, or solve claims.

## Phase 0 Initial State

- Branch: `main`
- Local HEAD: `5b9acb9bb4d21d6310fc703e331868f785e08870`
- `origin/main`: `5b9acb9bb4d21d6310fc703e331868f785e08870`
- Latest CI: success, run `26008267051`
- Stage 3M image analysis package: present
- Stage 3K image locks: present
- Local page image count: `58`
- Discord logs present but untouched: true
- Tutorials and Wiki source: present
- Pillow available: true
- Generated outputs staged: `0`
- Raw images staged: `0`
- Raw Discord logs staged: `0`

## Phase 1 Output And Ignore Policy

- Added ignored output area under `experiments/results/image-transforms/stage3p/`.
- Added contact sheet, review page, and derived image subdirectories.
- Preserved raw page-image and Discord-log ignore rules.

## Phase 2 Schemas

- Added image transform, metric, candidate, contact sheet, and run summary schemas.
- Schema flags require `trusted_as_canonical=false`, `usable_as_experiment_seed=false` where applicable, and `solve_claim=false`.
- Output path schema patterns constrain generated records to `experiments/results/image-transforms/stage3p/`.

## Phase 3 Implementation

- Added `python/libreprimus/image_transforms/`.
- Implemented grayscale, invert, autocontrast, posterize, threshold, channel, bitplane, edge, split/mirror, 180-difference, component-overlay, contact-sheet, review-index, and candidate-flag generation.
- Candidate flags remain review aids only and cannot become experiment seeds automatically.
- No OCR, AI/ML, OpenCV, CUDA, Discord processing, or cipher execution was introduced.

## Phase 4 CLI

- Added `libreprimus image-transform run-local-pages`.
- Added `libreprimus image-transform validate-results`.
- Added `libreprimus image-transform summary`.
- `--allow-missing` supports raw-image-free CI operation.

## Phase 5 Consistency Integration

- Added Stage 3P consistency checks.
- Updated ignored-output policy checks with generated transform paths.
- Updated CI consistency scripts to validate the raw-image-free Stage 3P mode.
- Preserved Stage 3O Wiki validation in the consistency path.

## Phase 6 Local Run

- Executed `libreprimus image-transform run-local-pages` against `58` ignored local page images.
- Generated `2077` derived review images, `59` contact sheets, `58` review pages, and `6` visual transform candidates.
- Review index path: `experiments/results/image-transforms/stage3p/review_index.html`.
- Generated outputs remained ignored and unstaged.

## Phase 7 Tests

- Added Stage 3P tests for schemas, transforms, channel splits, bitplanes, edge maps, split/mirror metrics, component overlays, contact sheets, review index generation, candidate flags, CLI commands, and ignore policy.
- Focused Stage 3P pytest run passed: `17 passed`.
- Ruff passed for the new package, CLI, consistency updates, and Stage 3P tests.

## Phase 8 Docs Tutorial Wiki

- Added Stage 3P docs under `docs/forensics/`, `docs/visual/`, `docs/research/`, and `docs/reference/`.
- Updated README, STATUS, ROADMAP, EXPERIMENTS, RESULTS_SCHEMA, TESTING, AGENTS, CIPHER_CATALOG, and tutorials.
- Regenerated and validated `docs/wiki-source/` from tutorials.
- Reinforced that Stage 3P outputs are review aids only and no solve claim is made.
