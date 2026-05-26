# Contributor Module Map

## Stage 5AY Note

The token-block layer now includes Stage 5AY helpers under `python/libreprimus/token_block/`. These helpers create design-only preflight manifests, branch eligibility records, control families, branch budgets, result-schema previews, execution gates, DWH context, and summaries. They must not be extended into token execution, byte-stream generation, decoding, DWH/hash search, OCR/AI/ML interpretation, CUDA, cryptanalytic benchmarks, or scored experiments without an explicit future stage.

## Module Areas

- Profiles/corpus: `python/libreprimus/profiles/`, `python/libreprimus/corpus_candidate/`, `data/profiles/`.
- Solved fixtures: `python/libreprimus/solved_fixtures/`, `data/fixtures/`.
- Transforms: `python/libreprimus/transforms/`, `data/transform-registry/`.
- Scoring: `python/libreprimus/scoring/`, `python/libreprimus/candidate_inspection/`.
- Experiments: `python/libreprimus/experiments/`, `python/libreprimus/bounded_experiments/`, `experiments/`.
- Result store: `python/libreprimus/result_store/`, `schemas/result-store/`.
- Archive/history: `python/libreprimus/history/`, `data/observations/archive/`.
- Visual/image analysis: `python/libreprimus/image_analysis/`, `python/libreprimus/image_transforms/`, `data/observations/visual/`.
- Discord: `python/libreprimus/discord_ingestion/`, `discord_promotion/`, `discord_review/`, `discord_lead_promotion/`.
- Post-Discord: `python/libreprimus/post_discord/`.
- Stego: `python/libreprimus/stego/`.
- Token-block source locks: `python/libreprimus/token_block/`, `data/token-block/`, `schemas/token-block/`.
- Stage 5AP stego controls: `python/libreprimus/stego_controls/`, `data/stego/stage5ap-outguess-*.yaml`, `schemas/stego/outguess-*.json`.
- Stage 5AR token-block coordinates: `python/libreprimus/token_block/`, `data/token-block/stage5ar-*.yaml`, `schemas/token-block/*coordinate*.json`, and `schemas/token-block/*case*.json`.
- Stage 5AT/5AU token-case review packs: `python/libreprimus/token_block/`, `data/token-block/stage5at-*.yaml`, `data/token-block/stage5au-*.yaml`, `data/project-state/stage5at-*.yaml`, `data/project-state/stage5au-*.yaml`, `schemas/token-block/*case-review*.json`, `schemas/token-block/*challenge*.json`, `schemas/token-block/*review*.json`, and `schemas/token-block/*crop*.json`.
- Research synthesis: `python/libreprimus/research_synthesis/`, `data/research/`.
- Document staleness: `python/libreprimus/doc_staleness/`, `data/project-state/`, `schemas/project-state/`.
- Parallel validation: `python/libreprimus/parallel_validation/`, `data/ci/stage5ax-*.yaml`, `schemas/ci/*parallel*.json`, and `scripts/ci/run-parallel-validation.*`.
- Stage 5AY token-block preflight design: `python/libreprimus/token_block/stage5ay.py`, `data/token-block/stage5ay-*.yaml`, `data/project-state/stage5ay-*.yaml`, and `schemas/token-block/*preflight*.json`.
- Source harvester: `python/libreprimus/source_harvester/`, `data/source-harvester/`, `schemas/source-harvester/`.
- Website renderer: `python/libreprimus/website_render/`, `data/website-render/`, `schemas/website-render/`.
- CUDA parity/reporting: `python/libreprimus/cuda_*`, `python/libreprimus/prime_minus_one_*`, `python/libreprimus/bounded_p56_cuda_parity/`, `cuda/`, `data/cuda/`.
- CLI: `python/libreprimus/cli.py`, `python/libreprimus/cli_commands/`.
- CI/scripts: `.github/workflows/`, `scripts/ci/`, `scripts/github/`.

## Stable Areas

Docs, schemas, record validation, test fixtures, and source-lock metadata are relatively safe when changes are narrow and validated.

## Volatile Or Risky Areas

Corpus/profile semantics, scoring, experiment execution, privacy-sensitive Discord code, generated-output policy, and CUDA are high-risk. Read the relevant docs and tests first.

Source-harvester code is high-provenance tooling. Read `docs/architecture/cicada-source-harvester.md`, `docs/architecture/local-source-lock-inventory.md`, `docs/architecture/curated-research-bundle-format.md`, `docs/architecture/website-ingest-source-card-format.md`, `docs/architecture/extraction-fidelity-and-redaction-policy.md`, `docs/architecture/scraper-capture-profiles.md`, `docs/architecture/community-claim-records.md`, `docs/reference/source-harvester-cli.md`, `docs/reference/source-harvester-local-inventory-cli.md`, `docs/reference/source-harvester-curated-bundles-cli.md`, `docs/reference/source-harvester-usefulfiles-cli.md`, `docs/reference/source-harvester-community-facts-cli.md`, `docs/onboarding/source-harvester-workflow.md`, `docs/onboarding/local-source-inventory-workflow.md`, `docs/onboarding/deep-research-bundle-workflow.md`, `docs/onboarding/deep-research-ingest-format.md`, and `docs/onboarding/community-observation-ingest-workflow.md` before changing it. Do not make Google Drive a storage backend; manual Google/Dropbox/Colab/community exports belong in ignored local roots.

Stage 5AI source-harvester modules under `python/libreprimus/source_harvester/` classify local inventory rows, build source cards, create curated bundle metadata, build content and website-ingest indexes, prepare Deep-Research pack indexes, record missing-source plans, and validate guardrails. They must not read raw third-party material into committed files or execute hypotheses.

Stage 5AJ source-harvester modules add UsefulFilesAndIdeas inventory, workbook metadata extraction, important-link parsing, extraction-fidelity policy, redaction policy, scraper-capture policy, source-card/content-index updates, Deep-Research pack readiness, and guardrail validation. They must keep raw workbooks/images/text and generated cell/body indexes ignored.

Stage 5AK source-harvester modules add community-facts inventory, ordered attachment metadata, claim records, correction logs, arithmetic preflight, private Deep Research addenda, publication guardrails, and validation. They must keep raw message logs/images and generated body indexes ignored, and must not treat community number facts as execution-ready or solved.

Stage 5AL source-harvester modules add website-ingest package generation, publication-gate policy, private Deep Research export generation, data-contract validation, guardrails, and next-stage selection. They must keep public website-ready at zero, generated private export helpers ignored, and raw `third_party/` material out of committed records.

Stage 5AM website-render modules render the Stage 5AL metadata package into an ignored private static index and upload manifest. They must keep public website-ready at zero, preserve publication gates, avoid raw/private bodies, avoid external dependencies, write generated site files only under ignored `website-export/stage5am/`, and point Stage 5AN Deep Research at metadata rather than raw paths.

Stage 5AN deep-research-export modules package private handoff files, render hosted private content, and build the combined SFTP webroot. They must keep generated pack/site/webroot files ignored, preserve publication gates, exclude raw third-party binaries and archives by default, avoid network fetches, avoid Google Drive storage, and point future review work at Stage 5AU review-pack v2 records, Stage 5AT review-pack records, Stage 5AR coordinate records, Stage 5AP token-block records, plus metadata/private hosted URLs rather than raw paths.

Stage 5AP token-block and stego-control modules record page 49-51 source-lock/preflight metadata and OutGuess control readiness. They must not decode the token block, run hash/preimage search, run OCR/AI/ML, process raw page images into committed data, run LP-page OutGuess, execute CUDA, benchmark, or make solve claims.

Stage 5AR token-block coordinate modules record original-image source locks, image variants, page splits, pixel coordinates, case ambiguity, coordinate validation, and null-control/DWH context updates. They must not use screenshots/crops/modified images as coordinate truth, run OCR/AI/ML, interpret image semantics, run hidden-content forensics, decode, search hashes, execute stego/CUDA/scored experiments, benchmark, or make solve claims.

Stage 5AT/5AU token-block review modules build local human-review packs for case ambiguity. They may create ignored crops, overlays, and review sheets, but must not commit generated packs, use OCR/AI/ML/LLM vision to fill decisions, change the canonical transcription, decode, search hashes, execute stego/CUDA/scored experiments, benchmark, or make solve claims.

Stage 5AV token-block decision integration modules ingest the local filled Stage 5AU v2 decision template into committed metadata, confirmed-token records, unresolved variant records, reviewer-extra possible-token records, primary-60 impact summaries, and compact branch manifests. They must not commit the human decision template or generated reports, change canonical transcription, auto-resolve unresolved variants, generate variant byte streams, decode, search DWH/hash/preimage candidates, execute stego/CUDA/scored experiments, benchmark, or make solve claims.

Stage 5AW token-block decision-parser repair modules audit possible-token parser contamination, preserve valid reviewer extras, preserve visual placeholders as review-only unmappable records, audit malformed prose fragments, and rebuild repaired compact branch metadata. They must not reinterpret human decisions, change canonical transcription, generate variant byte streams, decode, search DWH/hash/preimage candidates, execute stego/CUDA/scored experiments, benchmark, or make solve claims.

Stage 5AX parallel-validation modules classify commands, cap worker counts, run read-only validation subprocesses, shard pytest when xdist is unavailable, aggregate logs/failures, and validate safety records. They must not schedule git/GitHub/network/generated-output-writing commands in the parallel pool or run cryptanalytic work.

Stage 5AY token-block preflight modules build design metadata only. They must use Stage 5AW repaired branch metadata, keep Stage 5AV branch metadata superseded for planning, define controls and gates without execution, keep generated reports ignored, and preserve all no-DWH/no-decode/no-CUDA/no-score/no-solve guardrails.

## Good First Areas

- Documentation fixes.
- Tests for validation code.
- Source-lock records.
- Observation records.
- Negative controls.
- Schema validation.

## Risky Areas

- Changing rune mappings or separator semantics.
- Changing scoring labels or thresholds.
- Executing new experiments.
- Touching Discord raw-log processing.
- Adding CUDA kernels.
