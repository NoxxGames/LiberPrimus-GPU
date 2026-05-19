# Stage 4G Cookie Exact-Candidate Refresh Summary

Stage 4G executed the bounded cookie refresh against the historical `167` and `761` cookie artefacts.

Inputs:

- `experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml`
- `data/observations/web/stage4b-cookie-candidate-source-records.yaml`
- `data/observations/web/cookie-hash-records-v0.yaml`

Results:

- Target cookies: `2`
- Source-backed base strings: `4`
- Byte variants: `1` (`raw`)
- Algorithms: `sha256`
- Generated candidates before deduplication: `4`
- Candidates after deduplication: `4`
- Duplicate candidates: `0`
- Previous-pack duplicates: `2`
- Comparisons: `8`
- Exact matches: `0`

Interpretation:

Stage 4G is a negative exact-match result. It does not prove anything about the historical cookie
artefacts, but it keeps the SHA-256 cookie pack family negative/deprioritised unless new exact
source-backed strings are locked later.

Policy:

- no fuzzy matching
- no partial matching
- no hashcat
- no GPU/CUDA
- no dictionary expansion
- no raw Discord processing
- no raw page-image processing
- no solve claim

Generated JSON/JSONL outputs remain ignored under `experiments/results/cookie-refresh/stage4g/`.
