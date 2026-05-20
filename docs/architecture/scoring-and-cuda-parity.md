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

Future result-store or CUDA work must preserve the Stage 4I score-summary shape and the Stage 4O parity expectation hashes. A CUDA score comparison is meaningful only after output token/text hashes match the CPU reference and Stage 4Q readiness gates mark the transform family as a future CUDA planning target.

## Stage 4P Unified Score Views

Stage 4P normalizes score-summary-like surfaces into Stage 4I-compatible unified records. It wrote `82` unified score-summary records without adding labels, scorers, calibration profiles, or score components.

Unknown score semantics are recorded as `scoring_not_available`, not inferred. Future CUDA score parity should compare against the unified Stage 4P result surface only after Stage 4O output hashes match and Stage 4Q benchmark/parity planning records are cited.

## Stage 5A Planning Records

Stage 5A CUDA planning records cite Stage 4O parity hashes and Stage 4P unified result surfaces. A future parity harness must compare score-summary shape and confidence-label vocabulary without treating scores as solve evidence.

Stage 5D does not add a scorer or alter score-summary semantics. Future CUDA parity work must keep
Stage 4I score summaries, Stage 4P unified result surfaces, and Stage 5D native CPU output hashes
separate and reproducible.
