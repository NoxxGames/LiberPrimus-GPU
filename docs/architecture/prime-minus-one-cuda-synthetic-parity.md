# Prime-Minus-One CUDA Synthetic Parity

Stage 5AA parity compares the host-computed synthetic CUDA output-token hash against the Stage 5Z validation hash.

Local Stage 5AA result:

- synthetic vector: `stage5z-validation-synthetic-prime-control-v0`
- CUDA attempted/pass/fail/skip: `1/1/0/0`
- expected hash: `06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab`
- computed hash: `06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab`
- parity status: `passed`

Passing this synthetic vector selects Stage 5AB reporting/preflight. It does not authorize p56/full-p56 execution, scored experiments, benchmarks, unsolved-page CUDA, or solve claims.
