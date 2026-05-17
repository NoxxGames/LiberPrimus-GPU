# Stage 3C Scoring Calibration And Null Controls

## Goal

Calibrate minimal triage scoring before widening transform families.

## Inputs

- Solved fixture expected plaintext.
- Safe synthetic readable controls.
- Deterministic local null controls.
- Synthetic negative controls.
- Stage 3A and Stage 3B generated candidate leads.

## Result

The calibration run classified the Stage 3A original top lead, Stage 3A refined/reranked top lead, and Stage 3B reverse-direction top lead as `noisy`.

Positive controls occupied a higher score band than null and negative controls, while the current Stage 3A/3B leads remained close to null-like behavior because they lack separator/word structure.

## Next Step

Stage 3D should run the conservative small Vigenere known-motif key-list preview selected in `experiments/queues/stage3c-bounded-cpu-queue.yaml`.

No solve claim is made. Generated calibration outputs remain ignored. CUDA is not used.
