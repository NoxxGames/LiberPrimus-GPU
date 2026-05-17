# Results Schema

## Purpose

Define planned result records before generated outputs exist.

## Stage 0A status

The result schema is planned, not finalized. Stage 0B implements legacy workbook extraction record shapes for non-canonical generated artefacts.

## Result record principles

Records must be replayable, reviewable, compact, and explicit about uncertainty.

## Planned JSONL fields

Planned fields include result ID, experiment ID, manifest hash, corpus lock ID, transform chain, candidate summary, scores, null-control scores, rank, timestamps, and review status.

Implemented legacy workbook record types:

- `legacy_workbook_sheet`
- `legacy_solved_delta`
- `legacy_prime_sum`
- `legacy_workbook_formula`
- `legacy_workbook_summary`
- `legacy_pastebin_line_pair`
- `legacy_pastebin_anchor`
- `legacy_pastebin_summary`
- `transcript_line`
- `scream314_reference_record`
- `pastebin_transcript_alignment`
- `lp2_page_boundary_candidate`
- `glyph_variant_observation`
- `stage0d_alignment_summary`

## Planned SQLite tables

Planned tables include experiments, runs, corpus_locks, transform_steps, scores, candidates, null_controls, hardware, and reviews.

## Required provenance fields

Required provenance will include git commit, manifest path and hash, tool versions, corpus locks, Gematria profile, transcript profile, random seed, and command line.

## Score breakdown fields

Scores should include component names, raw values, normalized values, weights, null-control distributions, and threshold notes.

## Hardware metadata

Hardware metadata should include CPU, RAM, GPU, driver, CUDA toolkit, compiler, OS, and relevant build flags.

## Reproducibility metadata

Reproducibility metadata should include run ID, timestamps, environment summary, deterministic seed, output schema version, and source data hashes.

## False-positive warnings

Every candidate record must be treated as unverified until rerun, compared to controls, and manually reviewed.

Workbook-derived records must include `trusted_as_canonical=false` and must not be treated as source truth.

Pastebin-derived records must include `source_id`, `source_sha256`, `source_local_filename`, and `trusted_as_canonical=false`.

Alignment-derived records must include source IDs, source SHA-256 hashes, confidence labels, and `trusted_as_canonical=false`. Boundary candidates must include `canonical_page_boundary=false`.

Public tutorials must not present generated results as evidence unless they are manifest-backed, provenance-complete, and explicitly reviewed. Stage 0D-P examples are smoke outputs only.

## Stage 0D-followup Record Types

Implemented/generated Stage 0D-followup record types include:

- `transcript_view_record`
- `alignment_gap_diagnostic`
- `page_boundary_confidence_audit`
- `stage0d_followup_alignment_summary`

These are diagnostic records only. They must include source hashes, confidence or reason labels where applicable, and non-canonical flags. Generated JSON/JSONL outputs under `data/normalized/alignment/` remain ignored.

## Stage 0E Corpus Schemas

Stage 0E adds schemas under `schemas/corpus/` for:

- `gematria-profile-v0`
- `glyph-variant-profile-v0`
- `separator-grammar-v0`
- `corpus_candidate_manifest`
- `corpus_token`
- `corpus_line`
- `corpus_page_candidate`
- `corpus_generation_warning`

Generated manifest and page records require `canonical_corpus_active=false`, `page_boundaries_final=false`, `canonical_page_boundary=false`, and `trusted_as_canonical=false` where applicable.

## Stage 1A Solved Fixture Schemas

Stage 1A adds schemas under `schemas/corpus/` for:

- `solved-page-fixture-v0` (`solved_page_fixture`)
- `solved_page_reproduction_record`
- `solved_page_reproduction_summary`

Fixture and reproduction records require provenance hashes and keep `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.
## Stage 1B Solved-Fixture Results

Stage 1B extends solved-page reproduction records with:

- `decoded_index_formula`
- `transform_parameters`
- `method_family=reverse_gematria`
- `method_family=rotated_reverse_gematria`

All reproduction records must keep `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`. Atbash-family generated outputs are stored under ignored solved-baseline directories and must not be committed.
## Stage 1C Reference And Vigenere Records

Stage 1C adds generated reference summary records:

- `reference_method_note`
- `tooling_reference_note`
- `stage1c_reference_source_summary`

Stage 1C also extends `solved_page_reproduction_record` with Vigenere-specific fields:

- `key_text`
- `key_indices`
- `skip_rule_applied_count`

All reproduction records continue to require `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Stage 1D Prime-Stream And Payload Records

Stage 1D extends `solved_page_fixture` records with optional `payload_checks` for fixture-declared payloads.

Stage 1D extends `solved_page_reproduction_record` with:

- `prime_values_used_count`
- `stream_values_used_count`
- `first_prime_values`
- `first_stream_values_mod29`
- `payload_check_results`

All reproduction records continue to require `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Stage 2A Registry And Manifest-Run Records

Stage 2A adds `solved-baseline-run-manifest-v0` for manifest-addressable solved-baseline regression runs.

Solved-fixture reproduction records now include registry metadata:

- `registry_id`
- `registry_sha256`
- `transform_id`
- `canonical_transform_id`
- `search_performed=false`
- `cuda_used=false`
- `scoring_used=false`

Manifest-run outputs include `solved_baseline_manifest_run_record` JSONL and `solved_baseline_manifest_run_summary` JSON. They must keep `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`, and generated files under `experiments/results/solved-baselines/` remain ignored.

## Stage 2B Experiment Result Store Schemas

Stage 2B adds result schemas under `schemas/results/`:

- `experiment-run-record-v0`
- `experiment-run-summary-v0`
- `experiment-event-record-v0`
- `experiment-artifact-record-v0`
- `experiment-result-store-manifest-v0`
- `sqlite-result-store-v0`

Solved-baseline imports require `canonical_corpus_active=false`, `page_boundaries_final=false`, `search_performed=false`, `scoring_used=false`, `cuda_used=false`, and `trusted_as_canonical=false`.

Generated result-store outputs include JSONL records and `results.sqlite3` under `experiments/results/result-store/`. They are ignored and must not be committed.

## Stage 2D Consistency Summary

Stage 2D may generate `consistency_check_suite_result` JSON summaries under `experiments/results/consistency/`. These summaries are generated outputs and are ignored by Git.

## Stage 2E Exploratory Dry-Run Schemas

Stage 2E adds committed schemas under `schemas/experiments/`:

- `exploratory-experiment-manifest-v0`
- `exploratory-dry-run-plan-v0`
- `exploratory-transform-space-v0`
- `exploratory-safety-gate-v0`
- `exploratory-corpus-slice-v0`

Generated `exploratory_dry_run_plan` records are ignored planning outputs under `experiments/results/exploratory-dry-runs/`. They are not candidate result rows and do not contain candidate plaintexts.

## Stage 2F CPU Execution Schemas

Stage 2F adds committed schemas under `schemas/experiments/`:

- `cpu-execution-manifest-v0`
- `cpu-execution-plan-v0`
- `cpu-execution-result-v0`
- `synthetic-corpus-record-v0`
- `execution-safety-gate-v0`

Generated `cpu_execution_plan`, `cpu_execution_result`, and execution summary records are ignored outputs under `experiments/results/cpu-execution/`. They are limited to synthetic and solved-fixture-only execution and require false search, candidate-generation, scoring, CUDA, canonical corpus, page-boundary, and canonical trust flags.

## Stage 2G Proposal And Approval Schemas

Stage 2G adds committed schemas under `schemas/experiments/`:

- `experiment-proposal-v0`
- `experiment-review-packet-v0`
- `experiment-approval-record-v0`
- `experiment-review-checklist-v0`

Generated `experiment_review_packet` records are ignored outputs under `experiments/results/proposal-reviews/`. Approval examples committed in Stage 2G are pending or denied only; no approved approval records are committed.

## Stage 2H Approval-Gated Execution Schemas

Stage 2H adds committed schemas under `schemas/experiments/`:

- `approval-gated-execution-request-v0.schema.json`
- `approval-gated-execution-plan-v0.schema.json`
- `approval-gated-execution-result-v0.schema.json`

Approval-gated execution records bind a proposal, a scope-bound approval record, and an output directory. Stage 2H permits approved execution only for synthetic and solved-control requests. Generated approval execution records are ignored under `experiments/results/approval-gated-execution/`; no approved unsolved-page approval records are committed.

## Stage 2I Approval-Readiness Packet Schema

Stage 2I adds `approval-readiness-packet-v0` under `schemas/experiments/`.

Generated `approval_readiness_packet` records summarize a real exploratory proposal, pending approval status, candidate-count bounds, risk summary, blocking conditions, and the exact human decision still required. They require false approval/execution/search/candidate-generation/scoring/CUDA/canonical flags. These packets are ignored outputs under `experiments/results/approval-readiness/` and are not approvals, execution records, candidate outputs, or solve evidence.

## Stage 2J Bounded Auto-Run Schemas

Stage 2J adds:

- `operator-policy-v0.schema.json`
- `bounded-experiment-queue-v0.schema.json`
- `bounded-experiment-item-v0.schema.json`
- `policy-check-result-v0.schema.json`
- `bounded-auto-run-result-v0.schema.json`

The operator policy records standing limits for local CPU experiments. Queue records list bounded items, policy-check records explain pass/fail/warning outcomes, and generated `bounded_auto_run_result` records summarize execution, deferral, or blocking outcomes.

Generated bounded auto-run records are ignored under `experiments/results/bounded-auto-runs/`. Stage 3A permits `search_performed=true` and `scoring_used=true` only for policy-passing bounded local CPU candidate enumeration summaries. They must keep `cuda_used=false`, `solve_claim_made=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Stage 3A Bounded Candidate And Minimal Scoring Schemas

Stage 3A adds:

- `bounded-candidate-record-v0`
- `bounded-experiment-run-summary-v0`
- `minimal-triage-score-v0`

Generated `bounded_candidate_record` rows are ignored output under `experiments/results/bounded-auto-runs/stage3a/`. They include transform family, transform parameters, candidate index, input slice ID, normalized output text, output hash, minimal score summary, ranking features, and explicit safety flags.

Minimal triage score records are deterministic local CPU scoring summaries. They are sorting metadata only and are not solve evidence.

## Stage 3B Refined Triage And Inspection Outputs

Stage 3B extends `minimal-triage-score-v0` with length-normalized score fields, separator-aware word counts, vowel-band checks, repeated-symbol penalties, tiny impossible-bigram penalties, feature explanations, confidence labels, and `no_solve_claim=true`.

Candidate-inspection and rerank outputs are generated records under `experiments/results/bounded-auto-runs/stage3b/`. They may include reranked top-k JSONL and summary JSON, but those files remain ignored outputs and must not be committed. Committed research logs may include top score metadata and transform parameters only, not full candidate text dumps.

## Stage 3C Scoring Calibration Schemas

Stage 3C adds:

- `scoring-control-record-v0`
- `scoring-calibration-summary-v0`
- `crib-check-result-v0`

Generated calibration records are ignored under `experiments/results/scoring-calibration/stage3c/`. They record positive, null, negative, and candidate score summaries, tiny crib hits, calibrated labels, score ranges, thresholds, and explicit `solve_claim=false` / `cuda_used=false` flags.

## Stage 3D Bounded Vigenere Candidate Records

Stage 3D reuses `bounded-candidate-record-v0` and `bounded-experiment-run-summary-v0` for the small explicit-key Vigenere preview. Candidate records add Stage 3D fields through schema `additionalProperties`:

- `key_text`
- `key_indices`
- `calibrated_confidence_label`
- `crib_hits`
- `crib_hit_count`
- `calibration_position`

Generated records remain ignored under `experiments/results/bounded-auto-runs/stage3d/`. They must keep `cuda_used=false`, `solve_claim=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Stage 3E Method Backlog And Dry-Run Records

Stage 3E adds committed experiment schemas:

- `method-backlog-v0`
- `method-backlog-item-v0`
- `stage3e-queue-item-v0`

The method backlog records evidence basis, exact parameters, candidate-count estimates, implementation status, required controls, and generated-output policy for bounded future methods. Stage 3E queue items require `cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

Generated `stage3e_queue_dry_run_summary` records are ignored under `experiments/results/bounded-auto-runs/stage3e/`. They record declared and calculated candidate counts, policy status, executor-support status, deferred reasons, and `executed_count=0` for this ingestion stage. They are not candidate outputs or solve evidence.

## Stage 3F Vigenere Key-Pack Records

Stage 3F reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the LP evidence-key Vigenere pack. Candidate records include:

- `transform_family=vigenere_key_pack`
- `transform_id=vigenere_explicit_key`
- `key_text`
- `key_indices`
- `transform_parameters.reset_mode`
- `transform_parameters.advance_mode`
- calibrated score fields and crib hits
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3F summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `key_count`, `reset_modes`, `advance_modes`, and `confidence_distribution`.

Generated Stage 3F files remain ignored under `experiments/results/bounded-auto-runs/stage3f/`. They are candidate leads only and not solve evidence.

## Stage 3G Prime Offset Sweep Records

Stage 3G reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the p56-local prime-minus-one offset sweep. Candidate records include:

- `transform_family=prime_stream_offset_sweep`
- `transform_id=prime_minus_one_stream`
- `transform_parameters.offset`
- `transform_parameters.direction`
- `transform_parameters.reset_mode`
- `transform_parameters.prime_index_policy`
- calibrated score fields and crib hits
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3G summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `prime_candidate_count`, `reset_modes`, and `confidence_distribution`.

Generated Stage 3G files remain ignored under `experiments/results/bounded-auto-runs/stage3g/`. They are candidate leads only and not solve evidence. Stage 3G also adds a future Mersenne/perfect-number queue item, but it remains `needs_executor` and is not executed.

## Stage 3H Reset/Advance Ablation Records

Stage 3H reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for reset/advance ablation. Candidate records include:

- `base_transform_id`
- `base_transform_family`
- `reset_mode`
- `advance_mode`
- `transformable_token_count`
- `metadata_support_status`
- calibrated scoring fields and crib-hit fields

The generated Stage 3H summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `reset_advance_candidate_count`, `negative_control_count`, `metadata_support_status`, and `confidence_distribution`.

Family-specific negative controls are generated as ignored JSONL records in `negative_control_records.jsonl`. They are false-positive controls only, not candidate solve evidence.

The consistency checks cross-reference committed schemas, manifests, registry metadata, documentation status, ignored-output policy, and result-store records when generated outputs are present.
