# Stage 3D Small Vigenere Key List

Stage 3D runs the conservative Stage 3C queue item `stage3c-small-vigenere-known-motif-key-list`.

This is an explicit-list bounded CPU preview, not a Vigenere key search. The only keys tested are:

- `LIBER`
- `PRIMUS`
- `DIVINITY`
- `CICADA`

The queue declares `candidate_count_upper_bound: 4`, `cpu_only: true`, `cuda_enabled: false`, `cloud_execution: false`, `generated_outputs_committed: false`, and `no_solve_claim: true`.

## Input Slice

The run uses the same reviewable input slice selected for Stage 3A:

- slice ID: `stage3a-page-candidate-018-reviewable-slice`
- page candidate: `page-candidate-018`
- expected rune token count: `87`

The committed queue stores selector metadata only. It does not include raw unsolved text.

## Execution

The bounded runner applies explicit-key Vigenere over Gematria index values with decrypt-subtract convention:

```text
decoded_index = (cipher_index - key_index[key_position]) mod 29
```

The current input slice is a flat rune index stream, so key position advances once per rune index. Separator context is not available for this slice and is recorded as a warning.

## Output Policy

Generated files remain ignored under:

```text
experiments/results/bounded-auto-runs/stage3d/
```

The generated files include candidate JSONL, top-candidate JSONL, score details, warnings, and a summary JSON. These files are local experiment outputs and must not be committed.

## Result Interpretation

Calibrated scores are triage metadata only. Key-list hits are leads only, not solve claims. Stage 3D does not activate the canonical corpus, finalize page boundaries, use CUDA, or publish candidate text as a solution.
