# Prime-Minus-One CUDA Synthetic Host Runner

The Stage 5AA host runner is a tiny synthetic harness around `prime_minus_one_stream_kernel_v0`.

It exists to prove that the Stage 5Z synthetic validation vector can cross the CUDA boundary and return the same deterministic hash as the Stage 5X native reference. It does not load raw data, p56 buffers, solved fixture packs, unsolved pages, or generated result bodies.

CI remains no-GPU-safe: the Python CLI can record a skipped CUDA run when CUDA tools are unavailable. A local CUDA pass is useful correctness metadata, but it is not benchmark evidence.
