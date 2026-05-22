# CUDA Kernel Readiness Classification

Stage 5T ranks future CUDA work without authorizing implementation.

## Ranking

| Rank | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| 1 | `gematria_shift_score_only` | verified existing kernel | Retain as a parity control; no new implementation is needed. |
| 2 | `prime_minus_one_stream` | ready for contract review after ABI | Needs stream-schedule ABI before a responsible CUDA contract. |
| 3 | `vigenere_explicit_key` | ready for contract review after ABI | Needs key-schedule ABI before a responsible CUDA contract. |
| 4 | `reverse_gematria` | needs CUDA kernel contract | Simple original semantics, but no CUDA contract exists. |
| 5 | `rotated_reverse_gematria` | needs CUDA kernel contract | Needs rotation parameter ABI and original semantics contract. |
| 6 | `direct_translation` | not CUDA kernel priority | Useful fixture source, not a meaningful next CUDA kernel by itself. |
| 7 | `top_k_reducer` | future reducer after score vector | Belongs after score-vector shape and batch ABI are stable. |

## Guardrail

Every Stage 5T kernel-readiness record sets `implementation_allowed_now=false`. More CUDA kernel work requires an explicit later stage, stable CPU/native semantics, Stage 4I-compatible score-summary shape, and no-unsolved guardrails.
