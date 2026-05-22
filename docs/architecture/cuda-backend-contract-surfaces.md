# CUDA Backend Contract Surfaces

Stage 5U assigns ownership and validation boundaries for future Candidate Batch ABI backends.

## Surfaces

- Python orchestration owns manifests, provenance, validation, result-store writes, and report generation.
- Native C++ reference backend is the next no-GPU conformance surface for Stage 5V.
- CUDA host runner may only marshal buffers in a future explicit stage.
- CUDA device kernels must use conservative CUDA-C style and explicit buffers.
- Result-store and score-summary surfaces remain compact metadata only.
- Generated body policy keeps full generated token/text bodies ignored and unpublished.

C++ must not launch Python worker scripts. Stage 5U permits no backend execution.
