# CUDA Device-Code Subset Policy

Stage 5G hardens CUDA-facing source toward a conservative CUDA-C style subset. The policy applies to `.cu` and `.cuh` files unless a later stage explicitly marks a file as host-only and keeps it out of device compilation.

## Required Style

CUDA-facing files should use:

- POD structs
- fixed-size C arrays
- raw pointers
- explicit counts and capacities
- explicit output buffers
- primitive integer and character types
- integer status codes at ABI boundaries

## Disallowed In CUDA-Facing Paths

The Stage 5G audit rejects STL and convenience C++ in `.cu` and `.cuh` paths:

- STL containers or strings
- `std::array`, `std::vector`, `std::string`, `std::span`, `std::optional`, `std::variant`
- standard iostream/sstream formatting
- exceptions and `throw`
- lambdas
- dynamic allocation
- C++ ownership types crossing kernel boundaries

Host-side C++ convenience code belongs in ordinary `.cpp`/`.hpp` files that do not define the CUDA-facing ABI.

## Current Audit

The committed audit is `data/cuda/stage5g-cuda-device-code-subset-audit.yaml`. It scans the Stage 5G CUDA-facing source list and records:

- `device_code_subset_compliant=true`
- `stl_used_in_cuda_device_path=false`
- `std_array_used_in_cuda_device_path=false`
- `cxx_exceptions_in_cuda_device_path=false`
- `dynamic_allocation_in_device_code=false`
- `new_cuda_kernels_added=0`

This audit is a style and boundary check. It is not throughput evidence and does not authorize broader CUDA execution.

## Stage 5H Requirement

The Stage 5H Gematria contract does not change CUDA-facing source. Future Gematria CUDA parity work
must keep this conservative CUDA-C subset compliant before any additional kernel target is accepted.
