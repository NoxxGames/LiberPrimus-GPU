# CUDA Solved-Family Readiness Matrix

Stage 5T converts the Stage 5M through Stage 5S CUDA parity arc review into a metadata-only solved-family readiness matrix.

The matrix answers one narrow question: which committed solved-family surfaces have enough CPU/native/reference evidence to support future CUDA contract work? It does not execute CUDA, modify CUDA source, add kernels, run benchmarks, publish generated result bodies, or claim solve evidence.

## Current Classification

Stage 5T records eight solved-family inventory rows and eight parity-matrix rows:

- `gematria_shift_score_only`: verified against the existing `gematria_mod29_shift_score_kernel` over the Stage 5M and Stage 5R solved-fixture-safe token buffers.
- `synthetic_shift_score`: verified existing synthetic uppercase-Latin kernel surface from Stage 5F.
- `synthetic_gematria_mod29`: verified existing synthetic numeric Gematria surface from Stage 5J.
- `direct_translation`: useful as a solved-fixture source for token buffers, but its original transform semantics are not CUDA-verified.
- `vigenere_explicit_key`: high-value future family, blocked on key-schedule ABI and a separate CUDA contract.
- `prime_minus_one_stream`: high-value future family, blocked on stream-schedule ABI and a separate CUDA contract.
- `reverse_gematria`: CPU/reference-ready, but needs an original-family CUDA contract.
- `rotated_reverse_gematria`: CPU/reference-ready, but needs rotation parameter ABI and an original-family CUDA contract.

## Boundary

`gematria_shift_score_only` parity must not be described as original transform-family CUDA parity for direct translation, reverse Gematria, Vigenere, or prime-stream semantics. Stage 5T records current-kernel parity separately from future original-family contracts.

Generated reports remain ignored under `experiments/results/cuda-solved-family-readiness/stage5t/`.

## Stage 5U Follow-Up

Stage 5U consumes the five ABI gap rows from the Stage 5T matrix and defines Candidate Batch ABI v0 contracts for token buffers, key schedules, stream schedules, score vectors, top-k output, backend surfaces, and result-store compatibility. It closes the Stage 5T gaps only at the contract level and selects Stage 5V native ABI conformance fixtures as the next bounded step.
