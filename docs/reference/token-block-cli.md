# Token-Block CLI

Stage 5AP adds `libreprimus token-block` for metadata-only source-lock and preflight records.
Stage 5AR extends the same group with original-image coordinate-lock commands documented in `docs/reference/token-block-coordinate-cli.md`. Stage 5AT adds token case-review pack commands documented in `docs/reference/token-case-review-pack-cli.md`. Stage 5AU adds review-pack v2 usability-repair commands documented in `docs/reference/token-case-review-pack-v2-cli.md`. Stage 5AV adds decision-integration commands documented in `docs/reference/token-case-decision-integration-cli.md`. Stage 5AW adds decision-parser repair commands documented in `docs/reference/decision-parser-repair-cli.md`.

Core commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-source-lock --search-roots third_party --search-roots research-inputs --search-roots website-export --search-roots data
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-transcription
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-alphabet-registry
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-mapping-preflight
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-null-control-plan
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-dwh-context
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5ap-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5ap
```

Generated reports are written under `experiments/results/token-block/stage5ap/` and remain ignored. The CLI must not perform OCR, image interpretation, decoding, hash/preimage search, CUDA execution, benchmark work, or hypothesis execution.

Stage 5AR generated reports are written under `experiments/results/token-block/stage5ar/` and remain ignored. The coordinate commands may read local original page images for deterministic pixel-coordinate metadata, but they must not commit raw images or use screenshots/crops/modified images as coordinate truth.

Stage 5AT generated reports are written under `experiments/results/token-block/stage5at/`, and generated review-pack files are written under `human-review-packs/stage5at/token-case-review/`; both remain ignored. The case-review commands must not change canonical transcription, use OCR/AI/ML/LLM vision, decode the block, run hash/preimage search, run CUDA, benchmark, execute scored experiments, or make solve claims.

Stage 5AU generated reports are written under `experiments/results/token-block/stage5au/`, and generated review-pack v2 files are written under `human-review-packs/stage5au/token-case-review-v2/`; both remain ignored. The v2 commands must not fill decisions, change canonical transcription, use OCR/AI/ML/LLM vision, interpret images, decode the block, run hash/preimage search, run stego, run CUDA, benchmark, execute scored experiments, or make solve claims.

Stage 5AV generated reports are written under `experiments/results/token-block/stage5av/`, and the filled decision template remains ignored under `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`. The integration commands must not change canonical transcription unless explicit validated `change_token` records exist, generate variant byte streams, enumerate the full branch product, run token experiments, search DWH hashes, decode, run OCR/AI/ML/LLM vision, run stego, run CUDA, benchmark, execute scored experiments, or make solve claims.

Stage 5AW generated reports are written under `experiments/results/token-block/stage5aw/`, and the filled decision template remains ignored under `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`. The parser-repair commands must not reinterpret human decisions, change canonical transcription, generate variant byte streams, enumerate the full branch product, run token experiments, search DWH hashes, decode, run OCR/AI/ML/LLM vision, run semantic or hidden-content image interpretation, run stego, run CUDA, benchmark, execute scored experiments, or make solve claims.
