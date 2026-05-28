# Stage 5BN String 4 Unsupported-Position Workflow

Stage 5BN is a metadata-only source-gap closure stage for one target: String 4 token index `199`, logical row `25`, column `8`.

Inputs:

- `data/token-block/stage5bm-string4-stage5aw-branch-membership.yaml`
- `data/token-block/stage5bm-string4-stage5ap-mismatch-analysis.yaml`
- `data/token-block/stage5aw-repaired-unresolved-token-variant-records.yaml`
- `data/source-harvester/stage5bi-local-spreadsheet-source-lock.yaml`
- ignored local `third_party/3N_3p_Bases_49-51.jpg.xlsx`

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bn-unsupported-position-review
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bn-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bn
```

Interpretation:

- Stage 5AW still allows only `0I`, `0j`, `OI`, and `Oj` at the target.
- The local spreadsheet target row records `0l` for the same zero-based position.
- Stage 5BN proposes `0l` only as an inactive review-only addendum.
- Active Stage 5AW/5AY/5AZ records, canonical transcription, and token-block manifests remain unchanged.

Do not generate byte streams, materialise variants, run DWH/hash searches, decode, score, run OCR/AI/CUDA/stego tooling, or treat this as solve evidence.
