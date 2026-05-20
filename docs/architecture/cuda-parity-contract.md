# CUDA Parity Contract

Stage 4H creates the CPU/CUDA parity contract but no CUDA implementation. Future CUDA work must match CPU batch semantics before any GPU output is trusted.

Required parity anchors:

- Token order must match normalized CPU input stream order.
- Only `token_kind=rune` participates in modulo-29 transform arithmetic.
- Separators and unknown symbols must be preserved or skipped exactly as CPU records specify.
- Modulo arithmetic is over `Z_29`.
- Vigenere key advancement and skip rules must match `libreprimus.solved_fixtures.vigenere`.
- Prime stream values and payload skips must match `libreprimus.solved_fixtures.prime_stream`.
- Scoring parity requires byte-for-byte matching output text before score comparison.
- `output_text_hash` and `output_token_hash` are the first comparison anchors.

Stage 4I adds the score-summary contract for future transform-and-score parity. Stage 4O adds adapter-level parity expectations for solved-fixture-safe CPU batch outputs. Stage 4P adds unified result and score-summary surfaces so future CUDA planning can compare output hashes, score labels, method status, and retirement state without reading raw data or generated bulk outputs from Git. Stage 4Q adds CPU benchmark and parity readiness records so future CUDA planning can distinguish ready, blocked, and non-target transform families. Stage 5A adds target plans, parity scaffolds, non-target records, and implementation gates.

CUDA remains deferred until observation review hardening, source-lock readiness, promotion readiness, positive-control readiness, Stage 4P result-store/score-summary unification, Stage 4Q CPU benchmark and parity planning, Stage 5A target scaffolds, parity tests, and benchmark plans exist. Existing CUDA code remains scaffold/smoke infrastructure unless a later explicit stage says otherwise.
