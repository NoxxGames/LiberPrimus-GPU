# Method Retirement Ledger

The method-retirement ledger is stored in `data/research/method-retirement-records-v0.yaml` and validated by `libreprimus research-synthesis validate`.

## Status Meanings

- `retired`: do not run again unless the reopen conditions are met.
- `deprioritised`: keep record of the result, but do not widen without new evidence.
- `deferred`: intentionally delayed until prerequisite infrastructure or source locks exist.
- `active_with_constraints`: still usable, but only under the recorded constraints.

## Current Guardrails

- Caesar/affine variants are noisy and should not be widened without new source evidence.
- Broad Vigenere/dictionary work is blocked without exact key evidence.
- Mersenne/perfect-number probes are low priority unless exact visual/source evidence appears.
- Cookie SHA-256 packs are negative for tried exact packs and must not broaden without explicit new candidate strings.
- CUDA is deferred until CPU batch APIs, scorer consolidation, parity tests, and benchmark plans exist.

The ledger does not make solve claims and does not replace experiment manifests. It prevents repeated expansion of methods already tested under bounded conditions.
