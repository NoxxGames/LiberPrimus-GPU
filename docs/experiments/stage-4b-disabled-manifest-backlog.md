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
