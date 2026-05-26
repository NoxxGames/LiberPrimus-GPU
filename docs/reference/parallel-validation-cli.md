# Parallel Validation CLI

Stage 5AX adds `libreprimus parallel-validation`.

Build the committed command plan:

```powershell
python -m libreprimus.cli parallel-validation build-stage5ax-plan
```

Run the local harness:

```powershell
python -m libreprimus.cli parallel-validation run-stage5ax-parallel-validation `
  --workers 16 `
  --pytest-workers 16 `
  --pytest-mode auto
```

Build and validate summary records:

```powershell
python -m libreprimus.cli parallel-validation build-stage5ax-summary
python -m libreprimus.cli parallel-validation validate-stage5ax
python -m libreprimus.cli parallel-validation summary
```

The command writes detailed logs and JSON reports under ignored `experiments/results/ci/parallel-validation/stage5ax/`. Commit only compact metadata under `data/ci/` and `data/project-state/`.

The CLI does not run token experiments, DWH/hash searches, decoding, OCR, AI/ML interpretation, LLM/vision token reading, hidden-content image forensics, stego, CUDA, cryptanalytic benchmarks, scored experiments, or solve-claim workflows.
