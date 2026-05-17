# Bounded Candidate Output Schema

Stage 3A generated candidate records use `schemas/experiments/bounded-candidate-record-v0.schema.json`.

Required fields include:

- `record_type=bounded_candidate_record`
- `run_id`
- `queue_item_id`
- `transform_family`
- `transform_id`
- `transform_parameters`
- `candidate_index`
- `input_slice_id`
- `output_normalized_text`
- `output_preview`
- `output_sha256`
- `score_summary`
- `ranking_features`
- `search_performed=true`
- `scoring_used=true`
- `cuda_used=false`
- `solve_claim=false`
- `canonical_corpus_active=false`
- `page_boundaries_final=false`
- `trusted_as_canonical=false`

Generated candidate records are ignored output. Do not commit `candidate_records.jsonl`, `top_candidates.jsonl`, SQLite outputs, or bulk result files.

The summary schema is `schemas/experiments/bounded-experiment-run-summary-v0.schema.json`. Summary records can be used to write committed research-log notes, but committed notes should include counts and top score metadata only, not full candidate dumps.

Stage 3B refined score summaries include length-normalized scores, separator-aware word counts, impossible-bigram counts, feature explanations, and a confidence label. These fields are triage metadata only; they do not justify a solve claim.
