# OutGuess Positive-Control Readiness

Stage 4N records readiness metadata for historical OutGuess fixture candidates. It does not run OutGuess, extract payloads, scan image sets, or claim hidden content.

Committed records:

- `data/observations/stego/stage4n-outguess-positive-control-readiness.yaml`
- `data/observations/stego/stage4n-fixture-cache-records.yaml`
- `data/observations/stego/stage4n-expected-output-records.yaml`

Readiness requires a locked source, a cached or immutable fixture asset, exact expected-output metadata, documented toolchain state, and false `solve_claim`, `execution_performed`, and `tool_executed` flags. Stage 4N leaves historical OutGuess fixtures blocked where expected output hashes or cached assets are missing.

Synthetic controls are allowed for CI-safe readiness tests because they do not use historical artefacts.
