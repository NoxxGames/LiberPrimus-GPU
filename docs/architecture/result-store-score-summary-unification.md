# Result Store Score Summary Unification

Stage 4P adds a read-only reporting layer over existing result surfaces. It inventories committed summaries and optional ignored generated outputs, normalizes result-like records into a stable shape, maps score views through the Stage 4I score-summary contract, and joins results to method-family and retirement state.

This is infrastructure only. It does not run experiments, import raw data, add a scorer, recalibrate labels, publish generated result bodies, implement CUDA, activate the canonical corpus, finalize page boundaries, or make solve claims.

## Inputs

Stage 4P prefers committed aggregate summaries under `data/research/`, `data/observations/`, and `data/scoring/`. Optional generated outputs under `experiments/results/` are read only when they already exist locally. Missing optional outputs are explicit inventory records with `optional_generated_missing`, not failures.

Raw-required sources are skipped with `skipped_raw_required`. The inventory does not read raw Discord logs, raw LP page images, raw stego/audio artefacts, third-party caches, SQLite databases, or local reports.

## Contracts

Unified result records keep these policy flags false:

- `solve_claim`
- `cuda_used`
- `canonical_corpus_active`
- `page_boundaries_final`
- `generated_outputs_committed`
- `raw_data_processed`
- `new_experiment_executed`
- `new_scorer_added`

Unified score-summary records use the Stage 4I finite confidence-label vocabulary. Unknown score semantics become `scoring_not_available` with a warning instead of a new label.

## Outputs

Generated records live under `experiments/results/result-store-unification/stage4p/` and remain ignored. The committed aggregate summary is `data/research/stage4p-result-store-score-summary-unification-summary.yaml`.

