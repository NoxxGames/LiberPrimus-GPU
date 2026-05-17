# Stage 3L Cookie Hash Preimage Summary

Stage 3L ran bounded SHA-256-only preimage packs against the two archived 2013 cookie/hash artefacts recorded in Stage 3K.

Targets tested:

- `cookie-2013-167-v0`
- `cookie-2013-761-v0`

Algorithm tested:

- `sha256`

Packs run:

- `hist_cookie_literal_pack_v1`
- `hist_cookie_base29_numeric_pack_v1`

Candidate counts:

- Generated before deduplication: `1968`
- Deduplicated candidates tested: `1809`
- Duplicate byte-string candidates recorded: `159`
- Target comparisons: `3618`

Result:

- Exact SHA-256 matches: `0`
- Zero exact SHA-256 matches were found.
- No fuzzy, partial, or near-match claims were made.

Generated output paths:

- `experiments/results/hash-preimage/stage3l/hash_candidate_records.jsonl`
- `experiments/results/hash-preimage/stage3l/exact_matches.jsonl`
- `experiments/results/hash-preimage/stage3l/summary.json`
- `experiments/results/hash-preimage/stage3l/warnings.jsonl`

Generated outputs are ignored and are not committed.

No solve claim is made. The cookie/hash values remain archived claims with unknown preimage status.
