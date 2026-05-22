# Stage 5U Next-Stage Decision Summary

Stage 5U selects `Stage 5V - native candidate batch ABI reference adapter and conformance fixtures`.

Rationale:

- Stage 5T identified five shared ABI gaps across token buffers, key schedules, stream schedules, score vectors, and top-k outputs.
- Stage 5U closes those gaps by contract records.
- The next safe step is a no-GPU native reference adapter and conformance-fixture layer that exercises the ABI without CUDA execution.

Deferred or blocked directions:

- Additional `shift_score` widening remains deferred.
- Original-family CUDA contracts remain deferred until native ABI conformance fixtures exist.
- GPU benchmarks remain deferred until parity and benchmark-planning gates are explicitly satisfied.
- Unsolved-page CUDA remains blocked.
- Website expansion and generated-body publication remain out of scope.
