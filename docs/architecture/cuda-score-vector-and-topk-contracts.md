# CUDA Score Vector And Top-K Contracts

Stage 5U binds future backend score output to Stage 4I triage-only scoring semantics.

## Score Vector

The contract records required compact score components:

- `output_token_hash`
- `score_status`
- `confidence_label`
- `triage_label`

Optional n-gram, crib, and dictionary placeholders are not execution-ready and do not define a new scorer.

## Top-K

Top-k output requires deterministic candidate-major ordering, stable tie breaking, required candidate IDs, required `output_token_hash`, and score-vector references. Top-k reducers are not implemented in Stage 5U.

Score labels and top-k order are triage/comparison aids only; they are not solve evidence and cannot upgrade method status.
