# Native Candidate Batch ABI Reference Adapter

Stage 5V records the first no-GPU Candidate Batch ABI reference adapter surface.

The implemented adapter is a pure Python reference path for raw-data-free fixtures. It validates shared ABI behavior before family-specific native or CUDA contracts are widened. The C++ reference adapter remains explicitly deferred.

## Scope

- Consume Stage 5U Candidate Batch ABI v0 contracts.
- Preserve candidate-major output ordering.
- Preserve token values, token kinds, separator placeholders, transformable masks, fixture offsets, and fixture lengths.
- Produce deterministic output-token hashes for executed `shift_mod29` fixtures.
- Record shape-only coverage for key schedule, stream schedule, score-vector, and top-k surfaces.
- Keep compact result-store metadata separate from generated result bodies.

## Boundaries

- `python_reference_adapter_implemented=true`
- `cpp_reference_adapter_implemented=false`
- `native_cpu_execution_performed=false`
- `cuda_execution_performed=false`
- `cuda_source_modified=false`
- `new_cuda_kernels_added=0`

Stage 5V does not run CUDA, does not run native/CUDA CMake, does not benchmark, and does not authorize unsolved-page CUDA or original transform-family CUDA semantics.

Stage 5W consumes this conformance surface for the prime-minus-one stream family. It prepares contract metadata only; the next executable step is Stage 5X no-GPU native parity execution scoped by Stage 5W records.
