# Bounded Token-Block Preflight Workflow

Use Stage 5AY records when reviewing future page 49-51 token-block preflight work.

Start with:

- `data/token-block/stage5ay-preflight-source-inputs.yaml`
- `data/token-block/stage5ay-branch-eligibility-policy.yaml`
- `data/token-block/stage5ay-bounded-variant-family-manifest.yaml`
- `data/token-block/stage5ay-branch-count-budget.yaml`
- `data/token-block/stage5ay-execution-gates.yaml`
- `data/project-state/stage5ay-summary.yaml`

Rules:

- Use Stage 5AW repaired branch metadata for planning.
- Do not fall back to the Stage 5AV branch manifest.
- Do not generate byte streams or enumerate variants during design review.
- Do not execute DWH/hash searches, decoding, controls, scoring, OCR/AI/ML/LLM vision, stego, CUDA, or benchmarks.
- Treat Stage 5AZ as review of the design and gates, not execution.
