# Candidate Batch Score-Vector And Top-K Conformance

Stage 5V records score-vector and top-k conformance as shape and policy metadata.

## Score Vector

Score-vector rows preserve Stage 4I semantics:

- score labels remain triage-only;
- no score can imply solved plaintext;
- unavailable or unresolved scoring surfaces must remain explicit;
- score-vector output shape is deterministic across fixtures.

## Top-K

The top-k conformance row records deterministic ordering and tie-policy expectations. It does not implement a CUDA reducer and does not authorize benchmark work.

## Result Store Boundary

Stage 5V result-store conformance records keep generated result bodies ignored. Only compact metadata and hashes are committed.

Stage 5W keeps the same boundary for prime-minus-one preparation: score-summary and result-store compatibility are preflight records only, and no generated result body is committed.
