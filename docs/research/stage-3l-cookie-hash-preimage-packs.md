# Stage 3L Cookie Hash Preimage Packs

Research purpose: test whether the archived 2013 `167` and `761` cookie/hash artefacts have a simple historically motivated SHA-256 preimage in two small explicit packs.

Result:

- Algorithm: `sha256`
- Cookie targets: `2`
- Candidate packs: `2`
- Generated candidates before deduplication: `1968`
- Deduplicated candidates: `1809`
- Comparisons: `3618`
- Exact matches: `0`

Interpretation:

No exact SHA-256 preimage was found in the bounded Stage 3L packs. This does not prove the cookie values are not hashes, nor that SHA-256 is impossible. It only falsifies this specific explicit candidate set.

No near-match, partial-match, or solve claim is made.
