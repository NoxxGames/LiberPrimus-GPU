# Prime-Minus-One CUDA Kernel ABI

Stage 5Z records a CUDA-C style ABI for a future `prime_minus_one_stream_candidate_kernel`.

The ABI uses raw numeric token buffers, token-kind buffers, transformable masks, fixture offsets/lengths, stream schedule values, candidate fixture references, candidate stream starts, candidate-major output buffers, and status codes. Output hashes are host-side `sha256_canonical_json_v1` records.

The ABI forbids STL containers, strings, exceptions, RTTI, lambdas, dynamic allocation, and iostreams in CUDA-facing `.cu`/`.cuh` device paths. The ABI record is not a kernel implementation.
