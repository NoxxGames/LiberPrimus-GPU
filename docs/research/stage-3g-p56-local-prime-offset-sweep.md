# Stage 3G p56-local prime offset sweep

Stage 3G tests the next bounded method selected after the noisy Stage 3F Vigenere evidence-key run: a p56-local prime-minus-one offset sweep over the same reviewable slice used in Stages 3A through 3F.

The method stays local CPU-only and manifest-bound:

- Stream: `prime_minus_one`
- Offsets: `0..63`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`
- Candidate count: `256`
- Scoring: calibrated triage from Stage 3C

The run generated ignored local candidate outputs and a committed summary-only research log. It did not activate a canonical corpus, finalize page boundaries, use CUDA, or claim a solve.

The top Stage 3G candidate is an `inconclusive` lead, not a solution. The next step should either inspect the p56 top candidates as leads or proceed to reset/advance ablation or family-specific negative controls before considering lower-priority stream probes.
