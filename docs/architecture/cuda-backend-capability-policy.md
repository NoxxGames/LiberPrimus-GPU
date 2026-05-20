# CUDA Backend Capability Policy

Stage 5B records backend capability profiles without requiring CUDA hardware or CUDA execution.

## Profiles

- `ci_no_gpu`: CI-safe profile. Validation must pass without CUDA hardware or toolkit.
- `compatibility_8gb`: minimum planning profile for future memory-layout work.
- `local_16gb`: optional local planning metadata for the developer's RTX 4060 Ti class machine.

The local 16 GB profile is never required. It does not authorize GPU benchmarks, performance claims, speedup claims, or CUDA implementation work.

## Future Use

Stage 5C adds CUDA build and device-detection scaffolding. Stage 5D adds native CPU backend and deterministic threading records. Stage 5E selects the first future kernel contract. Future kernel implementation still requires an explicit stage, CPU/native references, Stage 5E contract records, parity tests, benchmark plans, and no-fast-math/default reproducibility controls.
