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
