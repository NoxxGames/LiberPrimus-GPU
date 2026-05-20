# Stage 5I Gematria CUDA ABI Plan Summary

Stage 5I records one CUDA-C ABI plan for the future `gematria_mod29_shift_score_kernel`.

The planned boundary uses raw `uint8_t` token buffers, `uint8_t` transformable masks, `uint8_t`
shift candidates, candidate-major output buffers, explicit token/candidate counts, and integer
status codes. Host ownership and output hashing stay host-side.

No `.cu` or `.cuh` file was added in Stage 5I.
