# Token-Block Preflight Runner Scaffold Workflow

Use this workflow when reviewing or extending Stage 5BB.

1. Start with `data/token-block/stage5bb-active-manifest-registry.yaml`.
2. Confirm active branch metadata points to Stage 5AW repaired records.
3. Confirm active variant-family metadata points to Stage 5AZ repaired records.
4. Confirm `data/token-block/stage5ay-branch-eligibility-policy.yaml` is present and validated.
5. Check `data/token-block/stage5bb-legacy-pointer-audit.yaml` before trusting any legacy pointer in Stage 5AZ execution-gate records.
6. Use the dry-run preview only for plan review; it must not include real token bytes, variant outputs, scores, hashes, or decoded text.
7. Treat fixture records as synthetic schema tests only.

Do not run token experiments, generate byte streams, materialise variants, perform DWH/hash search, decode, score, run CUDA, benchmark, or claim a solve from Stage 5BB material.
