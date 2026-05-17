# Triage Scoring Refinements

Stage 3B refines the minimal triage score used for bounded CPU candidates.

Added fields:

- `length_normalized_score`
- `separator_aware_word_count`
- `vowel_band_score`
- `impossible_bigram_count`
- `impossible_bigram_hits`
- `impossible_bigram_penalty`
- `positive_features`
- `negative_features`
- `confidence_label`
- `no_solve_claim=true`

The scorer now penalizes flat no-separator streams, repeated character runs, vowel ratios outside a small sanity band, and a tiny generic impossible-bigram list.

These scores are not solve evidence. They exist to reduce obvious false positives and to explain why a lead is ranked, weak, noisy, or garbage.
