# Bounded Token-Block Preflight Workflow

Use Stage 5AZ repaired records when reviewing future page 49-51 token-block preflight work. Stage 5AY remains the design source stage, but its bounded variant-family manifest is superseded for Deep Research review because it duplicated `unresolved_as_current_only` as a flat family record.

Start with:

- `data/token-block/stage5ay-preflight-source-inputs.yaml`
- `data/token-block/stage5ay-branch-eligibility-policy.yaml`
- `data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml`
- `data/token-block/stage5ay-branch-count-budget.yaml`
- `data/token-block/stage5az-repaired-branch-count-budget.yaml`
- `data/token-block/stage5az-repaired-execution-gates.yaml`
- `data/token-block/stage5az-deep-research-readiness.yaml`
- `data/project-state/stage5az-summary.yaml`

Rules:

- Use Stage 5AW repaired branch metadata for planning.
- Do not fall back to the Stage 5AV branch manifest.
- Do not treat `data/token-block/stage5ay-bounded-variant-family-manifest.yaml` as the active variant-family manifest for Deep Research review.
- Preserve `unresolved_as_current_only` as one family record with `baseline_family` and `unresolved_policy_family` taxonomy memberships.
- Do not generate byte streams or enumerate variants during design review.
- Do not execute DWH/hash searches, decoding, controls, scoring, OCR/AI/ML/LLM vision, stego, CUDA, or benchmarks.
- Treat Stage 5BA as review of the repaired design and gates, not execution.
