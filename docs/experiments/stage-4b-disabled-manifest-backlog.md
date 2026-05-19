# Stage 4B Disabled Manifest Backlog

Stage 4B queues future bounded manifest candidates without executing them. These files live under `experiments/manifests/stage4b-disabled/`.

## Disabled Manifests

- `exp_stage4b_gp_rune_verifier_batch002.yaml`
- `exp_stage4b_dot_ambiguity_audit_v1.yaml`
- `exp_stage4b_delimiter_handedness_v1.yaml`
- `exp_stage4b_onion7_raw_routes_v1.yaml`
- `exp_stage4b_cookie_pack_v2.yaml`
- `exp_stage4b_cuneiform_reading_pack_v1.yaml`
- `exp_stage4b_visual_negative_controls_v1.yaml`

## Required Flags

Every queued manifest must keep:

- `execution_enabled=false`
- `cuda_enabled=false`
- `no_solve_claim=true`
- `canonical_corpus_active=false`
- `page_boundaries_final=false`

These manifests are planning records. A later explicit execution stage must validate source basis, candidate caps, stop conditions, and operator policy before running anything.

## Stage 4D Follow-Up

Stage 4D consumed this backlog conservatively:

- `exp_stage4b_gp_rune_verifier_batch002`: skipped because no exact new claims were present.
- `exp_stage4b_delimiter_handedness_v1`: audited as delimiter metadata only.
- `exp_stage4b_dot_ambiguity_audit_v1`: audited as ambiguity metadata only.
- `exp_stage4b_onion7_raw_routes_v1`: skipped because raw number-square values are not locked.
- `exp_stage4b_visual_negative_controls_v1`: audited as negative-control metrics.
- `exp_stage4b_cuneiform_reading_pack_v1`: deferred pending accepted annotation.
- `exp_stage4b_cookie_pack_v2`: deferred to Stage 4E cookie exact-candidate refresh.

The Stage 4B manifest files remain disabled. Stage 4D authorization is represented by the bounded numeric CLI and generated ignored result records, not by changing these records to `execution_enabled=true`.
