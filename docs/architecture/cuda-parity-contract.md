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

Stage 4I adds the score-summary contract for future transform-and-score parity. CUDA remains deferred until observation review hardening, explicit CUDA planning, parity tests, and benchmark plans exist. Existing CUDA code remains scaffold/smoke infrastructure unless a later explicit stage says otherwise.
