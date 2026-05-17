# Stage 3B Result Summary

Date: 2026-05-16

## Stage 3A Inspection

- Source run ID: `stage3a-stage2j-caesar-affine-first-reviewable-slice-20260517T025531Z`
- Candidate count inspected: `841`
- Original top lead: `affine_mod29`, parameters `a=25`, `b=1`, score `33.353307`
- Original top lead had no separator or space context.
- Top 25 candidates were dominated by affine transforms: affine `24`, Caesar `1`.
- Qualitative inspection label: `weak_noisy`

Interpretation: the Stage 3A top lead is not readable English and appears to be driven by accidental embedded short common-word fragments in a flat rune-label stream. It is a lead only, not solve evidence.

## Refined Rerank

- Rerank executed against the generated ignored Stage 3A candidate records.
- Refined top lead: `affine_mod29`, parameters `a=19`, `b=26`
- Refined total score: `8.040756`
- Refined length-normalized score: `6.245247`
- Confidence label: `noisy`
- Top candidate changed: true

Interpretation: the refined scorer penalizes the missing separator context and reduces the original top lead. The reranked result remains noisy and inconclusive.

## Reverse-Direction Run

- Run ID: `stage3b-stage3b-caesar-affine-reverse-direction-20260517T033313Z`
- Candidate count: `841`
- Caesar reverse candidates: `29`
- Affine reverse candidates: `812`
- Top reverse lead: `affine_mod29_reverse`
- Top reverse parameters: `a=26`, `a_inverse=19`, `b=20`, `direction=reverse`
- Top reverse total score: `8.040756`
- Top reverse length-normalized score: `6.245247`
- Top reverse confidence label: `noisy`

Interpretation: reverse direction did not produce a strong lead. The top reverse lead is equivalent in output hash to the refined forward rerank lead and remains noisy.

## Next Queue Decision

Stage 3B queues `stage3b-caesar-affine-reverse-direction` as the bounded comparison method and keeps `stage3b-stage3a-rerank-control` as a rerank-only control. Because both refined and reverse-direction outputs remain noisy, the recommended next stage is Stage 3C: improve scoring calibration and add null/crib-style checks before widening transform families.

No solve claim is made. CUDA was not used. Full candidate dumps remain ignored under `experiments/results/bounded-auto-runs/stage3b/`.
