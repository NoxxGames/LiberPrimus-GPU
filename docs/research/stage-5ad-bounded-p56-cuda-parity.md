# Stage 5AD Bounded P56 CUDA Parity Research Note

Stage 5AD consumed the Stage 5AC preflight and executed the one allowed bounded p56 CUDA vector. The vector completed through CUDA build and CTest plumbing, but its output-token hash matched the kernel formula hash rather than the Stage 5X expected bounded reference hash.

This result keeps the prime-minus-one CUDA path in an infrastructure-only state. It does not upgrade the method family, does not validate full p56, and does not indicate a Liber Primus solve.

The recommended next Codex prompt is `Stage 5AD-fix - bounded p56 CUDA parity mismatch investigation`. That follow-up should compare the Stage 5X reference-mode material, Stage 5L candidate-major hash construction, Stage 5W mapping, Stage 5Z validation vector, and existing CUDA host serialization before any expansion.
