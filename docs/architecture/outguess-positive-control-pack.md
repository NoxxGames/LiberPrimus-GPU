# OutGuess Positive-Control Pack

Stage 5AP adds OutGuess positive-control infrastructure for future controlled checks. It does not run OutGuess against Liber Primus page images or historical fixtures.

Committed records:

- `data/stego/stage5ap-outguess-positive-control-policy.yaml`
- `data/stego/stage5ap-outguess-toolchain-readiness.yaml`
- `data/stego/stage5ap-outguess-positive-control-matrix.yaml`
- `data/stego/stage5ap-outguess-historical-fixture-readiness.yaml`
- `data/stego/stage5ap-outguess-guardrail.yaml`

The matrix separates synthetic controls from historical fixtures. Synthetic controls can be used for raw-data-free tests. Historical fixtures remain blocked unless assets, expected payload hashes, and toolchain readiness are source-locked by a future explicit stage.

Stage 5AP recorded the local OutGuess state as `outguess_missing`. This is not a failure for source-lock readiness; it keeps future execution blocked until the toolchain and expected outputs are reproducible.
