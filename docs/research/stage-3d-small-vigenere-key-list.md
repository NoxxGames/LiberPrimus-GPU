# Stage 3D Small Vigenere Key List

Stage 3D executes the small known-motif Vigenere key-list preview selected by Stage 3C calibration.

## Inputs

- Policy: `experiments/policies/operator-policy-v0.yaml`
- Queue: `experiments/queues/stage3c-bounded-cpu-queue.yaml`
- Queue item: `stage3c-small-vigenere-known-motif-key-list`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Candidate count: `4`

## Method

The runner loads the four manifest-declared keys and rejects key mutation or expansion. It maps each key through the Gematria profile, applies explicit-key Vigenere decrypt-subtract convention over the bounded input index stream, scores each generated candidate with the Stage 3C calibrated minimal triage scorer, and writes full generated records only to ignored output paths.

## Safety

- CPU only.
- CUDA disabled.
- No cloud or paid service.
- No broad key search.
- No generated output commit.
- No canonical corpus activation.
- No page-boundary finalization.
- No solve claim.

## Outcome

The Stage 3D local run generated four candidates. The top key was `LIBER`, with calibrated confidence `noisy`. This is not solve evidence.

The summary-only research log is `research-log/2026-05-16-stage-3d-small-vigenere-key-list-summary.md`.
