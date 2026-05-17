# Null Controls And Positive Controls

Stage 3C uses small local controls to check whether the triage scorer separates readable signal from nonsense.

## Positive Controls

Positive controls come from committed solved fixture expected plaintext and short synthetic readable strings. These controls are known-readable references, not new solves.

## Null Controls

Null controls are deterministic random and shuffled Gematria-like strings. The policy file is `data/scoring/null-control-policy-v0.yaml`, which fixes the seed, count, and length.

## Negative Controls

Negative controls include repeated-character strings, high-entropy strings, separatorless gibberish, and impossible-bigram-heavy text.

## Interpretation

A candidate that scores like null or negative controls remains noisy. A candidate that scores closer to positive controls is a lead only and still requires reproducible review before escalation.
