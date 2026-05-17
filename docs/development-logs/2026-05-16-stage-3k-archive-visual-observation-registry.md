# Stage 3K Archive Visual Observation Registry Developer Log

Date: 2026-05-16

## Scope

Stage 3K creates source/archive, local image lock, visual numeric observation, and cookie/hash registries. It does not execute image-derived text experiments, run live Tor crawling, use OCR or AI image interpretation as source truth, use CUDA, activate a canonical corpus, finalize page boundaries, or claim a solve.

## Initial State

- Starting commit: `a8121280b0c560ec4e4221c0ea529ad670e83341`
- Latest prior CI: success, run `25999489778`
- Root archive/image research report present locally and copied into `docs/research/` with a non-solution research-input note.
- Local page image directory present at `third_party/LiberPrimusPages/`.
- Raw page images remain ignored and uncommitted.

## Changes

- Added Stage 3K schemas under `schemas/history/` and `schemas/visual/`.
- Added source/archive records, visual numeric observation records, cookie/hash records, and local image lock/artifact outputs.
- Added stdlib PNG/JPEG metadata extraction and prime-dimension checks.
- Added `libreprimus archive` and `libreprimus observation` CLI groups.
- Added raw-image-free consistency checks and CI script hooks.
- Added tests and public documentation updates.

## Local Registry Run

- Source records: `12`
- Local images scanned: `58`
- Image lock records: `58`
- Image artifact records: `58`
- Prime-dimension image count: `0`
- Visual observations: `5`
- Cookie/hash records: `2`

## Safety

- Raw local page images remain ignored under `third_party/LiberPrimusPages/`.
- Generated scan summaries remain ignored under `experiments/results/archive-visual-registry/stage3k/`.
- Visual observations remain `usable_as_experiment_seed=false`.
- All records remain `trusted_as_canonical=false`.
- No solve claim.
