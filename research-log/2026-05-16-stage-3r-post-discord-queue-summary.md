# Stage 3R Post-Discord Queue Summary

Stage 3R created exactly three disabled post-Discord experiment manifests:

- `EXP-3R-001 cookie_sha256_signed_variants_a`
  - Candidate cap: `576`
  - SHA-256 exact-match only
  - Execution enabled: `false`
- `EXP-3R-003 onion7_raw_prime_order_seed_pack_a`
  - Candidate cap: `144`
  - Candidate estimate: `72`
  - Execution enabled: `false`
- `EXP-3R-004 gp_rune_claim_verifier_a`
  - Claim cap: `64`
  - Execution enabled: `false`

All three manifests keep `cpu_only=true`, `cuda_enabled=false`, `cloud_execution=false`, `paid_services=false`, `generated_outputs_committed=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

Stage 3R queues these manifests only. It does not execute them and makes no solve claim.
