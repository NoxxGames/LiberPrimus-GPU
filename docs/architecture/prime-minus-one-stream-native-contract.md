# Prime-Minus-One Stream Native Contract

Stage 5W prepares a native parity contract for `prime_minus_one_stream`.

The contract is source-backed and raw-data-free. It records the stream formula `(prime_i - 1) mod 29`, source-backed decryption direction, token-advance policy, separator/skip policy, Candidate Batch ABI v0 mapping, and result-store preflight records. It does not execute native parity and does not authorize CUDA.

## Boundary

- `cuda_execution_performed=false`
- `cuda_source_modified=false`
- `new_cuda_kernels_added=0`
- `native_execution_performed=false`
- `raw_data_processed=false`
- `solve_claim=false`

The bounded p56 Stage 4O/5L mapping was consumed by Stage 5X no-GPU native parity execution. Full p56 parity remains blocked until a full committed p56 cipher token buffer is explicitly scoped.
