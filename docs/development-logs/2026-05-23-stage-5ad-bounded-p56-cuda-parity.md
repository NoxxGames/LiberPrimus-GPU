# Stage 5AD Development Log

Stage 5AD added bounded p56 CUDA parity records and CLI support around the existing prime-minus-one CUDA kernel. The stage reused existing device code, added a bounded host/test target, generated ignored reports, and committed compact YAML records only.

The bounded vector ran locally and produced a hash mismatch:

- expected Stage 5X hash: `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`
- computed CUDA hash: `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`
- parity status: `failed_hash_mismatch`

The selected next stage is `Stage 5AD-fix - bounded p56 CUDA parity mismatch investigation`. Full p56, unsolved pages, benchmarks, scored experiments, generated-output publication, website expansion, method-status upgrades, canonical corpus activation, page-boundary finalisation, and solve claims remain blocked.
