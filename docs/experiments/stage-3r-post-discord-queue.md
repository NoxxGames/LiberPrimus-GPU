# Stage 3R Post-Discord Queue

Stage 3R creates the first three bounded post-Discord experiment manifests. They are queued only; execution is disabled.

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

Stage 3S may execute one manifest explicitly, such as `EXP-3R-003` or `EXP-3R-001`, after reviewing the manifest and confirming candidate bounds.
