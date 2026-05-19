# Stage 4I Scorer Consolidation Summary

Date: 2026-05-18

Stage 4I consolidated existing scoring behavior into durable records without introducing a new scorer. It inventoried the minimal triage scorer, Stage 3C calibration classifier, and crib-check component; added finite confidence labels; and mapped legacy labels into the Stage 4I score-summary contract.

## Local Run

- Scorer records: `3`
- Confidence labels: `9`
- Compatibility mappings: `11`
- CPU batch compatibility: `true`
- Generated outputs: `experiments/results/scoring-consolidation/stage4i/` and ignored
- Raw data staged: `0`
- Solve claim: `false`
- CUDA used: `false`

## Notes

The CPU batch scoring adapter now records Stage 4I scorer/profile metadata while preserving the legacy confidence label. Scoring remains a triage aid only and does not validate plaintext.
