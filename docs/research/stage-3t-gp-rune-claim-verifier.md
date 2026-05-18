# Stage 3T GP/Rune Claim Verifier

Stage 3T executes `EXP-3R-004`, a bounded verifier for promoted GP-sum, rune-count, prime-status, and derived numeric claims.

## Research Question

Which promoted numeric claims can be exactly recomputed from committed review records and profiles without treating Discord-derived leads as facts?

## Method

The verifier loads the Stage 3R manifest, promoted observation records, visual numeric observations, and the Gematria Primus profile. It supports exact rune-index spans for rune counts and GP sums, plus explicit derived-value checks such as the cuneiform `[17, 13, 55, 1]` arithmetic. It classifies unsupported visual motif claims instead of forcing them into numeric evidence.

The verifier does not search neighbouring spans, infer missing spans, fuzz boundaries, process raw Discord logs, process raw images, use CUDA, or claim solves.

## Local Result

- Claims loaded: `25`
- Claims deduplicated: `25`
- Verified: `23`
- Unverified: `0`
- Boundary-sensitive: `0`
- Missing-source-span: `0`
- Unsupported: `2`
- Malformed: `0`
- Duplicates: `0`

The two unsupported claims are visual motif observations with no exact GP/rune claim to recompute. The verified claims are arithmetic or prime-status checks over explicit committed values; they are evidence hygiene, not solve evidence.

## Output Policy

Generated verification JSONL and summary JSON remain ignored under `experiments/results/post-discord/stage3t/`. The committed research log contains counts and representative claim IDs only.
