# Token-Block CLI

Stage 5AP adds `libreprimus token-block` for metadata-only source-lock and preflight records.
Stage 5AR extends the same group with original-image coordinate-lock commands documented in `docs/reference/token-block-coordinate-cli.md`. Stage 5AT adds token case-review pack commands documented in `docs/reference/token-case-review-pack-cli.md`. Stage 5AU adds review-pack v2 usability-repair commands documented in `docs/reference/token-case-review-pack-v2-cli.md`. Stage 5AV adds decision-integration commands documented in `docs/reference/token-case-decision-integration-cli.md`. Stage 5AW adds decision-parser repair commands documented in `docs/reference/decision-parser-repair-cli.md`. Stage 5AY adds bounded preflight manifest-design commands documented in `docs/reference/token-block-preflight-manifest-cli.md`. Stage 5AZ adds manifest-integrity repair commands in the same preflight reference. Stage 5BB adds no-execution preflight runner scaffold commands documented in `docs/reference/token-block-preflight-runner-scaffold-cli.md`. Stage 5BD adds metadata-only dry-run implementation records. Stage 5BF keeps token-block execution paused while historical route source-lock and technique taxonomy records are reviewed. Stage 5BI keeps it paused while Fandom-derived source-lock/crosswalk gaps are recorded. Stage 5BJ keeps it paused while original/archive crosswalk closures and exact 2014 surface source locks are recorded. Stage 5BK integrates historical-route planning constraints and iddqd-v2 metadata before Stage 5BL review. Stage 5BM integrates that review into String 4 branch-crosswalk repair. Stage 5BN closes the single unsupported-position source gap as inactive addendum metadata. Stage 5BO integrates corrected human-review template errata into inactive planning metadata before Stage 5BP review. Stage 5BQ integrates that review outcome into fail-closed inactive-branch dry-run planning constraints before Stage 5BR review.

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

Stage 5AY generated preflight reports are written under `experiments/results/token-block/stage5ay/` and remain ignored. The bounded preflight manifest-design commands write compact metadata only; they must not generate variant byte streams, enumerate the full branch product, execute token experiments or controls, search DWH/hash/preimage targets, decode, run OCR/AI/ML/LLM vision, run semantic or hidden-content image interpretation, run stego, run CUDA, benchmark, execute scored experiments, upgrade method status, activate the canonical corpus, finalise page boundaries, or make solve claims.

Stage 5AZ generated integrity reports are written under `experiments/results/token-block/stage5az/` and remain ignored. The repair commands write compact superseding metadata only; they must not overwrite Stage 5AY history, generate variant byte streams, enumerate the full branch product, execute token experiments or controls, search DWH/hash/preimage targets, decode, run OCR/AI/ML/LLM vision, run semantic or hidden-content image interpretation, run stego, run CUDA, benchmark, execute scored experiments, upgrade method status, activate the canonical corpus, finalise page boundaries, expand the public website, or make solve claims.

Stage 5BB generated dry-run and fixture-schema reports are written under `experiments/results/token-block/stage5bb/` and remain ignored. The scaffold commands write compact metadata only; they must not generate real token-block byte streams, materialise variants, enumerate Cartesian products, execute token experiments or controls, search DWH/hash/preimage targets, compare hashes, decode, score, run OCR/AI/ML/LLM vision, run semantic or hidden-content image interpretation, run stego, run CUDA, benchmark, execute scored experiments, upgrade method status, activate the canonical corpus, finalise page boundaries, expand the public website, or make solve claims.

Stage 5BI adds token-block external context records under `data/token-block/stage5bi-*` through the `historical-route` CLI. These records must not change canonical token transcription, active token-block manifests, or Stage 5BD dry-run records, and must not authorize byte-stream generation, 2014/page49-51 surface combination, DWH/hash search, decoding, scoring, stego/audio/image/OCR/AI/CUDA work, benchmarks, or solve claims.

Stage 5BJ adds token-block lineage and 2014 surface context closure records under `data/token-block/stage5bj-*` through the `historical-route` CLI. These records preserve canonical token transcription, active token-block manifests, and Stage 5BD dry-run gates unchanged, and must not authorize byte-stream generation, 2014/page49-51 surface combination, DWH/hash search, decoding, scoring, stego/audio/image/OCR/AI/CUDA work, benchmarks, or solve claims.

Stage 5BK adds token-block historical constraint, 2014 surface/page49 context, String 4 page49-51 crosswalk, lineage preservation, and future dry-run planning impact records under `data/token-block/stage5bk-*` through the `historical-route` CLI. These records preserve canonical token transcription, active token-block manifests, and Stage 5BD dry-run gates unchanged. String 4 is external matrix-hex context only; it must not replace Stage 5AP transcription and must not authorize byte-stream generation, 2014/page49-51 surface combination, DWH/hash/preimage search, decoding, scoring, stego/audio/image/OCR/AI/CUDA work, benchmarks, or solve claims.

## Stage 5BM Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bm-string4-reconciliation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bm-string4-reconciliation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bm
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bm-summary
```

Stage 5BM commands write compact String 4 branch-crosswalk metadata under `data/token-block/stage5bm-*`, `data/historical-route/stage5bm-*`, `data/source-harvester/stage5bm-*`, and `data/project-state/stage5bm-*`. Generated diagnostics are written under `experiments/results/token-block/stage5bm/` and `experiments/results/historical-route/stage5bm/` and remain ignored. These commands may parse the ignored local iddqd-v2 String 4 file in memory, but they must not commit full String 4 bodies, decoded bytes, reconstructed token streams, generated diagnostics, or raw third-party files.

## Stage 5BN Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bn-unsupported-position-review
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bn-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bn
.\.venv\Scripts\python.exe -m libreprimus.cli token-block show-stage5bn-summary
```

Stage 5BN commands write compact target-only String 4 unsupported-position metadata under `data/token-block/stage5bn-*`, `data/historical-route/stage5bn-*`, `data/source-harvester/stage5bn-*`, and `data/project-state/stage5bn-*`. Generated diagnostics are written under `experiments/results/token-block/stage5bn/` and `experiments/results/historical-route/stage5bn/` and remain ignored. These commands may parse only the target row/cell metadata from the ignored local spreadsheet and target source metadata from ignored local roots, but they must not commit the workbook, full cell dumps, full String 4 bodies, decoded bytes, reconstructed token streams, review-pack bodies, generated diagnostics, or raw third-party files. They preserve Stage 5AP canonical transcription, Stage 5AW active options, Stage 5AZ active manifests, and Stage 5BD dry-run records unchanged.

## Stage 5BO Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bo-decision-template-errata `
  --original-template human-review-packs/stage5au/token-case-review-v2/decision-template.yaml `
  --corrected-template human-review-packs/stage5au/token-case-review-v2/decision-template-corrected.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bo
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bo-summary
```

Stage 5BO commands write compact operator-errata and inactive String 4 after-errata metadata under `data/token-block/stage5bo-*`, `data/historical-route/stage5bo-*`, `data/source-harvester/stage5bo-*`, and `data/project-state/stage5bo-*`. Generated diagnostics are written under `experiments/results/token-block/stage5bo/` and `experiments/results/historical-route/stage5bo/` and remain ignored. These commands may parse the ignored original and corrected decision templates for hashing and compact diff metadata only, but they must not commit either template, full review-pack bodies, full String 4 bodies, decoded bytes, reconstructed token streams, generated diagnostics, byte streams, or raw third-party files. They preserve Stage 5AP canonical transcription, Stage 5AW/5AY/5AZ active records, and Stage 5BD dry-run records unchanged.

## Stage 5BQ Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bq-planning-integration
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bq
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bq-summary
```

Stage 5BQ commands write compact inactive-branch dry-run planning metadata under `data/token-block/stage5bq-*`, `data/historical-route/stage5bq-*`, `data/source-harvester/stage5bq-*`, and `data/project-state/stage5bq-*`. Generated diagnostics are written under `experiments/results/token-block/stage5bq/` and remain ignored. These commands consume committed Stage 5BO/5BD records and Stage 5BP findings metadata only; they must not commit Deep Research bodies, ingest String 4 into dry-run plans, generate byte streams, materialise variants, run DWH/hash search, decode, score, run CUDA, benchmark, or make solve claims. They preserve Stage 5AP canonical transcription, Stage 5AW/5AY/5AZ active records, Stage 5BB active-manifest records, and Stage 5BD dry-run records unchanged.
