# Stage 5AX Validation Infrastructure

Stage 5AX exists to reduce local Codex validation turnaround while preserving the project safety model.

The useful research outcome is process quality: validation can now be launched through one local command, with explicit worker caps, pytest-xdist detection, deterministic sharded fallback, separated logs, complete failure aggregation, and a safety audit proving serial-only operations were not parallelised.

The Stage 5AW-selected bounded token-block preflight work remains valid but is now Stage 5AY. Stage 5AX does not change token-block source truth, human review decisions, branch counts, canonical transcription, DWH context, or null-control requirements.

The harness is safe for read-only validation. It is not a path for running experiments, source crawling, stego/audio tooling, image interpretation, CUDA, benchmarks, scored experiments, or solve claims.
