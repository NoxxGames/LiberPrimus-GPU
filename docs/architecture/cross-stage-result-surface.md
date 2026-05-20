# Cross Stage Result Surface

The Stage 4P cross-stage result surface makes older result-store records, bounded summaries, scoring records, CPU batch parity records, observation summaries, image preflight summaries, fixture readiness summaries, and method ledgers comparable without reinterpreting them.

## Normalized Shape

Each unified result records:

- source stage and source record type;
- source path and source presence status;
- result source kind;
- method family and transform family when known;
- candidate and result counts when available;
- score-summary availability and confidence label when available;
- method status and retirement status when known;
- output hashes and parity expectation references when present;
- explicit no-CUDA, no-solve, no-canonical-corpus, and no-generated-output-publication flags.

The join is conservative. Missing method families remain `unknown` with warnings rather than guessed.

## Report Use

The cross-stage report is a triage and planning aid. It can show where a family is noisy, negative, inconclusive, retired, blocked, or infrastructure-only, but it cannot promote a result, revive a method family, or prove plaintext.

Future CUDA planning should reference both Stage 4O parity expectations and Stage 4P unified result surfaces before any benchmark or kernel work is trusted.

