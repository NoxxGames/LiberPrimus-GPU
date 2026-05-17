# Stage 3F Evidence-Key Vigenere Pack

Stage 3F implements the bounded executor for `stage3e_vig_lp_evidence_pack_v1`.

## Scope

- Transform family: explicit-key Vigenere key pack.
- Keys: the 12 LP evidence keys declared in `experiments/queues/stage3e-bounded-cpu-queue.yaml`.
- Reset modes: `none`, `line`.
- Advance modes: `runes_only`, `token_break_preserving`.
- Candidate count: `12 * 2 * 2 = 48`.
- Execution: local CPU only.
- CUDA: disabled.
- Solve claims: disabled.

## Semantics

The executor uses decrypt-subtract Vigenere over the Gematria index ring:

```text
output_index = (cipher_index - key_index[key_position]) mod 29
```

`runes_only` advances the key only on rune/index tokens. `token_break_preserving` preserves available token-break metadata and still advances only on transformable rune tokens. `line` reset restarts the key position at line boundaries; if line metadata is unavailable, those candidates are deferred instead of inventing boundaries.

## Result

The Stage 3F local run executed all `48` expected candidates against `stage3a-page-candidate-018-reviewable-slice`; no reset or advance mode was deferred. The top lead used key `EMERGE`, reset mode `none`, and advance mode `runes_only`, but it remained `noisy` under calibrated scoring.

Generated outputs are ignored under `experiments/results/bounded-auto-runs/stage3f/`. The committed record is the summary-only research log.

## Stop Conditions

Do not expand the key list, add dictionary search, add skip masks, use CUDA, activate the canonical corpus, finalize page boundaries, or claim a solve from Stage 3F output.
