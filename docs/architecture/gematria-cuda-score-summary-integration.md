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
