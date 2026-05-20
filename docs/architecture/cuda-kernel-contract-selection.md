# CUDA Kernel Contract Selection

Stage 5E chooses a first kernel contract by joining existing readiness surfaces:

- Stage 5A target plans, parity scaffolds, non-targets, and implementation gates.
- Stage 5B harness plans, parity fixtures, backend capability profiles, and future-kernel matrix.
- Stage 5C build/device records.
- Stage 5D native CPU backend and deterministic threading records.
- Stage 4O parity expectations and Stage 4P unified result references.

The selected target is `shift_score_kernel` because the `caesar_mod29` shift-score path is the
smallest regular future kernel candidate with stable CPU/native parity inputs. Stage 5E records
`3` alternate candidates and `10` blocked or rejected candidates rather than forcing a broader
first-kernel surface.

Future Stage 5F work may target only this selected synthetic-only contract unless a later explicit
stage updates the contract. Contract selection does not authorize GPU benchmarks, raw-data
processing, broad searches, or speedup claims.
