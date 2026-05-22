# Stage 5V Native Candidate Batch ABI Conformance

Stage 5V is a conformance infrastructure stage, not a cryptanalytic experiment.

It consumes Stage 5U Candidate Batch ABI v0 records and writes adapter, fixture, token-buffer, schedule, score-vector, top-k, result-store, implementation-status, next-stage decision, and summary records under `data/cuda/`.

Generated reports remain ignored under `experiments/results/cuda-candidate-batch-abi-conformance/stage5v/`.

## Local Outcome

- Native adapter records: `2`
- Conformance fixture records: `7`
- Executed conformance fixtures: `3`
- Shape-only fixtures: `4`
- Token-buffer conformance records: `7`
- Schedule conformance records: `2`
- Score-vector conformance records: `7`
- Top-k conformance records: `1`
- Result-store conformance records: `3`
- Implementation-status records: `8`

Stage 5V selected Stage 5W prime-minus-one stream native parity contract preparation. It ran no CUDA, changed no CUDA source, added no kernels, ran no GPU benchmark, and made no solve claim.
