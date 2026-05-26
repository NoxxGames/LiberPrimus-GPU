# Bounded Token-Block Preflight Workflow

Use Stage 5BB records when reviewing future page 49-51 token-block preflight runner work. Stage 5AY remains the design source stage, Stage 5AZ repaired the duplicate bounded variant-family manifest, and Stage 5BB is now the no-execution scaffold and active-manifest registry layer.

Start with:

- `data/token-block/stage5ay-preflight-source-inputs.yaml`
- `data/token-block/stage5ay-branch-eligibility-policy.yaml`
- `data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml`
- `data/token-block/stage5ay-branch-count-budget.yaml`
- `data/token-block/stage5az-repaired-branch-count-budget.yaml`
- `data/token-block/stage5az-repaired-execution-gates.yaml`
- `data/token-block/stage5az-deep-research-readiness.yaml`
- `data/project-state/stage5az-summary.yaml`
- `data/token-block/stage5bb-active-manifest-registry.yaml`
- `data/token-block/stage5bb-legacy-pointer-audit.yaml`
- `data/token-block/stage5bb-branch-eligibility-reference-validation.yaml`
- `data/token-block/stage5bb-runner-scaffold-manifest.yaml`
- `data/token-block/stage5bb-no-execution-proof.yaml`
- `data/project-state/stage5bb-summary.yaml`

Rules:

- Use Stage 5AW repaired branch metadata for planning.
- Do not fall back to the Stage 5AV branch manifest.
- Do not treat `data/token-block/stage5ay-bounded-variant-family-manifest.yaml` as the active variant-family manifest for Deep Research review.
- Load future runner inputs through the Stage 5BB active-manifest registry.
- Treat Stage 5BB dry-run previews as no-output plan previews only.
- Preserve `unresolved_as_current_only` as one family record with `baseline_family` and `unresolved_policy_family` taxonomy memberships.
- Do not generate byte streams or enumerate variants during design review.
- Do not execute DWH/hash searches, decoding, controls, scoring, OCR/AI/ML/LLM vision, stego, CUDA, or benchmarks.
- Treat Stage 5BC as review of the runner scaffold and gates, not execution.
