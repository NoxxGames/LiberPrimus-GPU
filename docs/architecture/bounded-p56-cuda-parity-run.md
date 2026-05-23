# Bounded P56 CUDA Parity Run

Stage 5AD runs exactly one prime-minus-one CUDA parity vector:

- validation vector: `stage5z-validation-p56-bounded-v0`
- mapping: `stage5w-mapping-p56-stage4o-bounded-v0`
- fixture: `p56-an-end-prime-minus-one`
- candidate: `stage4o-prime-minus-one-an-v0`

The run reuses the existing `prime_minus_one_stream_kernel_v0` implementation. It adds host/test plumbing for the bounded vector but does not add a new CUDA kernel and does not alter CUDA device arithmetic.

The Stage 5X expected output-token hash is:

`4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`

The local Stage 5AD CUDA run produced:

`6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`

That mismatch is recorded as `failed_hash_mismatch`. It is correctness metadata only, not performance evidence and not a solve claim. The selected follow-up is `Stage 5AD-fix - bounded p56 CUDA parity mismatch investigation`.

Generated reports stay ignored under `experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/`.
