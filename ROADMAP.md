# Roadmap

## Phase 0A - Project bootstrap

Create repository structure, documentation, toolchain scripts, C++ smoke build, optional CUDA smoke build, Python package, and smoke tests.

## Phase 0B - Source mirroring and corpus locks

Mirror source archives, pin SHA-256 locks, define canonical transcript/versioning policy, and freeze Gematria profile metadata without cryptanalysis.

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
