# Prime-Minus-One CUDA Host-Runner Contract

Stage 5Z records the future host-runner boundary without implementing it. Python remains orchestration. C++ must not launch Python workers. Any future host runner must validate buffers, preserve status-code semantics, compute host-side output hashes, and write compact result-store metadata only.

Generated result bodies, raw inputs, SQLite files, and `codex-output/**` handoffs remain ignored and uncommitted.
