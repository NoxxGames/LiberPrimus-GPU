# Stage 3R Post-Discord Queue

Stage 3R creates the first three bounded post-Discord experiment manifests. They are queued only; execution is disabled in Stage 3R.

## Manifests

- `EXP-3R-001-cookie-sha256-signed-variants-a.yaml`
  - Candidate cap: `576`
  - SHA-256 only
  - Exact byte-string comparison only
  - Uses archived cookie/hash artefact records and public-source string candidates
- `EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml`
  - Candidate cap: `144`
  - Candidate estimate: `72`
  - Uses Onion 7 raw, prime-delta, and prime-order table value spaces after source review
- `EXP-3R-004-gp-rune-claim-verifier-a.yaml`
  - Claim cap: `64`
  - Verifies exact GP-sum and rune-count claims in a future stage

All manifests require `execution_enabled=false`, `cpu_only=true`, `cuda_enabled=false`, `cloud_execution=false`, `paid_services=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Next Step

Stage 3S executed only `EXP-3R-003`. It did not run `EXP-3R-001` or `EXP-3R-004`.

The Stage 3S run enumerated `72` Onion 7 seed-pack candidates under the `144` cap, with `0` deferred candidates. The top candidate remained calibrated `inconclusive`, so the post-Discord queue still has no solve claim.

Stage 3T executed only `EXP-3R-004`. It loaded and deduplicated `25` exact GP/rune or derived numeric claims under the `64` cap, classifying `23` as verified and `2` as unsupported. It did not run `EXP-3R-001`, rerun Onion 7, search neighbouring spans, or claim a solve.

Stage 3U executed only `EXP-3R-001`. It expanded the signed/public string variant pack to `156` candidates before deduplication, tested `105` deduplicated byte strings against `2` cookie targets for `210` exact SHA-256 comparisons, and found `0` exact matches. It did not rerun Onion 7 or the GP/rune verifier, use hashcat/CUDA, process raw logs/images, broaden strings, or claim a solve.

Future Stage 3V work can implement an OutGuess regression harness. If a later cookie pack finds an exact match, independently verify the preimage and source provenance before any broader interpretation.
