# Stage 4G Cookie Exact-Candidate Refresh

Stage 4G refreshes the historical Cicada cookie artefact check with only source-backed strings from
Stage 4B and existing cookie records.

Inputs:

- `experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml`
- `data/observations/web/stage4b-cookie-candidate-source-records.yaml`
- `data/observations/web/cookie-hash-records-v0.yaml`

Run summary:

- Target cookies: `2`
- Source-backed base strings: `4`
- Byte variants: `raw`
- Algorithms: `sha256`
- Generated candidates before deduplication: `4`
- Candidates after deduplication: `4`
- Previous-pack duplicates: `2`
- Exact comparisons: `8`
- Exact matches: `0`

Policy:

- exact-match only
- no fuzzy or partial hash matching
- no dictionary expansion
- no hashcat
- no GPU/CUDA
- no live Tor or live web scraping
- no solve claim

Generated candidate records, exact-match records, duplicate records, warnings, and generated summary
JSON remain ignored under `experiments/results/cookie-refresh/stage4g/`. The committed aggregate
summary is `data/observations/web/stage4g-cookie-refresh-summary.yaml`.

Because the exact-match count is zero, the cookie SHA-256 exact-pack family remains negative and
deprioritised unless newly source-locked exact candidate strings appear.
