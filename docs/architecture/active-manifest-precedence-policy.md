# Active Manifest Precedence Policy

Stage 5BB makes active manifest precedence explicit before any future token-block runner can exist.

The registry canonicalises these key roles:

- `active_branch_manifest`: `data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml`
- `active_branch_eligibility_policy`: `data/token-block/stage5ay-branch-eligibility-policy.yaml`
- `active_bounded_variant_family_manifest`: `data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml`
- `active_execution_gates`: `data/token-block/stage5az-repaired-execution-gates.yaml`

Inactive as active inputs:

- `data/token-block/stage5av-token-variant-branch-manifest.yaml`
- `data/token-block/stage5ay-bounded-variant-family-manifest.yaml`

The Stage 5AZ execution-gate file contains a legacy pointer to the old Stage 5AY bounded variant-family manifest. Stage 5BB classifies that pointer as `legacy_superseded_pointer` and redirects active loading to the Stage 5AZ repaired manifest.

Loader rule: active loads must go through `data/token-block/stage5bb-active-manifest-registry.yaml`; stale active loads are blocked, while historical diagnostic loads must be explicit and audited.
