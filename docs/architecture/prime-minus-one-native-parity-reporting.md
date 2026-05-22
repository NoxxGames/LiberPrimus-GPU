# Prime-Minus-One Native Parity Reporting

Stage 5Y is the compact reporting layer over Stage 5X no-GPU prime-minus-one native parity. It consumes committed Stage 5X records and writes metadata-only summaries that can be used by result-store, score-summary, and future CUDA contract planning stages.

It does not execute parity again. It does not run CMake, native C++, CUDA, GPU tools, benchmarks, raw transcripts, full p56, or unsolved pages.

## Records

- `data/cuda/stage5y-prime-minus-one-native-parity-report.yaml`
- `data/cuda/stage5y-prime-minus-one-native-result-store-integration.yaml`
- `data/cuda/stage5y-prime-minus-one-native-score-summary-integration.yaml`
- `data/cuda/stage5y-prime-minus-one-native-reporting-summary.yaml`

Generated JSON reports are ignored under `experiments/results/prime-minus-one-native-reporting/stage5y/`.

## Policy

Only compact hashes, status fields, source IDs, and gate decisions are committed. Generated result bodies, token arrays, raw data, SQLite databases, and `codex-output/**` handoffs remain ignored.
