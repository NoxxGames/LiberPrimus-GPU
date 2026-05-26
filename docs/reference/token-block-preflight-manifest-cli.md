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
