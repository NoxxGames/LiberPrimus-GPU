# Decision Parser Repair Workflow

Use this workflow when a human-review decision note parser captures prose as a token alternative.

1. Audit the prior reviewer-extra token records with `libreprimus token-block audit-stage5aw-decision-parser`.
2. Repair possible-token parsing with `repair-stage5aw-decision-variants`.
3. Rebuild primary-60 impact and compact branch metadata with `build-stage5aw-repaired-branch-manifest`.
4. Build canonical non-update, null-control, DWH context, guardrail, next-stage, and summary records.
5. Validate with `libreprimus token-block validate-stage5aw`.

The workflow preserves the ignored local decision template and commits only compact metadata. It does not change canonical transcription, resolve ambiguous tokens automatically, generate variant byte streams, decode the token block, run DWH/hash search, run OCR/AI/ML/LLM vision, run stego, run CUDA, benchmark, execute scored experiments, or make solve claims.

Stage 5AX inserted parallel validation infrastructure after this repair. Stage 5AY then designed bounded token-block preflight manifests and gates from the repaired Stage 5AW branch manifest. Stage 5AZ should review those design records before any runner implementation or execution.
