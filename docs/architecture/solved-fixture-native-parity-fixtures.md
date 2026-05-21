# Solved-Fixture Native Parity Fixtures

Stage 5L prepares CPU/native output-token hash records for the mapped solved-fixture-safe Gematria
streams. These records are future parity inputs, not GPU results.

Each native parity record includes:

- source mapping and input stream identifiers
- candidate shifts `0, 1, 3, 13, 28`
- candidate-major output token records
- preserved token kind and separator metadata
- an output-token hash using `sha256_canonical_json_v1`
- Stage 4O candidate linkage where available
- `solved_fixture_cuda_execution_allowed=false`

The records intentionally do not include an output text hash because the Stage 5L parity material is
the token stream shape. Text rendering remains a higher-level reporting concern and cannot be used
to reinterpret a score as solve evidence.

Future CUDA stages must compare GPU output tokens against these native hashes and must keep Stage
4I confidence labels triage-only.
