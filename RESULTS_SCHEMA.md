# Results Schema

## Purpose

Define result, manifest, source-lock, observation, and generated-output record policy for the workbench.

## Current Schema State

The repository now includes committed schema families for solved-baseline records, result-store records, bounded experiment manifests, archive/image/web observations, hash preimage packs, Discord ingestion/review/promotion records, full Discord review bundle records, post-Discord manifests, GP/rune claim records, image-transform records, stego/OutGuess regression records, Stage 3Y research-synthesis ledgers, Stage 4B source-lock/visual-intake records, Stage 4D bounded numeric records, Stage 4E source-delta/image-artifact backlog records, Stage 4F historical stego/audio fixture source-lock records, Stage 4G cookie refresh records, Stage 4H CPU batch/parity records, Stage 4I scoring records, Stage 4J observation review records, Stage 4K public source-lock snapshot records, Stage 4L observation promotion ledger records, Stage 4M image source-variant/compression preflight records, Stage 4N stego/audio positive-control readiness records, Stage 4O CPU batch adapter expansion/parity expectation records, Stage 4P result-store/score-summary unification records, Stage 4Q benchmark/parity planning records, Stage 5A CUDA planning/parity scaffold records, Stage 5B CUDA parity harness skeleton records, Stage 5C CUDA build/device detection records, Stage 5D native CPU backend/threading records, Stage 5E first CUDA kernel contract records, Stage 5F synthetic CUDA kernel/parity records, Stage 5G CUDA parity-reporting/device-code audit records, Stage 5H Gematria mod-29 shift-score contract records, Stage 5I Gematria CUDA preparation records, Stage 5J Gematria CUDA kernel implementation/build/parity records, Stage 5K Gematria CUDA parity-reporting/preflight records, Stage 5L solved-fixture token-mapping/native parity records, Stage 5M solved-fixture CUDA run/parity/boundary records, Stage 5N solved-fixture CUDA reporting/gate records, Stage 5O solved-fixture CUDA repeat/result-store preflight records, Stage 5P Gematria CUDA result-store/score-summary integration records, and Stage 5Q Gematria expansion candidate-mapping records.

Generated candidate records, SQLite databases, local review indexes, derived images, topic shards, extraction payloads, and full run outputs remain ignored unless a future stage explicitly promotes a summary or curated record.

Stage 5P Gematria CUDA result-store integration records require `compact_summary_only=true`,
`stage4p_compatibility=true`, `stage4i_compatibility=true`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`method_status_upgrade_allowed=false`, `cuda_execution_performed=false`,
`cuda_source_modified=false`, `new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, and `solve_claim=false`. Generated JSON
reports remain ignored under `experiments/results/gematria-cuda-result-store/stage5p/`; only
compact YAML records under `data/cuda/` are committed.

Stage 5P schemas include `gematria-cuda-result-store-integration-record-v0`,
`gematria-cuda-score-summary-integration-record-v0`,
`gematria-cuda-method-status-impact-record-v0`,
`gematria-cuda-generated-body-policy-record-v0`,
`gematria-cuda-controlled-expansion-candidate-record-v0`, and
`stage5p-cuda-result-store-integration-summary-v0`.

Stage 5Q Gematria expansion candidate-mapping records require `compact_summary_only=true`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`, `cuda_execution_performed=false`,
`cuda_source_modified=false`, `new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, `method_status_upgrade_allowed=false`,
and `solve_claim=false`. Generated JSON reports remain ignored under
`experiments/results/gematria-expansion-candidate-mapping/stage5q/`; only compact YAML records
under `data/cuda/` are committed.

Stage 5Q schemas include `gematria-expansion-candidate-inventory-record-v0`,
`gematria-expansion-token-mapping-record-v0`, `gematria-expansion-native-parity-record-v0`,
`gematria-expansion-result-store-preflight-record-v0`, `gematria-expansion-gate-record-v0`, and
`stage5q-expansion-candidate-mapping-summary-v0`.

Stage 3Y research-synthesis records under `data/research/` are committed source-of-truth metadata, not generated experiment outputs. They must keep `solve_claim=false`, record method-family status/reopen conditions, and preserve no-broadening guardrails for noisy, negative, inconclusive, deferred, or infrastructure-only families.

Stage 4B records under `data/observations/archive/`, `data/locks/third-party/`, `data/observations/visual/`, `data/observations/research/`, and `data/observations/web/` are committed source/observation metadata. They must keep `trusted_as_canonical=false` and `solve_claim=false`; visual records must also keep `usable_as_experiment_seed=false`. Stage 4B disabled manifests must keep `execution_enabled=false`, `cuda_enabled=false`, and `no_solve_claim=true`.

Stage 4C records under `data/observations/visual/` are committed annotation task metadata. They must keep `trusted_as_canonical=false`, `usable_as_experiment_seed=false`, and `solve_claim=false`. Generated annotation sites, page-image copies, grid overlays, and blank templates remain ignored.

Stage 4D bounded numeric verifier records are generated JSON/JSONL outputs under `experiments/results/bounded-numeric/stage4d/`. They must keep `solve_claim=false`, `cuda_used=false`, `trusted_as_canonical=false`, `no_fudge_policy=true`, and `generated_outputs_committed=false`. Raw values and derived values must stay separated, and every derived value must record a formula and source.

Stage 4E source-delta records are committed metadata records only. They must keep `raw_file_committed=false`, `binary_committed=false`, `font_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`. Generated tree reports remain ignored under `experiments/results/source-delta/stage4e/`.

Stage 4F stego/audio fixture source records are committed metadata records only. They must keep `raw_file_committed=false`, `binary_committed=false`, `audio_committed=false`, `image_committed=false`, `font_committed=false`, `extracted_payload_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`. Future fixture manifests must keep `execution_enabled=false`. Generated fixture reports remain ignored under `experiments/results/stego-fixtures/stage4f/`.

Stage 4G cookie refresh schemas require exact-match-only records: `no_solve_claim=true`, `cuda_used=false`, `cloud_execution=false`, `hashcat_used=false`, `fuzzy_matching=false`, `partial_matching=false`, manifest-declared variants and algorithms, and source-backed base strings. Generated candidate/exact-match JSONL and summary JSON remain ignored under `experiments/results/cookie-refresh/stage4g/`; only the aggregate YAML summary is committed.

Stage 4H CPU batch records require `cpu_only=true`, `cuda_used=false`, `cuda_required=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `generated_outputs_committed=false`. Generated result JSONL and summary JSON remain ignored under `experiments/results/cpu-batch/stage4h/`; only the aggregate YAML summary and parity contract are committed.

Stage 4I scoring records require finite confidence labels, scorer IDs/versions, calibration-profile references where available, `solve_claim=false`, `trusted_as_canonical=false`, and `cuda_used=false`. Generated scorer inventories and rendered calibration reports remain ignored under `experiments/results/scoring-consolidation/stage4i/`.

Stage 4J observation review records require explicit review states, promotion gates, quarantine/control records, `solve_claim=false`, `trusted_as_canonical=false`, and `usable_as_experiment_seed=false` unless a future explicit promotion stage changes that with review evidence. Generated review decision, quarantine, promotion-gate, and path-sanitisation reports remain ignored under `experiments/results/observation-review/stage4j/`.

Stage 4K source-lock snapshot records require `raw_private_data_committed=false`,
`binary_committed=false`, `image_committed=false`, `audio_committed=false`, `font_committed=false`,
`archive_committed=false`, and `solve_claim=false`. Fetched records require content hashes, and
committed snapshots are restricted to explicitly allowed small text snapshot policy. Generated
source-lock reports remain ignored under `experiments/results/source-lock-snapshots/stage4k/`;
fetched public-source bytes remain ignored under `third_party/SourceSnapshots/`.

Stage 4L observation-promotion records require `execution_enabled=false`, `solve_claim=false`,
explicit promotion categories, review-decision references, blockers for blocked/deferred/quarantined
and rejected states, and disabled manifest-readiness records. Generated reports remain ignored under
`experiments/results/observation-promotion/stage4l/`.

Stage 4M image-preflight records require `raw_image_committed=false`,
`generated_image_committed=false`, `solve_claim=false`, `trusted_as_canonical=false`,
`usable_as_experiment_seed=false`, `image_interpretation_claim=false`, metric-only compression
records, explicit source-variant statuses, and blocked bigram/Fibonacci-421 readiness unless a
future stage provides reproducible matrix regeneration and controls. Generated JSONL reports remain
ignored under `experiments/results/image-preflight/stage4m/`; raw page images and
`data/raw/images/Fib421.jpg` remain ignored.

Stage 4N stego/audio positive-control readiness records require `raw_file_committed=false`,
`binary_committed=false`, `image_committed=false`, `audio_committed=false`, `font_committed=false`,
`archive_committed=false`, `extracted_payload_committed=false`, `solve_claim=false`,
`execution_performed=false`, and `tool_executed=false`. Historical real positive-control readiness
requires exact expected-output metadata; synthetic controls must be labelled synthetic. Generated
reports remain ignored under `experiments/results/stego-positive-controls/stage4n/`; fixture cache
bytes remain ignored under `third_party/StegoPositiveControls/`.

Stage 4O CPU batch adapter expansion records require `cpu_only=true`, `cuda_used=false`,
`cuda_required=false`, `no_solve_claim=true`, `canonical_corpus_active=false`,
`page_boundaries_final=false`, and `generated_outputs_committed=false`. Adapter coverage records use
`supported`, `missing`, `deferred`, or `unsupported_by_design`; parity expectation records require
output hashes when parity passes. Generated result, coverage, parity, scoring, and summary reports
remain ignored under `experiments/results/cpu-batch/stage4o/`; only the aggregate Stage 4O summary
is committed under `data/research/`.

Stage 4P result-store and score-summary unification records require `cuda_used=false`,
`cuda_required=false`, `no_solve_claim=true`, `solve_claim=false`,
`canonical_corpus_active=false`, `page_boundaries_final=false`,
`generated_outputs_committed=false`, `raw_data_processed=false`,
`new_experiment_executed=false`, and `new_scorer_added=false`. Score interpretation remains
`triage_only`, confidence labels use the Stage 4I vocabulary plus explicit unavailable states, and
missing optional generated outputs are inventory warnings. Generated unified records remain ignored
under `experiments/results/result-store-unification/stage4p/`; only the aggregate Stage 4P summary
is committed under `data/research/`.

Stage 5B CUDA parity harness records require `cuda_kernel_added=false`,
`cuda_source_modified=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `solve_claim=false`, `no_solve_claim=true`,
`generated_outputs_committed=false`, `codex_output_committed=false`, and
`website_expansion=false`. Backend capability records must keep `cuda_hardware_required=false`
and `local_16gb_profile_required=false`; local 16GB GPU metadata is optional planning metadata
only. Generated harness reports remain ignored under `experiments/results/cuda-parity/stage5b/`;
only compact YAML records under `data/cuda/` are committed.

Committed Stage 5B schema IDs:

- `cuda-parity-harness-record-v0`
- `cuda-parity-fixture-record-v0`
- `cuda-backend-capability-record-v0`
- `cuda-future-kernel-parity-matrix-v0`
- `stage5b-cuda-parity-harness-summary-v0`

Stage 5C CUDA build/device records require `cuda_build_device_detection_only=true`,
`cuda_required=false`, `gpu_required=false`, `local_16gb_profile_required=false`,
`compatibility_8gb_profile_present=true`, `cuda_kernel_added=false`,
`cuda_source_modified=false`, `cryptanalytic_cuda_kernel_added=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`solve_claim=false`, `no_solve_claim=true`, `generated_outputs_committed=false`,
`codex_output_committed=false`, and `website_expansion=false`. Generated build/device reports
remain ignored under `experiments/results/cuda-build/stage5c/`; only compact YAML records under
`data/cuda/` are committed.

Committed Stage 5C schema IDs:

- `cuda-build-profile-record-v0`
- `cuda-toolchain-detection-record-v0`
- `cuda-device-detection-record-v0`
- `cuda-smoke-build-record-v0`
- `stage5c-cuda-build-device-summary-v0`

Stage 5D native CPU backend records require `native_cpu_only=true`, `cuda_used=false`,
`cuda_required=false`, `gpu_required=false`, `gpu_benchmark_performed=false`,
`cuda_kernel_added=false`, `cuda_source_modified=false`, `performance_claim=false`,
`speedup_claim=false`, `solve_claim=false`, `no_solve_claim=true`,
`generated_outputs_committed=false`, `codex_output_committed=false`, `website_expansion=false`,
`python_semantic_reference_preserved=true`, and `cxx_launches_python_workers=false`. Threading
records must preserve deterministic ordering, fixed output slots, and range partitioning. Generated
native CPU reports remain ignored under `experiments/results/native-cpu/stage5d/`; only compact YAML
records under `data/native-cpu/` are committed.

Committed Stage 5D schema IDs:

- `native-cpu-backend-capability-record-v0`
- `native-cpu-threading-record-v0`
- `native-cpu-parity-record-v0`
- `native-cpu-diagnostic-record-v0`
- `stage5d-native-cpu-summary-v0`

Stage 5E first CUDA kernel contract records require `cuda_kernel_contract_only=true`,
`cuda_kernel_added=false`, `cuda_source_modified=false`, `cryptanalytic_cuda_kernel_added=false`,
`cuda_transform_executed=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `broad_experiment_executed=false`, `raw_data_processed=false`,
`solve_claim=false`, `no_solve_claim=true`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `website_expansion=false`, `cuda_required=false`,
`gpu_required=false`, `local_16gb_profile_required=false`,
`python_semantic_reference_preserved=true`, and `cxx_launches_python_workers=false`. Generated
kernel-contract reports remain ignored under
`experiments/results/cuda-kernel-contract/stage5e/`; only compact YAML records under `data/cuda/`
are committed.

Committed Stage 5E schema IDs:

- `cuda-first-kernel-contract-record-v0`
- `cuda-adapter-selection-record-v0`
- `cuda-native-parity-adapter-record-v0`
- `cuda-implementation-readiness-record-v0`
- `stage5e-first-kernel-contract-summary-v0`

Stage 5F synthetic CUDA kernel records require `selected_kernel_id=shift_score_kernel`,
`selected_transform_family=caesar_mod29`, `selected_adapter_family=native_cpu_synthetic_shift_adapter`,
`synthetic_only=true`, `cuda_kernel_added=true`, `cuda_source_modified=true`,
`real_liber_primus_data_used=false`, `solved_fixture_cuda_used=false`,
`unsolved_page_cuda_used=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `broad_experiment_executed=false`, `raw_data_processed=false`,
`solve_claim=false`, `no_solve_claim=true`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `website_expansion=false`, `canonical_corpus_active=false`,
`page_boundaries_final=false`, `ci_gpu_required=false`, `no_gpu_ci_safe=true`,
`python_semantic_reference_preserved=true`, and `cxx_launches_python_workers=false`. Generated
kernel reports remain ignored under `experiments/results/cuda-kernel/stage5f/`; only compact YAML
records under `data/cuda/` are committed.

Committed Stage 5F schema IDs:

- `cuda-synthetic-kernel-implementation-record-v0`
- `cuda-kernel-build-record-v0`
- `cuda-synthetic-parity-run-record-v0`
- `stage5f-synthetic-cuda-kernel-summary-v0`

Stage 5G CUDA parity-reporting records require `selected_kernel_id=shift_score_kernel`,
`stage5f_cuda_native_hash_match=true`, `device_code_subset_compliant=true`,
`new_cuda_kernels_added=0`, `solved_fixture_cuda_execution_allowed=false`,
`production_gematria_mod29_cuda_ready=false`, `real_liber_primus_data_used=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`generated_outputs_committed=false`, `codex_output_committed=false`, and `solve_claim=false`.

Committed Stage 5G schema IDs:

- `cuda-shift-score-parity-report-record-v0`
- `cuda-device-code-subset-audit-record-v0`
- `cuda-solved-fixture-safe-preflight-record-v0`
- `stage5g-cuda-parity-reporting-summary-v0`

Stage 5H Gematria shift contract records require `selected_future_kernel_id=shift_score_kernel`,
`token_domain=integers_0_to_28`, `arithmetic_direction=forward_add_shift_mod29`,
`stage5h_cuda_execution_allowed=false`, `solved_fixture_cuda_execution_allowed=false`,
`production_gematria_mod29_cuda_ready=false`, `real_liber_primus_data_used=false`,
`solved_fixture_cuda_used=false`, `unsolved_page_cuda_used=false`, `new_cuda_kernels_added=0`,
`cuda_source_modified=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `generated_outputs_committed=false`, `codex_output_committed=false`, and
`solve_claim=false`. The Stage 5H native fixture hash must not equal the Stage 5F uppercase Latin
synthetic hash.

Committed Stage 5H schema IDs:

- `gematria-shift-score-contract-record-v0`
- `gematria-native-parity-fixture-record-v0`
- `gematria-solved-fixture-safe-mapping-record-v0`
- `gematria-score-summary-parity-plan-record-v0`
- `stage5h-gematria-shift-contract-summary-v0`

Stage 5I Gematria CUDA preparation records require `target_future_kernel_name=gematria_mod29_shift_score_kernel`,
`token_domain=integers_0_to_28`, `arithmetic_direction=forward_add_shift_mod29`,
`separator_policy=non_transformable_separators_preserved_unshifted`, `cuda_source_modified=false`,
`new_cuda_kernels_added=0`, `cuda_execution_performed=false`,
`solved_fixture_cuda_execution_allowed=false`, `production_gematria_mod29_cuda_ready=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`real_liber_primus_data_used=false`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`,
`no_solve_claim=true`, and `solve_claim=false`. Validation vectors use raw numeric token buffers,
transformable masks, and candidate-major output order; separator placeholders stay inert.

Committed Stage 5I schema IDs:

- `gematria-cuda-kernel-preparation-record-v0`
- `gematria-cuda-abi-plan-record-v0`
- `gematria-cuda-validation-vector-record-v0`
- `gematria-cuda-implementation-checklist-record-v0`
- `stage5i-gematria-cuda-preparation-summary-v0`

Stage 5J Gematria CUDA kernel records require `implemented_kernel_name=gematria_mod29_shift_score_kernel`,
`source_contract_id=gematria_mod29_shift_score_contract_v0`,
`token_domain=integers_0_to_28`, `arithmetic_direction=forward_add_shift_mod29`,
`separator_policy=non_transformable_separators_preserved_unshifted`, `synthetic_only=true`,
`new_cuda_kernels_added=1`, `solved_fixture_cuda_execution_allowed=false`,
`production_gematria_mod29_cuda_ready=false`, `real_liber_primus_data_used=false`,
`solved_fixture_cuda_used=false`, `unsolved_page_cuda_used=false`, `gpu_benchmark_performed=false`,
`performance_claim=false`, `speedup_claim=false`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`,
`no_solve_claim=true`, and `solve_claim=false`. A passed synthetic parity record must match the
Stage 5H native fixture hash `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`.

Committed Stage 5J schema IDs:

- `gematria-cuda-kernel-implementation-record-v0`
- `gematria-cuda-kernel-build-record-v0`
- `gematria-cuda-synthetic-parity-record-v0`
- `stage5j-gematria-cuda-kernel-summary-v0`

Stage 5K Gematria CUDA parity-reporting records require `implemented_kernel_name=gematria_mod29_shift_score_kernel`,
`source_contract_id=gematria_mod29_shift_score_contract_v0`,
`native_fixture_id=stage5h-gematria-mod29-synthetic-shift-fixture-v0`,
`stage5j_cuda_native_hash_match=true`, `synthetic_parity_verified=true`,
`device_code_subset_compliant=true`, `new_cuda_kernels_added=0`,
`cuda_source_modified=false`, `cuda_execution_performed=false`,
`solved_fixture_cuda_execution_allowed=false`, `production_gematria_mod29_cuda_ready=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`real_liber_primus_data_used=false`, `solved_fixture_cuda_used=false`,
`unsolved_page_cuda_used=false`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`,
`no_solve_claim=true`, and `solve_claim=false`. A Stage 5K parity report must preserve the
Stage 5J CUDA output hash and Stage 5H native fixture hash as matching values, and solved-fixture
preflight records must remain blocked until token mapping, score-summary parity, and no-unsolved
guardrails are explicit.

Committed Stage 5K schema IDs:

- `gematria-cuda-parity-report-record-v0`
- `gematria-cuda-device-code-audit-record-v0`
- `gematria-solved-fixture-safe-preflight-record-v0`
- `gematria-cuda-score-summary-preflight-record-v0`
- `stage5k-gematria-cuda-parity-reporting-summary-v0`

Stage 5L solved-fixture token-mapping records require source-backed Gematria token values in
`0..28`, explicit token kinds, transformable masks, separator metadata, candidate-major output
ordering, `hash_algorithm=sha256_canonical_json_v1`, and Stage 4I-compatible score-summary labels.
They must keep `cuda_execution_performed=false`, `cuda_source_modified=false`,
`new_cuda_kernels_added=0`, `solved_fixture_cuda_execution_allowed=false`,
`generated_outputs_committed=false`, `codex_output_committed=false`, `no_solve_claim=true`, and
`solve_claim=false`.

Committed Stage 5L schema IDs:

- `gematria-solved-fixture-token-mapping-record-v0`
- `gematria-solved-fixture-native-parity-record-v0`
- `gematria-solved-fixture-output-hash-contract-v0`
- `gematria-solved-fixture-score-summary-shape-v0`
- `stage5l-solved-fixture-token-mapping-summary-v0`

Stage 5M solved-fixture CUDA records require `executed_kernel=gematria_mod29_shift_score_kernel`,
`executed_semantics=gematria_shift_score_only`, `solved_fixture_cuda_execution_allowed=true`,
`solved_fixture_cuda_execution_scope=exact_stage5l_mapped_token_buffers_only`,
`unsolved_page_cuda_used=false`, `real_liber_primus_cuda_data_used=false`,
`new_cuda_kernels_added=0`, `device_kernel_arithmetic_modified=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`generated_outputs_committed=false`, `codex_output_committed=false`,
`canonical_corpus_active=false`, `page_boundaries_final=false`, `no_solve_claim=true`, and
`solve_claim=false`. Passed parity records require the CUDA output-token hash to match the Stage 5L
native output-token hash.

Committed Stage 5M schema IDs:

- `gematria-solved-fixture-cuda-run-record-v0`
- `gematria-solved-fixture-cuda-parity-record-v0`
- `gematria-solved-fixture-cuda-boundary-record-v0`
- `stage5m-solved-fixture-cuda-parity-summary-v0`

Stage 5N solved-fixture CUDA reporting records require `cuda_source_modified=false`,
`additional_cuda_execution_performed=false`, `new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`,
`real_liber_primus_cuda_data_used=false`, `gpu_benchmark_performed=false`, `speedup_claim=false`,
`generated_outputs_committed=false`, and `solve_claim=false`.

Committed Stage 5N schema IDs:

- `gematria-solved-fixture-cuda-report-record-v0`
- `gematria-cuda-controlled-expansion-gate-record-v0`
- `gematria-cuda-boundary-review-record-v0`
- `gematria-cuda-result-store-preflight-record-v0`
- `gematria-no-unsolved-guardrail-record-v0`
- `stage5n-solved-fixture-cuda-reporting-summary-v0`

Stage 5O solved-fixture CUDA repeat records require `cuda_source_modified=false`,
`new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`, `real_liber_primus_cuda_data_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, `generated_outputs_committed=false`, and
`solve_claim=false`. Passed repeat parity records must match both the Stage 5L native output-token hash
and the Stage 5M CUDA output-token hash.

Committed Stage 5O schema IDs:

- `gematria-solved-fixture-cuda-repeat-run-record-v0`
- `gematria-solved-fixture-cuda-repeat-parity-record-v0`
- `gematria-cuda-result-store-preflight-v0`
- `gematria-cuda-score-summary-preflight-v0`
- `gematria-cuda-expansion-decision-record-v0`
- `stage5o-repeat-verification-result-store-summary-v0`

## Result record principles

Records must be replayable, reviewable, compact, and explicit about uncertainty.

## Common JSONL Fields

Generated and committed record families use fields such as result ID, experiment ID, manifest hash, corpus lock ID, transform chain, candidate summary, scores, null-control scores, rank, timestamps, review status, privacy flags, CUDA flags, canonical-corpus flags, page-boundary flags, and solve-claim flags.

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

## SQLite Result Store

Stage 2B added a SQLite result-store foundation for generated local outputs. SQLite databases and sidecar files are generated outputs and must not be committed.

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

## Stage 3O Discord Promotion Records

Stage 3O committed promotion records use redacted YAML summaries under `data/observations/discord/`.

Required fields include:

- `promoted_id`
- `source=discord_admin_export_stage3n`
- `source_record_type`
- `redacted=true`
- `review_status`
- `trusted_as_canonical=false`
- `raw_message_committed=false`
- `usernames_committed=false`

Generated full candidate lists and unsafe-link rejection lists remain ignored under `experiments/results/discord-promotion/stage3o/`. Wiki sync reports remain ignored under `experiments/results/wiki-sync/stage3o/`.

## Stage 3Q Discord Review Bundle Records

Stage 3Q adds schemas for generated redacted message records, generated topic shard records, generated review lead records, and the committed aggregate review-bundle summary.

Committed aggregate fields include:

- `bundle_id`
- `html_file_count`
- `redacted_message_count`
- `topic_shard_count`
- `review_lead_count`
- `public_link_count`
- `method_claim_count`
- `numeric_observation_count`
- `visual_observation_count`
- `debunk_count`
- false privacy flags for raw logs, raw messages, usernames, private URLs, AI upload, live API use, scraping, and solve claims

Generated redacted streams, topic shards, JSONL indexes, and local HTML review indexes remain ignored under `experiments/results/discord-review-bundles/stage3q/`.

## Stage 4A Discord Full Review Bundle Records

Stage 4A adds schemas for generated full-review channel records, redacted message records, shard
records, index records, bundle summaries, Discord image references, and LP page gallery records.

Committed schema IDs:

- `discord-full-review-channel-record-v0`
- `discord-full-review-message-record-v0`
- `discord-full-review-shard-record-v0`
- `discord-full-review-index-record-v0`
- `discord-full-review-summary-v0`

## Stage 4B Source-Lock And Visual Intake Records

Stage 4B adds schemas for source triage, source health, visual observation intake, negative-control records, and disabled future manifest records.

Committed schema IDs:

- `stage4b-source-triage-record-v0`
- `source-health-record-v0`
- `stage4b-visual-observation-record-v0`
- `negative-control-record-v1`
- `stage4b-disabled-experiment-manifest-v0`

Generated triage diagnostics remain ignored under `experiments/results/source-lock-triage/stage4b/`.
- `lp-page-gallery-record-v0`
- `discord-image-reference-v0`

## Stage 4C Visual Annotation Records

Stage 4C adds schemas for visual annotation tasks, region annotation templates, cuneiform reading candidates, dot-pattern ambiguity tasks, delimiter tasks, visual negative-control annotation tasks, and the annotation pack summary.

Committed schema IDs:

- `visual-annotation-task-v0`
- `visual-region-annotation-v0`
- `cuneiform-reading-candidate-v0`
- `dot-pattern-annotation-v0`
- `delimiter-annotation-v0`
- `visual-negative-control-annotation-v0`
- `visual-annotation-pack-summary-v0`

Committed records live under `data/observations/visual/`. Generated site files and templates remain ignored under `experiments/results/visual-annotation/stage4c/`.

## Stage 4D Bounded Numeric Verifier Records

Stage 4D adds generated schemas for bounded numeric manifests, bounded numeric result records, numeric negative-control result records, and delimiter handedness audit records.

Committed schema IDs:

- `bounded-numeric-manifest-v0`
- `bounded-numeric-result-record-v0`
- `numeric-negative-control-result-v0`
- `delimiter-handedness-audit-record-v0`

Generated result files remain ignored under `experiments/results/bounded-numeric/stage4d/`.

## Stage 4E Source Delta Audit Records

Stage 4E adds committed schemas for source-delta audit records, source-path candidate records, source-variant comparison backlog records, image-compression artefact observations, and disabled future image/stego provenance manifests.

Committed schema IDs:

- `source-delta-audit-record-v0`
- `source-path-candidate-record-v0`
- `source-variant-comparison-record-v0`
- `image-compression-artifact-observation-v0`
- `future-image-artifact-manifest-v0`

Committed records live under `data/observations/archive/`, `data/locks/third-party/`, `data/observations/visual/`, and `experiments/manifests/stage4e-disabled/`. They must keep `raw_file_committed=false`, `binary_committed=false`, `font_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`.

Generated path indexes, source-delta reports, duplicate/unique candidate JSONL files, and warnings remain ignored under `experiments/results/source-delta/stage4e/`. Raw cache contents under `third_party/CicadaSolversIddqd/` remain ignored except for README/.gitkeep.

## Stage 4F Stego Audio Fixture Source Records

Stage 4F adds committed schemas for historical OutGuess fixture source records, audio fixture source records, source-health records, historical stego fixture manifests, and toolchain requirement records.

Committed schema IDs:

- `stego-fixture-source-record-v0`
- `audio-fixture-source-record-v0`
- `fixture-source-health-record-v0`
- `historical-stego-fixture-manifest-v0`
- `toolchain-requirement-record-v0`

Committed records live under `data/observations/stego/` and `data/locks/third-party/`. Disabled future manifests live under `experiments/manifests/stego/stage4f-disabled/`.

Generated fixture candidate reports, source-gap JSONL files, and warnings remain ignored under `experiments/results/stego-fixtures/stage4f/`. Raw images, audio, binaries, fonts, archives, and extracted payloads remain uncommitted.

## Stage 4N Stego Audio Positive-Control Readiness Records

Stage 4N adds committed schemas for stego readiness, audio readiness, fixture-cache records,
expected-output records, toolchain readiness, and positive-control summaries.

Committed schema IDs:

- `stego-positive-control-readiness-v0`
- `audio-positive-control-readiness-v0`
- `stego-fixture-cache-record-v0`
- `stego-expected-output-record-v0`
- `stego-toolchain-readiness-v0`
- `stego-positive-control-summary-v0`

Generated readiness reports remain ignored under `experiments/results/stego-positive-controls/stage4n/`.
Local fixture cache bytes remain ignored under `third_party/StegoPositiveControls/`.

## Stage 4O CPU Batch Adapter Expansion Records

Stage 4O adds committed schemas for adapter coverage, parity expectations, solved-fixture streams,
scoring compatibility, and the aggregate adapter-expansion summary.

Committed schema IDs:

- `cpu-batch-adapter-coverage-v0`
- `cpu-batch-parity-expectation-v0`
- `cpu-batch-adapter-expansion-summary-v0`
- `cpu-batch-solved-fixture-stream-v0`
- `cpu-batch-scoring-compatibility-v0`

Generated Stage 4O result, coverage, parity, scoring, and summary records remain ignored under
`experiments/results/cpu-batch/stage4o/`. The committed aggregate summary lives under
`data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml`.

## Stage 4P Result Store Score Summary Unification Records

Stage 4P adds committed schemas for unified result records, unified score-summary records, source
inventory records, method-status joins, cross-stage reports, and aggregate unification summaries.

Committed schema IDs:

- `unified-result-record-v0`
- `unified-score-summary-record-v0`
- `result-source-inventory-v0`
- `result-method-status-join-v0`
- `cross-stage-comparison-report-v0`
- `result-store-unification-summary-v0`

Generated Stage 4P source inventory, unified result JSONL, unified score-summary JSONL,
method-status join, cross-stage report, summary JSON, warnings, and any SQLite probes remain ignored
under `experiments/results/result-store-unification/stage4p/`. The committed aggregate summary lives
under `data/research/stage4p-result-store-score-summary-unification-summary.yaml`.

## Stage 4G Cookie Refresh Records

Stage 4G adds committed schemas for the cookie refresh manifest view, generated candidate records, and committed aggregate summary:

- `schemas/web/cookie-refresh-manifest-v0.schema.json`
- `schemas/web/cookie-refresh-candidate-record-v0.schema.json`
- `schemas/web/cookie-refresh-summary-v0.schema.json`

Candidate records log the experiment ID, source record, source basis, byte variant, UTF-8 candidate byte hash, digest, target cookie, exact-match flag, previous-pack duplicate flag, and all no-broadening policy flags. Generated records are not committed.

## Stage 4H CPU Batch Records

Stage 4H adds committed schemas for the CPU batch manifest, input stream, transform candidate, generated result record, run summary, and CPU/CUDA parity contract:

- `schemas/experiments/cpu-batch-manifest-v0.schema.json`
- `schemas/experiments/cpu-batch-input-stream-v0.schema.json`
- `schemas/experiments/cpu-batch-transform-candidate-v0.schema.json`
- `schemas/experiments/cpu-batch-result-record-v0.schema.json`
- `schemas/experiments/cpu-batch-run-summary-v0.schema.json`
- `schemas/experiments/cpu-cuda-parity-contract-v0.schema.json`

Result records log transform IDs, parameters, token counts, execution status, output hashes, optional structured score summaries, and all no-CUDA/no-solve policy flags. Generated CPU batch records are not committed.

Committed aggregate summaries live under:

- `data/observations/discord/stage4a-full-review-aggregate.yaml`
- `data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml`

Aggregate records contain only counts, generated output paths, source directory references, and
privacy flags. They must not contain raw messages, usernames, user IDs, message IDs, private URLs,
raw Discord HTML, generated site content, or copied LP page image bytes.

Generated redacted streams, channel shards, topic shards, indexes, static site files, copied LP page
images, thumbnails, contact sheets, and upload archives remain ignored under
`experiments/results/discord-full-review/stage4a/`.

## Stage 3R Discord Lead Promotion And Post-Discord Manifest Records

Stage 3R adds committed schemas for:

- `promoted_discord_source_record`
- `promoted_discord_observation_record`
- `negative_control_record`
- `post_discord_experiment_manifest`
- `gp_rune_claim_record`

Promoted source and observation records require false privacy flags for raw messages, usernames, and private URLs. Observation records keep `usable_as_experiment_seed=false` and `trusted_as_canonical=false`.

Negative-control records preserve known false-positive classes and require `solve_claim=false`.

Post-Discord manifests require `execution_enabled=false`, `cpu_only=true`, `cuda_enabled=false`, `cloud_execution=false`, `paid_services=false`, `generated_outputs_committed=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

Generated promotion-audit records remain ignored under `experiments/results/discord-lead-promotion/stage3r/`.

## Stage 3S Onion 7 Candidate Records

Stage 3S generated records are written only to ignored outputs under `experiments/results/post-discord/stage3s/`.

Candidate records include:

- `experiment_id=EXP-3R-003`
- `manifest_id`
- `value_space`
- `route`
- `direction`
- `reset_mode`
- `numeric_sequence`
- `numeric_sequence_mod29`
- `sequence_signature_sha256`
- `candidate_index`
- `input_slice_id`
- `transform_family=onion7_numeric_seed_pack`
- `transform_id=onion7_mod29_stream_subtract`
- score summary and calibrated confidence label
- `cuda_used=false`
- `no_solve_claim=true`
- `canonical_corpus_active=false`
- `page_boundaries_final=false`
- `trusted_as_canonical=false`

Generated `candidate_records.jsonl`, `top_candidates.jsonl`, `summary.json`, and warning/score files must not be committed. Research logs may summarize counts, top parameters, top score, and confidence only.

## Stage 3T GP/Rune Verification Records

Stage 3T generated records are written only to ignored outputs under `experiments/results/post-discord/stage3t/`.

Verification records include:

- `experiment_id=EXP-3R-004`
- `claim_id`
- `source_basis`
- `claim_type`
- `target_span`
- `claimed_value`
- `computed`
- `verification_status`
- `raw_message_committed=false`
- `username_committed=false`
- `private_url_committed=false`
- `cuda_used=false`
- `no_solve_claim=true`
- `canonical_corpus_active=false`
- `page_boundaries_final=false`
- `trusted_as_canonical=false`

Generated `gp_rune_claim_verification_records.jsonl`, per-status JSONL files, `summary.json`, and warnings must not be committed. Research logs may summarize status counts and representative claim IDs only.

## Stage 3U Cookie Signed-Variant Records

Stage 3U generated records are written only to ignored outputs under `experiments/results/post-discord/stage3u/`.

Candidate records include:

- `experiment_id=EXP-3R-001`
- `pack_id`
- `manifest_id`
- `candidate_id`
- `base_string_id`
- `base_string`
- `source_basis`
- `byte_variant`
- `encoding`
- `candidate_bytes_sha256`
- `digest_algorithm=sha256`
- `digest_hex`
- `target_cookie_id`
- `target_cookie_name`
- `exact_match`
- `solve_claim=false`
- `cuda_used=false`
- `cloud_execution=false`
- `trusted_as_canonical=false`

Generated `hash_candidate_records.jsonl`, `exact_matches.jsonl`, `summary.json`, and warnings must not be committed. Research logs may summarize counts and exact-match IDs only.

## Stage 3V OutGuess Regression Records

Stage 3V generated records are written only to ignored outputs under `experiments/results/stego/outguess/stage3v/`.

Committed schemas:

- `stego-artifact-record-v0`
- `outguess-regression-manifest-v0`
- `outguess-tool-record-v0`
- `outguess-extraction-record-v0`
- `outguess-regression-summary-v0`

Extraction records include tool availability, asset availability, attempt status, exit code, extracted payload hash and size, expected payload hash, payload-match flag, status, output paths, `raw_payload_committed=false`, `solve_claim=false`, and `cuda_used=false`.

Generated extraction JSONL, tool JSON, summary JSON, warnings, synthetic inputs, and extracted payloads must not be committed.

## Post-Discord Manifest Schemas

Committed post-Discord queue metadata uses `post-discord-experiment-manifest-v0` for disabled/explicit experiment manifests and `gp-rune-claim-record-v0` for exact GP/rune verifier claim records. These schemas keep execution disabled until a later bounded stage explicitly runs one manifest and require no-solve policy fields.

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

Generated Stage 3G files remain ignored under `experiments/results/bounded-auto-runs/stage3g/`. They are candidate leads only and not solve evidence. Stage 3G also adds a future Mersenne/perfect-number queue item, which Stage 3J later promotes to runnable through a bounded executor.

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

## Stage 3I Historical Vigenere Key-Pack Records

Stage 3I reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the historical motif Vigenere key pack. Candidate records include:

- `transform_family=vigenere_key_pack`
- `transform_id=vigenere_explicit_key`
- `key_text`
- `key_indices`
- `evidence_family=historical_motif_key_pack`
- `transform_parameters.reset_mode`
- `transform_parameters.advance_mode`
- `transform_parameters.evidence_family`
- calibrated scoring fields and crib-hit fields
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3I summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `key_count`, `reset_modes`, `advance_modes`, and `confidence_distribution`.

Generated Stage 3I files remain ignored under `experiments/results/bounded-auto-runs/stage3i/`. They are candidate leads only and not solve evidence.

## Stage 3J Mersenne Probe Records

Stage 3J reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the finite-sequence Mersenne/perfect-number probe. Candidate records include:

- `transform_family=mersenne_prime_stream`
- `transform_id=mersenne_prime_stream_tiny`
- `stream_variant`
- `exponent_sequence_id`
- `exponent_sequence`
- `offset`
- `direction`
- `reset_mode`
- `stream_signature_sha256`
- calibrated scoring fields and crib-hit fields
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3J summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `mersenne_candidate_count`, `stream_variants`, `directions`, `reset_modes`, `unique_stream_signature_count`, `duplicate_stream_signature_count`, and `confidence_distribution`.

Duplicate stream signatures are expected because the declared eight-exponent sequence is cyclic. They must be reported, not silently deduplicated.

Generated Stage 3J files remain ignored under `experiments/results/bounded-auto-runs/stage3j/`. They are candidate leads only and not solve evidence.

## Stage 3K Archive And Visual Registry Records

Stage 3K adds committed schemas under `schemas/history/` and `schemas/visual/` for:

- `source_archive_record`
- `source_lock_record`
- `cookie_hash_record`
- `image_artifact_record`
- `visual_numeric_observation`
- `visual_observation_reading`
- `image_analysis_summary`

Committed record files live under `data/observations/` and `data/locks/third-party/liber-primus-pages/`. Generated scan summaries remain ignored under `experiments/results/archive-visual-registry/stage3k/`.

All Stage 3K records keep `trusted_as_canonical=false`; visual observations keep `usable_as_experiment_seed=false`; cookie/hash records do not claim preimages.

## Stage 3L Hash Preimage Records

Stage 3L adds committed schemas under `schemas/web/` for:

- `hash_preimage_candidate_pack`
- `hash_preimage_candidate_record`
- `hash_preimage_match_record`
- `hash_preimage_run_summary`

Candidate records log the exact literal text before UTF-8 encoding, byte variant, byte-string SHA-256, target cookie, digest, and exact-match status.

Generated records remain ignored under `experiments/results/hash-preimage/stage3l/`. They are bounded preimage-test records only and not solve evidence.

## Stage 3M Image Analysis Records

Stage 3M adds committed schemas under `schemas/visual/` for:

- `image_analysis_record`
- `image_threshold_summary`
- `image_symmetry_record`
- `image_bitplane_summary`
- `image_component_summary`
- `visual_feature_candidate`
- `image_analysis_run_summary`

Generated records remain ignored under `experiments/results/image-analysis/stage3m/`.

All Stage 3M records keep `trusted_as_canonical=false` and `solve_claim=false`. Visual feature candidate records also keep `usable_as_experiment_seed=false`; they are human-review aids only and not image-derived seed manifests.

## Stage 3N Discord Ingestion Records

Stage 3N adds committed schemas under `schemas/history/` for:

- `discord_archive_record`
- `discord_html_file_lock`
- `discord_extracted_link`
- `discord_attachment_candidate`
- `discord_method_claim_candidate`
- `discord_numeric_observation_candidate`
- `discord_ingestion_summary`

Generated link, attachment, method-claim, numeric-observation, local-review, and per-file lock
records remain ignored under `experiments/results/discord-ingestion/stage3n/`.

Committed aggregate records under `data/locks/third-party/discord-chats/` and
`data/observations/discord/` contain aggregate counts and false privacy flags only. Raw logs,
message bodies, usernames, AI upload, live API use, and scraping are prohibited by schema and
validation.

## Stage 3P Image Transform Records

Stage 3P adds committed schemas under `schemas/visual/` for:

- `image_transform_record`
- `image_transform_metric_record`
- `visual_transform_candidate`
- `contact_sheet_record`
- `image_transform_run_summary`

Generated records remain ignored under `experiments/results/image-transforms/stage3p/`.

All Stage 3P records keep `trusted_as_canonical=false` and `solve_claim=false`. Transform and candidate records also keep `usable_as_experiment_seed=false`; they are human-review artefacts only and not image-derived seed manifests.

The consistency checks cross-reference committed schemas, manifests, registry metadata, documentation status, ignored-output policy, and result-store records when generated outputs are present.

## Stage 4I Scoring Consolidation Records

Stage 4I adds committed schemas under `schemas/scoring/` for:

- `scorer-record-v0`
- `scoring-calibration-profile-v0`
- `score-summary-record-v0`
- `confidence-label-record-v0`
- `scorer-compatibility-map-v0`
- `scoring-calibration-report-v0`

Committed records live under `data/scoring/`. Generated scorer inventories and report renderings remain ignored under `experiments/results/scoring-consolidation/stage4i/`.

All Stage 4I records keep scoring as triage metadata only. Score summary records require `solve_claim=false`, `trusted_as_canonical=false`, and `cuda_used=false`.
# Stage 4Q Benchmark Schemas

Stage 4Q adds benchmark planning schemas:

- `cpu-benchmark-plan-v0`
- `cpu-benchmark-smoke-record-v0`
- `benchmark-environment-record-v0`
- `cuda-parity-benchmark-readiness-v0`
- `stage4q-benchmark-parity-summary-v0`

These schemas require `cuda_used=false`, `cuda_required=false`, `gpu_benchmark_performed=false`, `cuda_implementation_added=false`, `solve_claim=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, `raw_data_processed=false`, `broad_experiment_executed=false`, and `generated_outputs_committed=false`.

# Stage 5A CUDA Planning Schemas

Stage 5A adds CUDA planning schemas:

- `cuda-target-plan-record-v0`
- `cuda-parity-scaffold-record-v0`
- `cuda-implementation-gate-record-v0`
- `cuda-non-target-record-v0`
- `cuda-planning-summary-v0`

These records require planning-only/no-solve flags and reject CUDA implementation, GPU benchmark, speedup claim, raw-data, generated-output, canonical-corpus, and page-boundary drift.
