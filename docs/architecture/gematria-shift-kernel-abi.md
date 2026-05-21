# Gematria Shift Kernel ABI

Stage 5I plans a conservative CUDA-C ABI for a future Gematria mod-29 `shift_score` kernel. Stage
5J implements that ABI for one synthetic numeric parity path while keeping solved-fixture-safe and
real page execution blocked.

## Planned Kernel Boundary

```text
gematria_shift_score_kernel(
    const uint8_t* token_values,
    const uint8_t* transformable_mask,
    const uint8_t* shifts,
    uint8_t* output_token_values,
    int token_count,
    int candidate_count,
    int* status_codes)
```

The output is candidate-major:

```text
output[candidate_index * token_count + token_index]
```

The device formula is:

```text
mask ? (token + shift) % 29 : token
```

## Ownership

Host-side C++ may own buffers outside CUDA-facing files. `.cu` and `.cuh` kernel/device paths must
use raw pointers, explicit counts, simple integer status codes, and the Stage 5G conservative
CUDA-C subset.

Stage 5I creates no future header or source file. The planned paths are
`cuda/include/libreprimus/gematria_shift_score_kernel.cuh` and
`cuda/kernels/gematria_shift_score_kernel.cu` for a later explicit implementation stage.
