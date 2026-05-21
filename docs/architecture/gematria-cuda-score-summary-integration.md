# Gematria CUDA Score-Summary Integration

Stage 5P maps compact CUDA parity metadata into the Stage 4I score-summary vocabulary without adding
a scorer. The integration records use `scoring_not_available` and `triage_only` because parity hashes
are correctness metadata, not language evidence.

The score-summary surface is useful for cross-stage reporting and future review queues. It cannot
make a solve claim, upgrade a method family to solved, or imply that the original source transform
semantics were implemented in CUDA.

Stage 5Q keeps this score-summary boundary. New expansion candidates receive result-store preflight
records with `confidence_interpretation=triage_only` and `score_status=scoring_not_available`; no
new scoring model or confidence label is added.

Stage 5R keeps the same boundary for expanded solved-fixture CUDA parity. Its score-summary preflight
records cite the Stage 4I contract, use `scoring_not_available` with `triage_only` interpretation,
and do not introduce solve-evidence labels.
## Stage 5S Expanded Score-Summary Integration

Stage 5S writes three score-summary integration records for the Stage 5R expanded parity matches.
They use the Stage 4I contract and `scoring_not_available` as triage-only metadata because parity
success is not a decrypted-text score and does not rank unsolved candidates. The records preserve
`solve_claim=false`, `performance_claim=false`, `speedup_claim=false`, and
`method_status_upgrade_allowed=false`.
