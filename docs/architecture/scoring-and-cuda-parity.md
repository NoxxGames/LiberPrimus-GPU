# Scoring And CUDA Parity

Stage 4H defines CPU batch transform parity. Stage 4I adds the matching score-summary contract.

Future CUDA work must match CPU output text and token hashes before score parity is meaningful. Once output hashes match, CUDA score summaries must match the CPU scorer contract:

- same scorer id and version
- same calibration profile
- same score components and confidence-label mapping
- same no-solve, canonical-corpus, page-boundary, and CUDA flags

CUDA remains deferred. Existing CUDA code is scaffold/smoke infrastructure only until an explicit future stage adds CPU/GPU parity tests and benchmark plans.
