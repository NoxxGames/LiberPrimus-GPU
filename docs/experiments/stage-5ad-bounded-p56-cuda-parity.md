# Stage 5AD Bounded P56 CUDA Parity

Stage 5AD is a bounded parity execution stage. It runs the existing prime-minus-one CUDA kernel only for `stage5z-validation-p56-bounded-v0` and compares the host-computed output-token hash against the Stage 5X reference hash.

Local result:

- CUDA attempted/pass/fail/skip: `1/0/1/0`
- parity status: `failed_hash_mismatch`
- expected Stage 5X hash: `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`
- computed CUDA hash: `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`
- CUDA source modified: `false`
- new CUDA kernels: `0`

The mismatch is the experiment outcome. No full p56, unsolved-page CUDA, scored experiment, benchmark, generated-output publication, or solve claim was made.
