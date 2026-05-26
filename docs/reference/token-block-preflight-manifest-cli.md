# Token-Block Preflight Manifest CLI

Stage 5AY extends `libreprimus token-block` with design-only commands:

```powershell
python -m libreprimus.cli token-block build-stage5ay-preflight-design
python -m libreprimus.cli token-block build-stage5ay-control-manifests
python -m libreprimus.cli token-block build-stage5ay-execution-gates
python -m libreprimus.cli token-block build-stage5ay-summary
python -m libreprimus.cli token-block validate-stage5ay
```

The commands write compact committed metadata under `data/token-block/` and `data/project-state/`, plus ignored reports under `experiments/results/token-block/stage5ay/`.

They do not execute token experiments, generate variant byte streams, run DWH/hash search, decode, score, benchmark, use OCR/AI/ML/LLM vision, run stego, or run CUDA.

Stage 5AZ extends the same group with manifest-integrity repair commands:

```powershell
python -m libreprimus.cli token-block audit-stage5az-preflight-manifests
python -m libreprimus.cli token-block repair-stage5az-variant-family-manifest
python -m libreprimus.cli token-block build-stage5az-readiness
python -m libreprimus.cli token-block build-stage5az-summary
python -m libreprimus.cli token-block validate-stage5az
```

The Stage 5AZ commands write compact superseding metadata under `data/token-block/` and `data/project-state/`, plus ignored reports under `experiments/results/token-block/stage5az/`. They keep Stage 5AY as the design source stage while making `data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml` the active variant-family record for Deep Research review.

They do not overwrite Stage 5AY history, execute token experiments, generate variant byte streams, run DWH/hash search, decode, score, benchmark, use OCR/AI/ML/LLM vision, run stego, run CUDA, expand the public website, or make solve claims.
