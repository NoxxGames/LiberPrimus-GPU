# Contributor Module Map

## Stage 5BI Note

The historical-route layer now also includes Stage 5BI Fandom/source-lock triage helpers under `python/libreprimus/historical_route/stage5bi.py`. Stage 5BI writes compact metadata for Fandom page triage, archive crosswalk candidates, 2014 surface context, spreadsheet source-lock/reconciliation, source gaps, negative controls, guardrails, and next-stage routing. These helpers must not be extended into Fandom page crawling, media downloading, spreadsheet cell-body publication, token execution, byte-stream generation, DWH/hash search, decoding, stego/audio/image/OCR/AI/CUDA work, benchmarking, scoring, or solve claims without an explicit future stage.

## Stage 5BF Note

The historical-route layer now includes Stage 5BF source-lock helpers under `python/libreprimus/historical_route/`. Stage 5BF reads ignored local archive files only to compute compact hashes and metadata, classifies technique families/trust levels, and keeps execution blocked. These helpers must not be extended into live scraping, online cloning, PGP keyserver use, stego execution, token execution, byte-stream generation, variant materialisation, decoding, DWH/hash search, scoring, OCR/AI/ML interpretation, CUDA, cryptanalytic benchmarks, or scored experiments without an explicit future stage.

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
- Stage 5AZ token-block manifest-integrity repair: `python/libreprimus/token_block/stage5az.py`, `data/token-block/stage5az-*.yaml`, `data/project-state/stage5az-*.yaml`, and `schemas/token-block/*integrity*.json`.
- Stage 5BB token-block preflight runner scaffold: `python/libreprimus/token_block/stage5bb.py`, `data/token-block/stage5bb-*.yaml`, `data/project-state/stage5bb-*.yaml`, and `schemas/token-block/*manifest*.json`, `schemas/token-block/*scaffold*.json`, `schemas/token-block/*execution-gate*.json`, plus `schemas/project-state/stage5bb-summary-v0.schema.json`.
- Stage 5BD token-block preflight dry-run package: `python/libreprimus/token_block/preflight_runner/`, `data/token-block/stage5bd-*.yaml`, `data/project-state/stage5bd-*.yaml`, `schemas/token-block/*dry-run*.json`, `schemas/token-block/*run-plan*.json`, and `schemas/project-state/stage5bd-summary-v0.schema.json`.
- Stage 5BF historical route source-lock package: `python/libreprimus/historical_route/`, `data/historical-route/stage5bf-*.yaml`, `data/project-state/stage5bf-*.yaml`, `schemas/historical-route/*.json`, and `schemas/project-state/stage5bf-summary-v0.schema.json`.
- Stage 5BI Fandom/source-lock triage package: `python/libreprimus/historical_route/stage5bi.py`, `data/historical-route/stage5bi-*.yaml`, `data/source-harvester/stage5bi-*.yaml`, `data/token-block/stage5bi-*.yaml`, `data/project-state/stage5bi-*.yaml`, `schemas/historical-route/stage5bi-*.json`, `schemas/source-harvester/stage5bi-*.json`, `schemas/token-block/stage5bi-*.json`, and `schemas/project-state/stage5bi-*.json`.
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

Stage 5AZ token-block manifest-integrity modules repair metadata only. They must supersede the Stage 5AY bounded variant-family manifest for Deep Research review, preserve taxonomy overlap through `taxonomy_memberships`, keep branch budgets unchanged, keep execution gates blocked, keep generated reports ignored, and preserve all no-DWH/no-decode/no-CUDA/no-score/no-solve guardrails.

Stage 5BD token-block preflight-runner modules build no-byte-stream dry-run policy, run-plan ID, future-path, counter, execution-gate, fixture-only, archive marker, and no-byte-stream proof records. They must use the Stage 5BB active-manifest registry lineage, keep Stage 5AV and old Stage 5AY manifests inactive as active inputs, keep generated reports ignored, and preserve all no-byte-stream/no-variant/no-DWH/no-decode/no-score/no-CUDA/no-benchmark/no-solve guardrails.

Stage 5BF historical-route modules locate and inventory the local `CicadaSolversIddqd` archive, hash-lock files, classify high-priority route artefacts, and build trust/technique/source-gap/readiness records. They must keep raw archive files ignored, generated reports ignored, no network clone/fetch, no PGP network verification, no stego execution, no token-block byte streams, no DWH/hash search, no CUDA, no benchmarks, no public website publication, and no solve claims.

Stage 5BI historical-route modules build Fandom/source-lock triage records and spreadsheet metadata only. They must keep Fandom page bodies/media, raw archive files, spreadsheet bytes/cell bodies, generated outputs, token-block byte streams, 2014/page49-51 combinations, DWH/hash searches, decode attempts, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website publication, and solve claims blocked.

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
## Stage 5BD Module

The Stage 5BD preflight-runner package split lives at `python/libreprimus/token_block/preflight_runner/` and remains dry-run-only.
