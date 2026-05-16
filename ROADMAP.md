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

## Phase 0D-followup - Resolve transcript-alignment gaps

Resolve transcript-alignment gaps, ambiguous page-boundary candidates, and glyph-variant evidence before corpus freeze.

## Phase 0E - Freeze Gematria profile and separator grammar

Freeze Gematria profile and separator grammar, then create canonical corpus v0 candidate records with page-boundary candidates preserved as non-final metadata.

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
