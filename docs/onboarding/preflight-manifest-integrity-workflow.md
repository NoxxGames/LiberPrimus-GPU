# Preflight Manifest Integrity Workflow

Stage 5AZ repaired the Stage 5AY duplicate bounded variant-family ID. Stage 5BB is now the active no-execution runner-scaffold layer that consumes that repair.

Use:

- `data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml` as the active bounded variant-family manifest.
- `data/token-block/stage5ay-bounded-variant-family-manifest.yaml` only for historical diagnostics.
- `data/token-block/stage5bb-active-manifest-registry.yaml` as the active loader source.
- `data/token-block/stage5bb-legacy-pointer-audit.yaml` to verify stale pointers are blocked.

Do not execute token experiments, generate byte streams, enumerate variants, search DWH/hashes, decode, score, run CUDA, benchmark, or claim a solve from manifest-integrity records.
