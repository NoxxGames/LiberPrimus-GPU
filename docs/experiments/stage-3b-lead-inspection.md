# Stage 3B Lead Inspection

Stage 3B inspects the ignored Stage 3A Caesar plus affine candidate outputs and records only summary-level conclusions.

The original Stage 3A top lead was `affine_mod29` with parameters `a=25`, `b=1`, score `33.353307`. Inspection found no separator or space context and top-candidate dominance by affine transforms. The result is treated as weak/noisy, not as plaintext evidence.

## Rerank

The refined scorer reranked the Stage 3A candidates into ignored Stage 3B outputs. The refined top lead changed to `affine_mod29` with `a=19`, `b=26`, score `8.040756`, confidence label `noisy`.

## Reverse Direction

Stage 3B queues and runs `stage3b-caesar-affine-reverse-direction` as a bounded comparison. It uses the same reviewable slice, generates `841` candidates, and writes outputs under `experiments/results/bounded-auto-runs/stage3b/reverse_direction/`.

The reverse-direction top lead is `affine_mod29_reverse`, parameters `a=26`, `a_inverse=19`, `b=20`, score `8.040756`, confidence label `noisy`.

## Interpretation

Stage 3B does not identify a strong candidate. The next stage should improve scoring calibration and add null/crib-style checks before widening transform families.
