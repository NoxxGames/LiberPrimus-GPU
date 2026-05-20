# Scoring And CUDA Parity

Stage 4H defines CPU batch transform parity. Stage 4I adds the matching score-summary contract.

Future CUDA work must match CPU output text and token hashes before score parity is meaningful. Once output hashes match, CUDA score summaries must match the CPU scorer contract:

- same scorer id and version
- same calibration profile
- same score components and confidence-label mapping
- same no-solve, canonical-corpus, page-boundary, and CUDA flags

CUDA remains deferred. Existing CUDA code is scaffold/smoke infrastructure only until an explicit future stage adds CPU/GPU parity tests and benchmark plans.

## Stage 4O Compatibility

Stage 4O expands CPU batch adapter coverage and writes parity expectations for `8` CPU-only outputs. The scoring compatibility check confirms `8` compatible score summaries and `0` unavailable score summaries for the Stage 4O run.

Future result-store or CUDA work must preserve the Stage 4I score-summary shape and the Stage 4O parity expectation hashes. A CUDA score comparison is meaningful only after output token/text hashes match the CPU reference.
