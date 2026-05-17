# Stage 3C Scoring Calibration Summary

Date: 2026-05-16

## Scope

Stage 3C calibrated minimal triage scoring before widening transform families. It used committed solved-fixture expected plaintext and safe synthetic readable strings as positive controls, deterministic local null controls, synthetic negative controls, and the Stage 3A/3B top candidates.

No CUDA, cloud service, large dictionary, external API, canonical corpus activation, page-boundary finalization, or solve claim was used.

## Control Counts

- Positive controls: `12`
- Null controls: `250`
- Negative controls: `4`
- Stage 3 candidate records calibrated: `3`

## Score Ranges

- Positive-control length-normalized score range: `4.806942` to `29.310739`, mean `19.142369`
- Null-control length-normalized score range: `1.163663` to `11.299382`, mean `5.917973`
- Negative-control length-normalized score range: `-21.268966` to `0.560659`, mean `-9.135780`

## Candidate Classifications

- Stage 3A original top lead: `noisy`
- Stage 3A refined/reranked top lead: `noisy`
- Stage 3B reverse-direction top lead: `noisy`

These classifications support the Stage 3B judgment that the current Caesar plus affine leads do not look solved-like under calibrated controls.

## Generated Outputs

Full calibration outputs remain ignored under:

- `experiments/results/scoring-calibration/stage3c/positive_control_scores.jsonl`
- `experiments/results/scoring-calibration/stage3c/null_control_scores.jsonl`
- `experiments/results/scoring-calibration/stage3c/negative_control_scores.jsonl`
- `experiments/results/scoring-calibration/stage3c/stage3_candidates_calibrated.jsonl`
- `experiments/results/scoring-calibration/stage3c/calibration_summary.json`

## Recommended Next Step

Stage 3D should run the conservative small Vigenere known-motif key-list preview with calibrated scoring. Candidate count should remain small, CPU-only, generated outputs ignored, and top candidates treated as leads only.

No solve claim is made.
