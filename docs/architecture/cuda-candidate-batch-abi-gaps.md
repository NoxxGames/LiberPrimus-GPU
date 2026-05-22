# CUDA Candidate Batch ABI Gaps

Stage 5T identifies shared ABI surfaces that block responsible future CUDA contracts.

## Blocking Surfaces

| Surface | Why It Blocks |
| --- | --- |
| `token_buffer_header` | Kernels need a shared token/mask/length descriptor before more family-specific contracts. |
| `key_schedule_buffer` | Explicit-key Vigenere needs key-token buffers and advance rules. |
| `stream_schedule_buffer` | Prime-minus-one needs stream values, start index, and advance policy surfaces. |
| `score_vector_shape` | Future GPU scoring needs a Stage 4I-compatible score-vector shape. |
| `top_k_output_shape` | Future reducers need deterministic top-k output and tie policies. |

## Stage 5U Rationale

Because multiple future families need these shared surfaces, Stage 5T selects `Stage 5U - unified candidate batch ABI and backend contract consolidation` before more CUDA contracts or benchmark work.
