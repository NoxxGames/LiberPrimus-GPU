# Stage 5J Gematria CUDA Kernel

Stage 5J is not a cryptanalytic experiment. It is a synthetic CUDA parity implementation stage for
the Stage 5H Gematria mod-29 shift contract.

Run the local validation commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-kernel validate-stage5j `
  --implementation data/cuda/stage5j-gematria-cuda-kernel-implementation.yaml `
  --build-records data/cuda/stage5j-gematria-cuda-kernel-build-records.yaml `
  --parity-records data/cuda/stage5j-gematria-cuda-synthetic-parity-records.yaml `
  --summary data/cuda/stage5j-gematria-cuda-kernel-summary.yaml `
  --results-dir experiments/results/gematria-cuda-kernel/stage5j
```

Stage 5J may record a skipped build in no-GPU CI, or a passed optional local build/parity record when
CUDA is available. In both cases the generated reports remain ignored.

Do not run real Liber Primus page data, solved fixtures, unsolved pages, broad experiments,
benchmarks, source crawling, stego/audio tools, image/OCR/AI processing, or solve-claim workflows
from this stage.
