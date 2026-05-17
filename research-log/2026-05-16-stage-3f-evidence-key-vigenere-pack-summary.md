# Stage 3F Evidence-Key Vigenere Pack Summary

Date: 2026-05-16

## Run

- Run ID: `stage3f-stage3e_vig_lp_evidence_pack_v1-20260517T143322Z`
- Queue item: `stage3e_vig_lp_evidence_pack_v1`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Keys tested: `DIVINITY`, `FIRFUMFERENFE`, `PARABLE`, `INSTAR`, `EMERGE`, `WITHIN`, `WELCOME`, `PILGRIM`, `TOTIENT`, `PRIMES`, `SACRED`, `ENCRYPTED`
- Reset modes tested: `none`, `line`
- Advance modes tested: `runes_only`, `token_break_preserving`
- Expected candidates: `48`
- Executed candidates: `48`
- Deferred candidates: `0`

## Top Lead

- Top key: `EMERGE`
- Top reset mode: `none`
- Top advance mode: `runes_only`
- Total score: `6.800831`
- Length-normalized score: `5.495621`
- Raw triage label: `garbage`
- Calibrated confidence label: `noisy`
- Crib hits: `0`

## Interpretation

The Stage 3F evidence-key Vigenere pack executed the full bounded LP evidence pack without deferred reset or advance modes. The top candidate is still classified `noisy` by the Stage 3C calibrated scorer, so this run does not provide solve evidence. The result supports moving to the next bounded method rather than expanding Vigenere keys.

## Generated Outputs

Full generated records remain ignored locally under:

- `experiments/results/bounded-auto-runs/stage3f/candidate_records.jsonl`
- `experiments/results/bounded-auto-runs/stage3f/top_candidates.jsonl`
- `experiments/results/bounded-auto-runs/stage3f/calibrated_scores.jsonl`
- `experiments/results/bounded-auto-runs/stage3f/summary.json`
- `experiments/results/bounded-auto-runs/stage3f/result_store_preview.json`

No full candidate dumps are committed. No solve claim is made.
