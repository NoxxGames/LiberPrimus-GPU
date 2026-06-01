# Results Schema

Stage 5CQ adds compact Stage 5CP findings integration records, operator-decision package scaffold records, Stage 5CO readiness/transition preservation records, real-record blockers, combined-gate and activation nonauthorization records, Stage 5CM/5CK/5CI/5CG/5CE/5CC/5BD preservation records, no-active/no-byte/no-execution transition-gate records, `codex-output` handoff restoration records, credential-redaction preservation records, and source-digest/reviewability records only. It does not publish generated result bodies, byte streams, decoded bytes, score summaries, SQLite databases, local reports, actual operator decisions, actual approval decisions, actual activation decisions, or active String 4 inputs. Generated Stage 5CQ diagnostics remain ignored under `experiments/results/token-block/stage5cq/`.

## Purpose

Define result, manifest, source-lock, observation, and generated-output record policy for the workbench.

## Current Schema State

The repository now includes committed schema families for solved-baseline records, result-store records, bounded experiment manifests, archive/image/web observations, hash preimage packs, Discord ingestion/review/promotion records, full Discord review bundle records, post-Discord manifests, GP/rune claim records, image-transform records, stego/OutGuess regression records, Stage 3Y research-synthesis ledgers, Stage 4B source-lock/visual-intake records, Stage 4D bounded numeric records, Stage 4E source-delta/image-artifact backlog records, Stage 4F historical stego/audio fixture source-lock records, Stage 4G cookie refresh records, Stage 4H CPU batch/parity records, Stage 4I scoring records, Stage 4J observation review records, Stage 4K public source-lock snapshot records, Stage 4L observation promotion ledger records, Stage 4M image source-variant/compression preflight records, Stage 4N stego/audio positive-control readiness records, Stage 4O CPU batch adapter expansion/parity expectation records, Stage 4P result-store/score-summary unification records, Stage 4Q benchmark/parity planning records, Stage 5A CUDA planning/parity scaffold records, Stage 5B CUDA parity harness skeleton records, Stage 5C CUDA build/device detection records, Stage 5D native CPU backend/threading records, Stage 5E first CUDA kernel contract records, Stage 5F synthetic CUDA kernel/parity records, Stage 5G CUDA parity-reporting/device-code audit records, Stage 5H Gematria mod-29 shift-score contract records, Stage 5I Gematria CUDA preparation records, Stage 5J Gematria CUDA kernel implementation/build/parity records, Stage 5K Gematria CUDA parity-reporting/preflight records, Stage 5L solved-fixture token-mapping/native parity records, Stage 5M solved-fixture CUDA run/parity/boundary records, Stage 5N solved-fixture CUDA reporting/gate records, Stage 5O solved-fixture CUDA repeat/result-store preflight records, Stage 5P Gematria CUDA result-store/score-summary integration records, Stage 5Q Gematria expansion candidate-mapping records, Stage 5R expanded solved-fixture CUDA parity records, Stage 5S expanded CUDA parity reporting/result-store integration records, Stage 5T solved-family CUDA readiness matrix records, Stage 5U Candidate Batch ABI/backend contract records, Stage 5V native Candidate Batch ABI conformance records, Stage 5W prime-minus-one native contract records, Stage 5X prime-minus-one native parity records, Stage 5Y prime-minus-one native reporting/readiness records, Stage 5Z prime-minus-one CUDA contract records, Stage 5AA prime-minus-one CUDA synthetic records, Stage 5AB project-state/doc-staleness records, Stage 5AC prime-minus-one CUDA synthetic reporting/preflight records, Stage 5AD bounded p56 CUDA parity records, Stage 5AD-fix bounded p56 mismatch investigation records, Stage 5AE corrected bounded p56 formula reporting/reference-contract repair records, Stage 5AF source-harvester/source-lock planning records, Stage 5AG local source inventory/source-lock metadata records, Stage 5AH stage-ledger/doc-staleness coverage records, Stage 5AI curated research-bundle extraction records, Stage 5AJ UsefulFilesAndIdeas source-harvester/extraction-fidelity records, Stage 5AK community-facts claim-record schemas, Stage 5AL website-ingest/publication-gate/Deep-Research-export schemas, Stage 5AM static website renderer schemas, Stage 5AN private Deep Research export schemas, Stage 5AP token-block/stego-control source-lock schemas, Stage 5AR original-image coordinate-lock schemas, Stage 5AT token case-review pack schemas, Stage 5AU review-pack usability/crop-quality schemas, Stage 5AV token-case decision integration and branch-manifest schemas, Stage 5AW decision-parser repair and superseding branch-manifest schemas, Stage 5AX parallel validation harness schemas, Stage 5AY bounded preflight manifest design schemas, Stage 5AZ preflight manifest-integrity repair schemas, Stage 5BD token-block dry-run planning schemas, Stage 5BF historical-route source-lock schemas, Stage 5BO operator-errata schemas, Stage 5BQ inactive-branch dry-run planning schemas, Stage 5BS planning-ingestion gate/future-runner citation schemas, Stage 5CA inactive-sidecar review-contract schemas, Stage 5CC active-planning-input preflight/no-byte-transition schemas, Stage 5CE proposal-package/operator-gate schemas, Stage 5CG approval-gate decision-scaffold schemas, Stage 5CI approval-template/activation-decision hardening schemas, Stage 5CK approval-fixture/review-package schemas, Stage 5CM approval-readiness-boundary/fixture-vs-real/credential-redaction schemas, Stage 5CO real approval-readiness package/activation-transition schemas, and Stage 5CQ operator-decision package scaffold/review-integration schemas.

Stage 5CO schemas cover Stage 5CN findings integration, reviewable stage markers, validation evidence, source-digest indexes, reviewability gaps, record-family filename-equivalence maps, real approval-record readiness packages, real operator approval readiness preflight, real Deep Research acceptance readiness preflight, real combined-gate validation readiness preflight, activation-decision transition plans, future transition sequences, current missing-requirements registers, real-record blockers, Stage 5CM/5CK/5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, no-active-ingestion proofs, no-byte-stream transition gates, no-execution transition gates, manifest-supersession nonactivation proofs, sidecar activation blockers, activation-decision nonauthorization proofs, DWH quarantine reaffirmation, source-gap severity updates, guardrails, credential-redaction/no-secret policy preservation, Codex handoff policy, review-packaging warnings, next-stage decisions, and aggregate summaries. They require actual approval records absent, Deep Research acceptance records absent, combined approval gate satisfied false, activation decision valid false, active-planning input authorization false, active-planning input selection false, String 4 active input false, dry-run ingestion false, byte-stream generation false, execution false, Stage 5BD run-plan IDs unchanged, manifest supersession false, generated outputs and Codex outputs uncommitted, Stage 5CO-and-later local validation capped at 8 workers, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5CQ schemas cover Stage 5CP findings integration, reviewable stage markers, validation evidence, source-digest indexes, reviewability gaps, record-family filename-equivalence maps, operator-decision package scaffold records, operator-decision nonauthorization proofs, combined-gate non-satisfaction proofs, activation-decision nonauthorization proofs, real-record creation blockers, Stage 5CO readiness/missing-requirements/transition preservation, Stage 5CM/5CK/5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, no-active-ingestion proofs, no-byte-stream transition gates, no-execution transition gates, manifest-supersession nonactivation proofs, sidecar activation blockers, Codex handoff restoration records, credential-redaction/no-secret policy preservation, review-packaging warnings, next-stage decisions, and aggregate summaries. They require actual operator decisions absent, actual approval records absent, Deep Research acceptance records absent, combined approval gate satisfied false, activation decision valid false, active-planning input authorization false, active-planning input selection false, String 4 active input false, dry-run ingestion false, byte-stream generation false, execution false, Stage 5BD run-plan IDs unchanged, manifest supersession false, generated outputs and Codex outputs uncommitted, Stage 5CQ-and-later local validation capped at 8 workers, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5CM schemas cover Stage 5CL findings integration, reviewable stage markers, validation evidence, source-digest indexes, reviewability gaps, Stage 5CK fixture preservation, Stage 5CI template preservation, Stage 5CG scaffold preservation, Stage 5CE proposal-package preservation, Stage 5CC contract preservation, approval-readiness boundary contracts, fixture-vs-real negative validation, end-to-end readiness-boundary validation, future real approval-readiness preflight, activation-decision gate hardening, credential-redaction/no-secret policy, no-byte-stream transition gates, no-execution transition gates, manifest-supersession nonactivation proof, Stage 5BD plan preservation, active-lineage preservation, DWH quarantine reaffirmation, guardrails, Codex handoff policy, next-stage decisions, and aggregate summaries. They require fixtures to remain fixtures only, actual approval records absent, approval gate satisfied false, activation decision valid false, active-planning input authorization false, String 4 active input false, dry-run ingestion false, byte-stream generation false, execution false, Stage 5BD run-plan IDs unchanged, manifest supersession false, generated outputs and Codex outputs uncommitted, Stage 5CM-and-later local validation capped at 8 workers, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5CI schemas cover Stage 5CH findings integration, reviewable stage markers, validation evidence, source-digest indexes, reviewability gaps, Stage 5CG scaffold preservation, Stage 5CE proposal-package preservation, Stage 5CC contract preservation, future operator approval record templates, future Deep Research acceptance templates, combined approval-gate validation preflight, combined approval-gate non-satisfaction proofs, active-planning-input activation-decision templates, negative validation contracts, no-byte-stream transition gates, no-execution transition gates, manifest-supersession nonactivation proof, Stage 5BD plan preservation, active-lineage preservation, DWH quarantine reaffirmation, guardrails, Codex handoff policy, next-stage decisions, and aggregate summaries. They require templates to remain templates only, actual approval records absent, approval gate satisfied false, activation decision valid false, active-planning input authorization false, String 4 active input false, dry-run ingestion false, byte-stream generation false, execution false, Stage 5BD run-plan IDs unchanged, manifest supersession false, generated outputs and Codex outputs uncommitted, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5CG schemas cover Stage 5CF findings integration, reviewable stage markers, validation evidence, source-digest indexes, reviewability gaps, Stage 5CE proposal-package/gate preservation, Stage 5CC contract preservation, operator approval decision scaffolds, Deep Research acceptance decision scaffolds, combined approval-gate scaffolds, active-planning-input decision scaffolds, Stage 5CE wording review, no-byte-stream transition gate, no-execution transition gate, manifest-supersession nonactivation proof, Stage 5BD plan preservation, active-lineage preservation, DWH quarantine reaffirmation, guardrails, Codex handoff policy, next-stage decisions, and aggregate summaries. They require active-planning input authorization false, approval gate satisfied false, approval records absent now, String 4 active input false, dry-run ingestion false, byte-stream generation false, execution false, Stage 5BD run-plan IDs unchanged, manifest supersession false, generated outputs and Codex outputs uncommitted, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5CC schemas cover Stage 5CB findings integration, Stage 5CA contract preservation, exact fail-closed trigger and activation-precondition contracts, non-gate-opening extension policies, active-planning-input proposal preflight, no-byte-stream transition gate, no-execution transition gate, manifest-supersession nonactivation proof, Stage 5BD plan preservation, active-lineage preservation, no-active-ingestion proof, DWH quarantine reaffirmation, guardrails, Codex handoff policy, next-stage decisions, and aggregate summaries. They require active-planning input authorization false, String 4 active input false, dry-run ingestion false, byte-stream generation false, execution false, Stage 5BD run-plan IDs unchanged, manifest supersession false, generated outputs and Codex outputs uncommitted, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5BS schemas cover Stage 5BR findings integration, reviewable stage markers, validation evidence, source-digest indexes, reviewability gaps, String 4 planning-ingestion gate records, future-runner citation policy, inactive-sidecar consumption policy, active-ingestion blockers, no-active-ingestion proofs, gate readiness matrices, manifest validation requirements, Stage 5BD plan preservation, active-manifest preservation, source-gap updates, DWH quarantine reaffirmation, guardrails, Codex handoff policy, next-stage decisions, and aggregate summaries. They require `stage5br_verdict=accept_with_warnings`, `string4_planning_ingestion_gate_status=closed_gate_no_active_ingestion`, `future_runner_citation_status=citation_required_fail_closed`, `string4_active_input_allowed=false`, `string4_dry_run_ingestion_allowed_now=false`, Stage 5BD records valid, canonical transcription and active manifest changes false, generated outputs and Codex outputs uncommitted, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5BQ token-block schemas cover Stage 5BP findings integration, review-packaging warnings, String 4 inactive branch planning context, operator-errata sidecar status, errata-aware dry-run constraint updates, no-active-ingestion proof, future dry-run requirements, active-manifest preservation, Stage 5BD dry-run lineage preservation, future planning impact, source-gap severity updates, DWH quarantine reaffirmation, guardrails, Codex handoff policy, next-stage decision, and aggregate summaries. They require `string4_active_input_allowed=false`, `string4_dry_run_ingestion_allowed_now=false`, `stage5bo_errata_aware_universe_active=false`, canonical transcription and active manifest changes false, Stage 5BD records valid, generated outputs and Codex outputs uncommitted, no token experiments, no byte streams, no DWH/hash/preimage search, no decode, no scoring, no CUDA, no benchmark, no website expansion, and no solve claim.

Stage 5BF historical-route schemas cover local archive location, archive tree summaries, source inventory summaries, annual route inventories, high-priority artifact indexes, artifact-family taxonomy, trust-classification policy and records, PGP/stego/OutGuess/OpenPuff/MP3/magic-square/hex-JPEG/onion/book-code/network-byte-channel/Liber Primus candidate records, historical technique taxonomy, token-block planning impact, source-gap register, Deep Research readiness, DWH historical context, guardrails, and aggregate project-state summaries. They require local-only source-lock behavior, raw archive files and generated reports uncommitted, network clone/fetch false, PGP network key fetch false, stego/OutGuess/OpenPuff/MP3Stego execution false, token experiments and byte-stream generation false, DWH/hash/preimage search false, OCR/AI/ML/LLM-vision/semantic-image/hidden-content forensics false, CUDA/benchmark/scored-experiment flags false, and solve claims false.

Stage 5BD token-block schemas cover dry-run policy, active-manifest locks, run-plan ID policy and registry, no-output dry-run plan manifests, future result-path policy and validation, branch/null/control family counters, dry-run report schema policy, fixture-only result examples, execution-gate dry-run validation, no-byte-stream proof, Stage 5BB validation-evidence consolidation, archive marker policy, DWH dry-run context, guardrails, archive review markers, and aggregate project-state summaries. They require Stage 5AW repaired branch metadata and Stage 5AZ repaired variant-family/design/budget/gate records to be active, Stage 5AV and Stage 5AY superseded manifests to be inactive as active inputs, fixture records to remain synthetic-only, future result paths to be validated but unwritten, real byte streams and variant outputs to remain false, and OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/hash-preimage/decode/scoring/CUDA/benchmark/scored-experiment flags and solve claims to remain false.

Stage 5AZ token-block schemas cover preflight manifest integrity audits, family-ID uniqueness audits, manifest-reference audits, taxonomy-membership policy, repaired bounded variant-family manifests, repaired design policies, repaired branch-count budgets, repaired execution gates, Deep Research readiness, DWH manifest-integrity context, guardrails, and aggregate project-state summaries. They require the duplicate family-ID count to become zero after repair, `unresolved_as_current_only` to be represented as one family record with multiple taxonomy memberships, Stage 5AW repaired branch metadata to remain active, Stage 5AV branch metadata to remain inactive, branch budgets to remain unchanged, execution gates to remain blocked, DWH/hash search to remain blocked, and OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/CUDA/benchmark/scored-experiment flags and solve claims to remain false.

Stage 5AY token-block schemas cover preflight source inputs, design policy, branch eligibility policy, bounded variant family manifests, null/alphabet/reading-order/page-split/source controls, branch-count budget, future result schema preview, execution gates, DWH preflight context, guardrails, and aggregate project-state summaries. They require Stage 5AW repaired branch metadata to be used, Stage 5AV branch metadata to remain superseded for planning, full Cartesian enumeration and byte-stream generation to remain false, future result records to be preview-only, DWH/hash search to remain blocked, and OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/CUDA/benchmark/scored-experiment flags and solve claims to remain false.

Stage 5AX CI/project-state schemas cover parallel validation plans, command registries, run policies, run summaries, safety audits, pytest shard plans, guardrails, and aggregate summaries. They require generated validation outputs to remain uncommitted, worker counts to remain capped, git/GitHub/network/generated-output-writing commands to stay out of the parallel scheduler, validation timings to be labelled as non-cryptanalytic diagnostics, and OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/hash-preimage/token-experiment/CUDA/benchmark/scored-experiment flags and solve claims to remain false.

Stage 5AW token-block schemas cover decision-parser audits, possible-token parser policy, repaired human-review decision records, repaired unresolved-token variant records, repaired reviewer-extra possible-token records, malformed possible-token fragment audits, repaired primary-60 impact summaries, repaired compact branch manifests, guardrails, and aggregate project-state summaries. They require prose fragments to be excluded from reviewer-extra tokens, visual placeholders to remain primary-60 unmappable and ineligible for variant byte streams, canonical transcription changes to remain false, variant byte-stream generation and full Cartesian enumeration to remain false, and OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/hash-preimage/CUDA/benchmark/scored-experiment flags and solve claims to remain false.

Stage 5AV token-block schemas cover decision-file ingest, decision validation, human-review decision records, confirmed-token records, unresolved-token variant records, reviewer-extra possible tokens, primary-60 variant impact summaries, compact branch manifests, canonical transcription non-updates, null-control updates, DWH decision context, guardrails, and aggregate project-state summaries. They require canonical transcription changes, full Cartesian enumeration, variant byte-stream generation, experiment execution, OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/hash-preimage/CUDA/benchmark/scored-experiment flags, generated-output commits, raw-data commits, and solve claims to remain false.

Stage 5AU token-block schemas cover Stage 5AT usability audits, crop-geometry policies, crop-quality diagnostics, v2 case-review challenge records, v2 canonical-transcription challenge records, v2 review-pack manifests, UI coverage, blank human decision templates, null-control updates, DWH review-pack context, guardrails, and aggregate project-state summaries. They require generated review-pack bodies and generated crops to remain uncommitted, derived crops to remain review aids rather than source truth, canonical transcription changes to remain false, human decisions to remain absent until manual review, OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/hash-preimage/CUDA/benchmark/scored-experiment flags to remain false, and solve claims to remain false.

Stage 5AT token-block schemas cover case-review policy, grouped case-review challenge records, canonical-transcription challenge records, crop manifests, human review decision templates, review-pack manifests, variant-classifier repair summaries, doc-drift repair summaries, null-control case updates, DWH case context, guardrails, and aggregate project-state summaries. They require active ambiguity classes to stay aligned with committed Stage 5AR data, generated review packs to remain uncommitted, canonical transcription changes to remain false, human decisions to remain absent until manual review, OCR/AI/ML/LLM-vision/semantic-image/hidden-content/stego/decode/hash-preimage/CUDA/benchmark/scored-experiment flags to remain false, and solve claims to remain false.

Stage 5AR token-block schemas cover original page-image source locks, image-variant classification, page-split policy and records, token pixel-coordinate policy and records, token case policy and ambiguity records, coordinate validation, source-lock/null-control updates, DWH coordinate context, and aggregate project-state summaries. They require original images as coordinate truth, reject screenshots/crops/modified/web-rendered/private generated images as coordinate sources, keep raw images and generated coordinate reports uncommitted, keep OCR/AI/ML/semantic-image/hidden-content/stego/decode/hash-preimage/CUDA/benchmark/scored-experiment flags false, and require solve claims to remain false.

Stage 5AP token-block schemas cover page 49-51 source locks, image provenance, canonical token transcription, logical coordinate records, candidate alphabet registry, primary-60 mapping preflight, null-control planning, Deep Web Hash context, OutGuess positive-control policy, toolchain readiness, control matrix, historical fixture readiness, guardrails, and aggregate project-state summaries. They require raw images and generated outputs to remain uncommitted, OCR/AI/ML/image-forensics/stego execution/hash-preimage/CUDA/benchmark/scored-experiment flags to remain false, and solve claims to remain false.

Stage 5AN deep-research-export schemas cover content-pack policy, inputs, manifest summaries, hosted-content export summaries, combined-webroot summaries, file-selection summaries, publication-gate audits, upload instructions, Deep Research consumption guides, and aggregate Stage 5AN summaries. They require private/generated output paths to remain ignored, public website-ready to stay zero, raw third-party files to be excluded, noindex/robots validation, and Deep Research/CUDA/benchmark/scored-experiment/solve-claim flags to remain false.

Stage 5AK source-harvester schemas cover community-facts local inventory records, ordered attachment indexes, source-card summaries, content-index summaries, clue-category records, claim policy, claim records, correction logs, arithmetic preflight records, and the Stage 5AK aggregate summary. They require raw message/image commits, generated extraction-body commits, network fetches, live scraping, online clones, Google Drive storage, OCR, AI/ML interpretation, image forensics, stego/audio execution, hypothesis generation/execution, CUDA, benchmarks, scored experiments, website expansion, method-status upgrades, and solve claims to remain false. Generated bodies remain ignored under `research-inputs/stage5ak/`; generated reports remain ignored under `experiments/results/research-bundles/stage5ak/` and `experiments/results/source-harvester-community-facts/stage5ak/`.

Stage 5AL website-ingest schemas cover research indexes, bundle cards, source cards, content records, community-claim metadata, publication gates, private Deep Research export records, and Stage 5AL summaries. They require public website-ready to stay zero, raw/publication flags to stay false, claim body fields to be omitted from committed website-ingest records, and Deep Research/CUDA/benchmark/scored-experiment/solve-claim flags to remain false. Generated private export files remain ignored under `research-inputs/stage5al/`; generated validation reports remain ignored under `experiments/results/website-ingest/stage5al/`.

Stage 5AM website-render schemas cover render policies, render inputs, static output manifests, site validation, privacy/publication audits, upload instructions, and the Stage 5AM summary. They require metadata-only rendering, public website-ready `0`, raw bodies and private identifiers absent, noindex/robots validation, generated static export files ignored under `website-export/stage5am/`, generated renderer reports ignored under `experiments/results/website-render/stage5am/`, and Deep Research/CUDA/benchmark/scored-experiment/solve-claim flags to remain false.

Stage 5AB project-state schemas cover document-staleness source-of-truth records, finding records, operational file-map records, and the Stage 5AB summary. They require no CUDA execution, no CUDA source changes, no new kernels, no benchmark, no scored experiment, no website expansion, no raw-data processing, no generated-output publication, and no solve claim.

Stage 5AC CUDA schemas cover compact synthetic parity report records, result-store integration records, score-summary integration records, method-status impact records, generated-body policy records, bounded-p56 preflight records, full-p56 blocker records, scored-experiment deferral records, doc-staleness validation records, next-stage decision records, and the Stage 5AC summary. They require no Stage 5AC CUDA execution, no CUDA source changes, no new kernels, no native execution, no benchmark, no scored experiment execution, no generated-body publication, no raw-data processing, no method-status upgrade, and no solve claim.

Stage 5AD CUDA schemas cover bounded p56 run records, parity records, result-store preflight records, score-summary preflight records, full-p56 blocker records, scored-experiment deferral records, doc-staleness validation records, device-subset audit records, next-stage decision records, and the Stage 5AD summary. They allow only the bounded vector run, require no full p56 or unsolved-page CUDA, no new kernels, no CUDA device arithmetic modification, no benchmark, no scored experiment execution, no generated-body publication, no raw-data processing, no method-status upgrade, and no solve claim.

Stage 5AD-fix CUDA schemas cover mismatch hash-lineage, token trace, stream trace, formula trace, hash-material, reference-contract, root-cause, repair-readiness, guardrail, next-stage decision, and summary records. They require no solve claim, no CUDA execution, no raw-data processing, no generated-output publication, no new kernels, no CUDA source modification, and explicit preservation of the Stage 5AD historical failure.

Stage 5AE CUDA schemas cover corrected formula-parity reports, reference-contract repair, hash-material policy, result-store and score-summary integration, method-status impact, generated-body policy, full-p56 blockers, scored-experiment deferral, archive/source-lock deferral, doc-staleness validation, next-stage decision, and summary records. They require Stage 5AD historical failure preservation, corrected formula hash `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`, no solve claim, no CUDA execution, no raw/archive-data processing, no generated-output publication, no new kernels, no CUDA source modification, and no Stage 5AD reclassification as passed.

Stage 5AF source-harvester schemas cover source records, manifests, harvest plans, failure records, file/hash inventories, extracted-page summaries, research-bundle plans, clue-target categories, next-stage decisions, and source-harvester summaries. They require dry-run-safe defaults, local-only raw output policy, no Google Drive project storage, no raw downloads committed, no raw archive processing, no CUDA execution, no benchmarks, no scored experiments, and no solve claim.

Stage 5AG local source inventory schemas cover local source-root summaries, file inventory summaries, archive inventory summaries, hash inventory summaries, manifest-local linkage, local source-manifest extensions, source-lock candidate summaries, local source gap reports, research-bundle readiness, guardrail records, next-stage decisions, and the Stage 5AG summary. They require metadata-only records, ignored full inventories, no raw third-party source commits, no Google Drive storage, no network fetch or online clone, no Deep Research execution, no CUDA execution/source changes/kernels, no benchmarks, no scored experiments, no generated-output publication, and no solve claim.

Stage 5AH doc-staleness schemas cover stage-ledger staleness records, stage-ledger coverage summaries, operational-file-map coverage records, and the Stage 5AH doc-staleness summary. They require generated-output publication to remain false, raw data processing to remain false, CUDA execution/source changes/kernels to remain absent, and solve claims to remain false.

Stage 5AI source-harvester schemas cover curated-bundle extraction policy, curated source-card summaries, curated content-index summaries, website-ingest source-card/bundle/content records, Deep-Research pack format records, unclassified source classifications, missing-source plans, and the Stage 5AI curated research-bundle summary. They require raw content commits, generated extract commits, network fetches, online clones, Google Drive storage, OCR, AI/ML interpretation, image/stego/audio execution, CUDA, benchmarks, scored experiments, website expansion, method-status upgrades, and solve claims to remain false. Generated bundle bodies remain ignored under `research-inputs/stage5ai/`; generated reports remain ignored under `experiments/results/research-bundles/stage5ai/`.

Stage 5AJ source-harvester schemas cover UsefulFiles local inventory records, source-manifest extension records, XLSX extraction summaries, important-link source indexes, extraction-fidelity policies, redaction policies, scraper-capture policies, Deep-Research pack update summaries, and the Stage 5AJ aggregate summary. They require raw workbook/image/text commits, generated extraction-body commits, network fetches, live scraping, online clones, Google Drive storage, OCR, AI/ML interpretation, image forensics, stego/audio execution, CUDA, benchmarks, scored experiments, website expansion, method-status upgrades, and solve claims to remain false. Generated bodies remain ignored under `research-inputs/stage5aj/`; generated reports remain ignored under `experiments/results/research-bundles/stage5aj/` and `experiments/results/source-harvester-usefulfiles/stage5aj/`.

Generated candidate records, SQLite databases, local review indexes, derived images, topic shards, extraction payloads, and full run outputs remain ignored unless a future stage explicitly promotes a summary or curated record.

Stage 5P Gematria CUDA result-store integration records require `compact_summary_only=true`,
`stage4p_compatibility=true`, `stage4i_compatibility=true`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`method_status_upgrade_allowed=false`, `cuda_execution_performed=false`,
`cuda_source_modified=false`, `new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, and `solve_claim=false`. Generated JSON
reports remain ignored under `experiments/results/gematria-cuda-result-store/stage5p/`; only
compact YAML records under `data/cuda/` are committed.

Stage 5P schemas include `gematria-cuda-result-store-integration-record-v0`,
`gematria-cuda-score-summary-integration-record-v0`,
`gematria-cuda-method-status-impact-record-v0`,
`gematria-cuda-generated-body-policy-record-v0`,
`gematria-cuda-controlled-expansion-candidate-record-v0`, and
`stage5p-cuda-result-store-integration-summary-v0`.

Stage 5Q Gematria expansion candidate-mapping records require `compact_summary_only=true`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`, `cuda_execution_performed=false`,
`cuda_source_modified=false`, `new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, `method_status_upgrade_allowed=false`,
and `solve_claim=false`. Generated JSON reports remain ignored under
`experiments/results/gematria-expansion-candidate-mapping/stage5q/`; only compact YAML records
under `data/cuda/` are committed.

Stage 5Q schemas include `gematria-expansion-candidate-inventory-record-v0`,
`gematria-expansion-token-mapping-record-v0`, `gematria-expansion-native-parity-record-v0`,
`gematria-expansion-result-store-preflight-record-v0`, `gematria-expansion-gate-record-v0`, and
`stage5q-expansion-candidate-mapping-summary-v0`.

Stage 5R expanded solved-fixture CUDA parity records allow CUDA execution only for the three
Stage 5Q mapped direct-translation candidates. They require `new_cuda_kernel_added=false`,
`new_cuda_kernels_added=0`, `device_kernel_arithmetic_modified=false`,
`unsolved_page_cuda_used=false`, `real_liber_primus_cuda_data_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`, `method_status_upgrade_allowed=false`,
and `solve_claim=false`. Generated JSON reports remain ignored under
`experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/`; only compact YAML records
under `data/cuda/` are committed.

Stage 5R schemas include `gematria-expanded-solved-fixture-cuda-run-record-v0`,
`gematria-expanded-solved-fixture-cuda-parity-record-v0`,
`gematria-expanded-solved-fixture-cuda-boundary-record-v0`,
`gematria-expanded-solved-fixture-result-store-preflight-record-v0`,
`gematria-expanded-solved-fixture-score-summary-preflight-record-v0`, and
`stage5r-expanded-solved-fixture-cuda-parity-summary-v0`.

Stage 5S schemas include `gematria-expanded-cuda-parity-report-record-v0`,
`gematria-expanded-cuda-result-store-integration-record-v0`,
`gematria-expanded-cuda-score-summary-integration-record-v0`,
`gematria-expanded-cuda-method-status-impact-record-v0`,
`gematria-expanded-cuda-generated-body-policy-record-v0`,
`gematria-expanded-cuda-boundary-review-record-v0`,
`gematria-expanded-cuda-next-step-decision-record-v0`, and
`stage5s-expanded-cuda-result-store-integration-summary-v0`.

Stage 5T schemas include `solved-family-cuda-inventory-record-v0`,
`solved-family-cuda-parity-matrix-record-v0`, `cuda-kernel-readiness-record-v0`,
`cuda-candidate-batch-abi-gap-record-v0`, `cuda-benchmark-readiness-record-v0`,
`cuda-no-unsolved-guardrail-review-record-v0`, `cuda-next-stage-decision-record-v0`, and
`stage5t-cuda-solved-family-readiness-summary-v0`. Stage 5T records require
`cuda_execution_performed=false`, `cuda_source_modified=false`, `new_cuda_kernel_added=false`,
`new_cuda_kernels_added=0`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `unsolved_page_cuda_used=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`, `method_status_upgraded=false`,
`solve_claim=false`, and `no_solve_claim=true`. Generated reports remain ignored under
`experiments/results/cuda-solved-family-readiness/stage5t/`.

Stage 5U schemas include `candidate-batch-abi-record-v0`,
`token-buffer-contract-record-v0`, `transform-parameter-contract-record-v0`,
`key-schedule-contract-record-v0`, `stream-schedule-contract-record-v0`,
`score-vector-contract-record-v0`, `topk-output-contract-record-v0`,
`backend-surface-contract-record-v0`,
`candidate-batch-result-store-compatibility-record-v0`,
`candidate-batch-abi-gap-closure-record-v0`, and
`stage5u-candidate-batch-abi-summary-v0`. Stage 5U records require
`metadata_only=true`, `contract_only=true`, `cuda_execution_performed=false`,
`cuda_source_modified=false`, `new_cuda_kernel_added=false`,
`new_cuda_kernels_added=0`, `gpu_benchmark_performed=false`,
`performance_claim=false`, `speedup_claim=false`, `unsolved_page_cuda_used=false`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`,
`method_status_upgraded=false`, `solve_claim=false`, and `no_solve_claim=true`.
Generated reports remain ignored under
`experiments/results/cuda-candidate-batch-abi/stage5u/`.

Stage 5V schemas include `native-candidate-batch-adapter-record-v0`,
`candidate-batch-conformance-fixture-record-v0`,
`token-buffer-conformance-record-v0`, `schedule-conformance-record-v0`,
`score-vector-conformance-record-v0`, `topk-conformance-record-v0`,
`native-conformance-result-store-record-v0`,
`candidate-batch-abi-implementation-status-record-v0`, and
`stage5v-native-candidate-batch-conformance-summary-v0`. Stage 5V records require
`native_cpu_execution_performed=false`, `python_reference_adapter_implemented=true`,
`cpp_reference_adapter_implemented=false`, `cuda_execution_performed=false`,
`cuda_source_modified=false`, `new_cuda_kernel_added=false`,
`new_cuda_kernels_added=0`, `gpu_benchmark_performed=false`,
`performance_claim=false`, `speedup_claim=false`, `unsolved_page_cuda_used=false`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`,
`method_status_upgraded=false`, `solve_claim=false`, and `no_solve_claim=true`.
Generated reports remain ignored under
`experiments/results/cuda-candidate-batch-abi-conformance/stage5v/`.

Stage 5W schemas include `prime-minus-one-source-inventory-record-v0`,
`prime-minus-one-stream-contract-record-v0`, `prime-minus-one-schedule-record-v0`,
`prime-minus-one-candidate-batch-mapping-record-v0`,
`prime-minus-one-native-parity-preparation-record-v0`,
`prime-minus-one-result-store-preflight-record-v0`,
`prime-minus-one-guardrail-record-v0`,
`prime-minus-one-next-stage-decision-record-v0`, and
`stage5w-prime-minus-one-native-contract-summary-v0`. Stage 5W records require
`metadata_only=true`, `contract_preparation_only=true`,
`native_execution_performed=false`, `python_reference_execution_performed=false`,
`cuda_execution_performed=false`, `cuda_source_modified=false`,
`new_cuda_kernel_added=false`, `new_cuda_kernels_added=0`,
`gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `unsolved_page_cuda_used=false`,
`generated_body_publication_allowed=false`, `generated_outputs_committed=false`,
`raw_data_processed=false`, `codex_output_committed=false`,
`method_status_upgraded=false`, `solve_claim=false`, and `no_solve_claim=true`.
Generated reports remain ignored under
`experiments/results/prime-minus-one-native-contract/stage5w/`.

Stage 5X schemas include `prime-minus-one-native-run-record-v0`,
`prime-minus-one-native-parity-record-v0`,
`prime-minus-one-native-result-store-preflight-record-v0`,
`prime-minus-one-native-score-summary-preflight-record-v0`,
`prime-minus-one-full-p56-blocker-record-v0`,
`prime-minus-one-native-guardrail-record-v0`,
`prime-minus-one-native-next-stage-decision-record-v0`, and
`stage5x-prime-minus-one-native-parity-summary-v0`. Stage 5X records require
CUDA execution, CUDA source changes, new kernels, native/CUDA CMake execution, GPU benchmarks,
speedup claims, generated-output commits, raw-data processing, full p56 execution, method-status
upgrades, and solve claims to remain false. Generated reports stay ignored under
`experiments/results/prime-minus-one-native-parity/stage5x/`.

Stage 5Y schemas include `prime-minus-one-native-parity-report-record-v0`,
`prime-minus-one-native-result-store-integration-record-v0`,
`prime-minus-one-native-score-summary-integration-record-v0`,
`prime-minus-one-native-method-status-impact-record-v0`,
`prime-minus-one-generated-body-policy-record-v0`,
`prime-minus-one-full-p56-blocker-preservation-record-v0`,
`prime-minus-one-cuda-contract-readiness-gate-record-v0`,
`bounded-scored-experiment-readiness-record-v0`,
`prime-minus-one-native-reporting-guardrail-record-v0`,
`prime-minus-one-native-reporting-next-stage-decision-record-v0`, and
`stage5y-prime-minus-one-native-reporting-summary-v0`. Stage 5Y records require
native execution, CUDA execution, CUDA source changes, new kernels, GPU benchmarks,
speedup claims, generated-output commits, raw-data processing, method-status upgrades,
and solve claims to remain false. Generated reports stay ignored under
`experiments/results/prime-minus-one-native-reporting/stage5y/`.

Stage 3Y research-synthesis records under `data/research/` are committed source-of-truth metadata, not generated experiment outputs. They must keep `solve_claim=false`, record method-family status/reopen conditions, and preserve no-broadening guardrails for noisy, negative, inconclusive, deferred, or infrastructure-only families.

Stage 4B records under `data/observations/archive/`, `data/locks/third-party/`, `data/observations/visual/`, `data/observations/research/`, and `data/observations/web/` are committed source/observation metadata. They must keep `trusted_as_canonical=false` and `solve_claim=false`; visual records must also keep `usable_as_experiment_seed=false`. Stage 4B disabled manifests must keep `execution_enabled=false`, `cuda_enabled=false`, and `no_solve_claim=true`.

Stage 4C records under `data/observations/visual/` are committed annotation task metadata. They must keep `trusted_as_canonical=false`, `usable_as_experiment_seed=false`, and `solve_claim=false`. Generated annotation sites, page-image copies, grid overlays, and blank templates remain ignored.

Stage 4D bounded numeric verifier records are generated JSON/JSONL outputs under `experiments/results/bounded-numeric/stage4d/`. They must keep `solve_claim=false`, `cuda_used=false`, `trusted_as_canonical=false`, `no_fudge_policy=true`, and `generated_outputs_committed=false`. Raw values and derived values must stay separated, and every derived value must record a formula and source.

Stage 4E source-delta records are committed metadata records only. They must keep `raw_file_committed=false`, `binary_committed=false`, `font_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`. Generated tree reports remain ignored under `experiments/results/source-delta/stage4e/`.

Stage 4F stego/audio fixture source records are committed metadata records only. They must keep `raw_file_committed=false`, `binary_committed=false`, `audio_committed=false`, `image_committed=false`, `font_committed=false`, `extracted_payload_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`. Future fixture manifests must keep `execution_enabled=false`. Generated fixture reports remain ignored under `experiments/results/stego-fixtures/stage4f/`.

Stage 4G cookie refresh schemas require exact-match-only records: `no_solve_claim=true`, `cuda_used=false`, `cloud_execution=false`, `hashcat_used=false`, `fuzzy_matching=false`, `partial_matching=false`, manifest-declared variants and algorithms, and source-backed base strings. Generated candidate/exact-match JSONL and summary JSON remain ignored under `experiments/results/cookie-refresh/stage4g/`; only the aggregate YAML summary is committed.

Stage 4H CPU batch records require `cpu_only=true`, `cuda_used=false`, `cuda_required=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `generated_outputs_committed=false`. Generated result JSONL and summary JSON remain ignored under `experiments/results/cpu-batch/stage4h/`; only the aggregate YAML summary and parity contract are committed.

Stage 4I scoring records require finite confidence labels, scorer IDs/versions, calibration-profile references where available, `solve_claim=false`, `trusted_as_canonical=false`, and `cuda_used=false`. Generated scorer inventories and rendered calibration reports remain ignored under `experiments/results/scoring-consolidation/stage4i/`.

Stage 4J observation review records require explicit review states, promotion gates, quarantine/control records, `solve_claim=false`, `trusted_as_canonical=false`, and `usable_as_experiment_seed=false` unless a future explicit promotion stage changes that with review evidence. Generated review decision, quarantine, promotion-gate, and path-sanitisation reports remain ignored under `experiments/results/observation-review/stage4j/`.

Stage 4K source-lock snapshot records require `raw_private_data_committed=false`,
`binary_committed=false`, `image_committed=false`, `audio_committed=false`, `font_committed=false`,
`archive_committed=false`, and `solve_claim=false`. Fetched records require content hashes, and
committed snapshots are restricted to explicitly allowed small text snapshot policy. Generated
source-lock reports remain ignored under `experiments/results/source-lock-snapshots/stage4k/`;
fetched public-source bytes remain ignored under `third_party/SourceSnapshots/`.

Stage 4L observation-promotion records require `execution_enabled=false`, `solve_claim=false`,
explicit promotion categories, review-decision references, blockers for blocked/deferred/quarantined
and rejected states, and disabled manifest-readiness records. Generated reports remain ignored under
`experiments/results/observation-promotion/stage4l/`.

Stage 4M image-preflight records require `raw_image_committed=false`,
`generated_image_committed=false`, `solve_claim=false`, `trusted_as_canonical=false`,
`usable_as_experiment_seed=false`, `image_interpretation_claim=false`, metric-only compression
records, explicit source-variant statuses, and blocked bigram/Fibonacci-421 readiness unless a
future stage provides reproducible matrix regeneration and controls. Generated JSONL reports remain
ignored under `experiments/results/image-preflight/stage4m/`; raw page images and
`data/raw/images/Fib421.jpg` remain ignored.

Stage 4N stego/audio positive-control readiness records require `raw_file_committed=false`,
`binary_committed=false`, `image_committed=false`, `audio_committed=false`, `font_committed=false`,
`archive_committed=false`, `extracted_payload_committed=false`, `solve_claim=false`,
`execution_performed=false`, and `tool_executed=false`. Historical real positive-control readiness
requires exact expected-output metadata; synthetic controls must be labelled synthetic. Generated
reports remain ignored under `experiments/results/stego-positive-controls/stage4n/`; fixture cache
bytes remain ignored under `third_party/StegoPositiveControls/`.

Stage 4O CPU batch adapter expansion records require `cpu_only=true`, `cuda_used=false`,
`cuda_required=false`, `no_solve_claim=true`, `canonical_corpus_active=false`,
`page_boundaries_final=false`, and `generated_outputs_committed=false`. Adapter coverage records use
`supported`, `missing`, `deferred`, or `unsupported_by_design`; parity expectation records require
output hashes when parity passes. Generated result, coverage, parity, scoring, and summary reports
remain ignored under `experiments/results/cpu-batch/stage4o/`; only the aggregate Stage 4O summary
is committed under `data/research/`.

Stage 4P result-store and score-summary unification records require `cuda_used=false`,
`cuda_required=false`, `no_solve_claim=true`, `solve_claim=false`,
`canonical_corpus_active=false`, `page_boundaries_final=false`,
`generated_outputs_committed=false`, `raw_data_processed=false`,
`new_experiment_executed=false`, and `new_scorer_added=false`. Score interpretation remains
`triage_only`, confidence labels use the Stage 4I vocabulary plus explicit unavailable states, and
missing optional generated outputs are inventory warnings. Generated unified records remain ignored
under `experiments/results/result-store-unification/stage4p/`; only the aggregate Stage 4P summary
is committed under `data/research/`.

Stage 5B CUDA parity harness records require `cuda_kernel_added=false`,
`cuda_source_modified=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `solve_claim=false`, `no_solve_claim=true`,
`generated_outputs_committed=false`, `codex_output_committed=false`, and
`website_expansion=false`. Backend capability records must keep `cuda_hardware_required=false`
and `local_16gb_profile_required=false`; local 16GB GPU metadata is optional planning metadata
only. Generated harness reports remain ignored under `experiments/results/cuda-parity/stage5b/`;
only compact YAML records under `data/cuda/` are committed.

Committed Stage 5B schema IDs:

- `cuda-parity-harness-record-v0`
- `cuda-parity-fixture-record-v0`
- `cuda-backend-capability-record-v0`
- `cuda-future-kernel-parity-matrix-v0`
- `stage5b-cuda-parity-harness-summary-v0`

Stage 5C CUDA build/device records require `cuda_build_device_detection_only=true`,
`cuda_required=false`, `gpu_required=false`, `local_16gb_profile_required=false`,
`compatibility_8gb_profile_present=true`, `cuda_kernel_added=false`,
`cuda_source_modified=false`, `cryptanalytic_cuda_kernel_added=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`solve_claim=false`, `no_solve_claim=true`, `generated_outputs_committed=false`,
`codex_output_committed=false`, and `website_expansion=false`. Generated build/device reports
remain ignored under `experiments/results/cuda-build/stage5c/`; only compact YAML records under
`data/cuda/` are committed.

Committed Stage 5C schema IDs:

- `cuda-build-profile-record-v0`
- `cuda-toolchain-detection-record-v0`
- `cuda-device-detection-record-v0`
- `cuda-smoke-build-record-v0`
- `stage5c-cuda-build-device-summary-v0`

Stage 5D native CPU backend records require `native_cpu_only=true`, `cuda_used=false`,
`cuda_required=false`, `gpu_required=false`, `gpu_benchmark_performed=false`,
`cuda_kernel_added=false`, `cuda_source_modified=false`, `performance_claim=false`,
`speedup_claim=false`, `solve_claim=false`, `no_solve_claim=true`,
`generated_outputs_committed=false`, `codex_output_committed=false`, `website_expansion=false`,
`python_semantic_reference_preserved=true`, and `cxx_launches_python_workers=false`. Threading
records must preserve deterministic ordering, fixed output slots, and range partitioning. Generated
native CPU reports remain ignored under `experiments/results/native-cpu/stage5d/`; only compact YAML
records under `data/native-cpu/` are committed.

Committed Stage 5D schema IDs:

- `native-cpu-backend-capability-record-v0`
- `native-cpu-threading-record-v0`
- `native-cpu-parity-record-v0`
- `native-cpu-diagnostic-record-v0`
- `stage5d-native-cpu-summary-v0`

Stage 5E first CUDA kernel contract records require `cuda_kernel_contract_only=true`,
`cuda_kernel_added=false`, `cuda_source_modified=false`, `cryptanalytic_cuda_kernel_added=false`,
`cuda_transform_executed=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `broad_experiment_executed=false`, `raw_data_processed=false`,
`solve_claim=false`, `no_solve_claim=true`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `website_expansion=false`, `cuda_required=false`,
`gpu_required=false`, `local_16gb_profile_required=false`,
`python_semantic_reference_preserved=true`, and `cxx_launches_python_workers=false`. Generated
kernel-contract reports remain ignored under
`experiments/results/cuda-kernel-contract/stage5e/`; only compact YAML records under `data/cuda/`
are committed.

Committed Stage 5E schema IDs:

- `cuda-first-kernel-contract-record-v0`
- `cuda-adapter-selection-record-v0`
- `cuda-native-parity-adapter-record-v0`
- `cuda-implementation-readiness-record-v0`
- `stage5e-first-kernel-contract-summary-v0`

Stage 5F synthetic CUDA kernel records require `selected_kernel_id=shift_score_kernel`,
`selected_transform_family=caesar_mod29`, `selected_adapter_family=native_cpu_synthetic_shift_adapter`,
`synthetic_only=true`, `cuda_kernel_added=true`, `cuda_source_modified=true`,
`real_liber_primus_data_used=false`, `solved_fixture_cuda_used=false`,
`unsolved_page_cuda_used=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `broad_experiment_executed=false`, `raw_data_processed=false`,
`solve_claim=false`, `no_solve_claim=true`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `website_expansion=false`, `canonical_corpus_active=false`,
`page_boundaries_final=false`, `ci_gpu_required=false`, `no_gpu_ci_safe=true`,
`python_semantic_reference_preserved=true`, and `cxx_launches_python_workers=false`. Generated
kernel reports remain ignored under `experiments/results/cuda-kernel/stage5f/`; only compact YAML
records under `data/cuda/` are committed.

Committed Stage 5F schema IDs:

- `cuda-synthetic-kernel-implementation-record-v0`
- `cuda-kernel-build-record-v0`
- `cuda-synthetic-parity-run-record-v0`
- `stage5f-synthetic-cuda-kernel-summary-v0`

Stage 5G CUDA parity-reporting records require `selected_kernel_id=shift_score_kernel`,
`stage5f_cuda_native_hash_match=true`, `device_code_subset_compliant=true`,
`new_cuda_kernels_added=0`, `solved_fixture_cuda_execution_allowed=false`,
`production_gematria_mod29_cuda_ready=false`, `real_liber_primus_data_used=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`generated_outputs_committed=false`, `codex_output_committed=false`, and `solve_claim=false`.

Committed Stage 5G schema IDs:

- `cuda-shift-score-parity-report-record-v0`
- `cuda-device-code-subset-audit-record-v0`
- `cuda-solved-fixture-safe-preflight-record-v0`
- `stage5g-cuda-parity-reporting-summary-v0`

Stage 5H Gematria shift contract records require `selected_future_kernel_id=shift_score_kernel`,
`token_domain=integers_0_to_28`, `arithmetic_direction=forward_add_shift_mod29`,
`stage5h_cuda_execution_allowed=false`, `solved_fixture_cuda_execution_allowed=false`,
`production_gematria_mod29_cuda_ready=false`, `real_liber_primus_data_used=false`,
`solved_fixture_cuda_used=false`, `unsolved_page_cuda_used=false`, `new_cuda_kernels_added=0`,
`cuda_source_modified=false`, `gpu_benchmark_performed=false`, `performance_claim=false`,
`speedup_claim=false`, `generated_outputs_committed=false`, `codex_output_committed=false`, and
`solve_claim=false`. The Stage 5H native fixture hash must not equal the Stage 5F uppercase Latin
synthetic hash.

Committed Stage 5H schema IDs:

- `gematria-shift-score-contract-record-v0`
- `gematria-native-parity-fixture-record-v0`
- `gematria-solved-fixture-safe-mapping-record-v0`
- `gematria-score-summary-parity-plan-record-v0`
- `stage5h-gematria-shift-contract-summary-v0`

Stage 5I Gematria CUDA preparation records require `target_future_kernel_name=gematria_mod29_shift_score_kernel`,
`token_domain=integers_0_to_28`, `arithmetic_direction=forward_add_shift_mod29`,
`separator_policy=non_transformable_separators_preserved_unshifted`, `cuda_source_modified=false`,
`new_cuda_kernels_added=0`, `cuda_execution_performed=false`,
`solved_fixture_cuda_execution_allowed=false`, `production_gematria_mod29_cuda_ready=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`real_liber_primus_data_used=false`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`,
`no_solve_claim=true`, and `solve_claim=false`. Validation vectors use raw numeric token buffers,
transformable masks, and candidate-major output order; separator placeholders stay inert.

Committed Stage 5I schema IDs:

- `gematria-cuda-kernel-preparation-record-v0`
- `gematria-cuda-abi-plan-record-v0`
- `gematria-cuda-validation-vector-record-v0`
- `gematria-cuda-implementation-checklist-record-v0`
- `stage5i-gematria-cuda-preparation-summary-v0`

Stage 5J Gematria CUDA kernel records require `implemented_kernel_name=gematria_mod29_shift_score_kernel`,
`source_contract_id=gematria_mod29_shift_score_contract_v0`,
`token_domain=integers_0_to_28`, `arithmetic_direction=forward_add_shift_mod29`,
`separator_policy=non_transformable_separators_preserved_unshifted`, `synthetic_only=true`,
`new_cuda_kernels_added=1`, `solved_fixture_cuda_execution_allowed=false`,
`production_gematria_mod29_cuda_ready=false`, `real_liber_primus_data_used=false`,
`solved_fixture_cuda_used=false`, `unsolved_page_cuda_used=false`, `gpu_benchmark_performed=false`,
`performance_claim=false`, `speedup_claim=false`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`,
`no_solve_claim=true`, and `solve_claim=false`. A passed synthetic parity record must match the
Stage 5H native fixture hash `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`.

Committed Stage 5J schema IDs:

- `gematria-cuda-kernel-implementation-record-v0`
- `gematria-cuda-kernel-build-record-v0`
- `gematria-cuda-synthetic-parity-record-v0`
- `stage5j-gematria-cuda-kernel-summary-v0`

Stage 5K Gematria CUDA parity-reporting records require `implemented_kernel_name=gematria_mod29_shift_score_kernel`,
`source_contract_id=gematria_mod29_shift_score_contract_v0`,
`native_fixture_id=stage5h-gematria-mod29-synthetic-shift-fixture-v0`,
`stage5j_cuda_native_hash_match=true`, `synthetic_parity_verified=true`,
`device_code_subset_compliant=true`, `new_cuda_kernels_added=0`,
`cuda_source_modified=false`, `cuda_execution_performed=false`,
`solved_fixture_cuda_execution_allowed=false`, `production_gematria_mod29_cuda_ready=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`real_liber_primus_data_used=false`, `solved_fixture_cuda_used=false`,
`unsolved_page_cuda_used=false`, `generated_outputs_committed=false`,
`codex_output_committed=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`,
`no_solve_claim=true`, and `solve_claim=false`. A Stage 5K parity report must preserve the
Stage 5J CUDA output hash and Stage 5H native fixture hash as matching values, and solved-fixture
preflight records must remain blocked until token mapping, score-summary parity, and no-unsolved
guardrails are explicit.

Committed Stage 5K schema IDs:

- `gematria-cuda-parity-report-record-v0`
- `gematria-cuda-device-code-audit-record-v0`
- `gematria-solved-fixture-safe-preflight-record-v0`
- `gematria-cuda-score-summary-preflight-record-v0`
- `stage5k-gematria-cuda-parity-reporting-summary-v0`

Stage 5L solved-fixture token-mapping records require source-backed Gematria token values in
`0..28`, explicit token kinds, transformable masks, separator metadata, candidate-major output
ordering, `hash_algorithm=sha256_canonical_json_v1`, and Stage 4I-compatible score-summary labels.
They must keep `cuda_execution_performed=false`, `cuda_source_modified=false`,
`new_cuda_kernels_added=0`, `solved_fixture_cuda_execution_allowed=false`,
`generated_outputs_committed=false`, `codex_output_committed=false`, `no_solve_claim=true`, and
`solve_claim=false`.

Committed Stage 5L schema IDs:

- `gematria-solved-fixture-token-mapping-record-v0`
- `gematria-solved-fixture-native-parity-record-v0`
- `gematria-solved-fixture-output-hash-contract-v0`
- `gematria-solved-fixture-score-summary-shape-v0`
- `stage5l-solved-fixture-token-mapping-summary-v0`

Stage 5M solved-fixture CUDA records require `executed_kernel=gematria_mod29_shift_score_kernel`,
`executed_semantics=gematria_shift_score_only`, `solved_fixture_cuda_execution_allowed=true`,
`solved_fixture_cuda_execution_scope=exact_stage5l_mapped_token_buffers_only`,
`unsolved_page_cuda_used=false`, `real_liber_primus_cuda_data_used=false`,
`new_cuda_kernels_added=0`, `device_kernel_arithmetic_modified=false`,
`gpu_benchmark_performed=false`, `performance_claim=false`, `speedup_claim=false`,
`generated_outputs_committed=false`, `codex_output_committed=false`,
`canonical_corpus_active=false`, `page_boundaries_final=false`, `no_solve_claim=true`, and
`solve_claim=false`. Passed parity records require the CUDA output-token hash to match the Stage 5L
native output-token hash.

Committed Stage 5M schema IDs:

- `gematria-solved-fixture-cuda-run-record-v0`
- `gematria-solved-fixture-cuda-parity-record-v0`
- `gematria-solved-fixture-cuda-boundary-record-v0`
- `stage5m-solved-fixture-cuda-parity-summary-v0`

Stage 5N solved-fixture CUDA reporting records require `cuda_source_modified=false`,
`additional_cuda_execution_performed=false`, `new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`,
`real_liber_primus_cuda_data_used=false`, `gpu_benchmark_performed=false`, `speedup_claim=false`,
`generated_outputs_committed=false`, and `solve_claim=false`.

Committed Stage 5N schema IDs:

- `gematria-solved-fixture-cuda-report-record-v0`
- `gematria-cuda-controlled-expansion-gate-record-v0`
- `gematria-cuda-boundary-review-record-v0`
- `gematria-cuda-result-store-preflight-record-v0`
- `gematria-no-unsolved-guardrail-record-v0`
- `stage5n-solved-fixture-cuda-reporting-summary-v0`

Stage 5O solved-fixture CUDA repeat records require `cuda_source_modified=false`,
`new_cuda_kernels_added=0`, `unsolved_page_cuda_used=false`, `real_liber_primus_cuda_data_used=false`,
`gpu_benchmark_performed=false`, `speedup_claim=false`, `generated_outputs_committed=false`, and
`solve_claim=false`. Passed repeat parity records must match both the Stage 5L native output-token hash
and the Stage 5M CUDA output-token hash.

Committed Stage 5O schema IDs:

- `gematria-solved-fixture-cuda-repeat-run-record-v0`
- `gematria-solved-fixture-cuda-repeat-parity-record-v0`
- `gematria-cuda-result-store-preflight-v0`
- `gematria-cuda-score-summary-preflight-v0`
- `gematria-cuda-expansion-decision-record-v0`
- `stage5o-repeat-verification-result-store-summary-v0`

## Result record principles

Records must be replayable, reviewable, compact, and explicit about uncertainty.

## Common JSONL Fields

Generated and committed record families use fields such as result ID, experiment ID, manifest hash, corpus lock ID, transform chain, candidate summary, scores, null-control scores, rank, timestamps, review status, privacy flags, CUDA flags, canonical-corpus flags, page-boundary flags, and solve-claim flags.

Implemented legacy workbook record types:

- `legacy_workbook_sheet`
- `legacy_solved_delta`
- `legacy_prime_sum`
- `legacy_workbook_formula`
- `legacy_workbook_summary`
- `legacy_pastebin_line_pair`
- `legacy_pastebin_anchor`
- `legacy_pastebin_summary`
- `transcript_line`
- `scream314_reference_record`
- `pastebin_transcript_alignment`
- `lp2_page_boundary_candidate`
- `glyph_variant_observation`
- `stage0d_alignment_summary`

## SQLite Result Store

Stage 2B added a SQLite result-store foundation for generated local outputs. SQLite databases and sidecar files are generated outputs and must not be committed.

## Required provenance fields

Required provenance will include git commit, manifest path and hash, tool versions, corpus locks, Gematria profile, transcript profile, random seed, and command line.

## Score breakdown fields

Scores should include component names, raw values, normalized values, weights, null-control distributions, and threshold notes.

## Hardware metadata

Hardware metadata should include CPU, RAM, GPU, driver, CUDA toolkit, compiler, OS, and relevant build flags.

## Reproducibility metadata

Reproducibility metadata should include run ID, timestamps, environment summary, deterministic seed, output schema version, and source data hashes.

## False-positive warnings

Every candidate record must be treated as unverified until rerun, compared to controls, and manually reviewed.

Workbook-derived records must include `trusted_as_canonical=false` and must not be treated as source truth.

Pastebin-derived records must include `source_id`, `source_sha256`, `source_local_filename`, and `trusted_as_canonical=false`.

Alignment-derived records must include source IDs, source SHA-256 hashes, confidence labels, and `trusted_as_canonical=false`. Boundary candidates must include `canonical_page_boundary=false`.

Public tutorials must not present generated results as evidence unless they are manifest-backed, provenance-complete, and explicitly reviewed. Stage 0D-P examples are smoke outputs only.

## Stage 3O Discord Promotion Records

Stage 3O committed promotion records use redacted YAML summaries under `data/observations/discord/`.

Required fields include:

- `promoted_id`
- `source=discord_admin_export_stage3n`
- `source_record_type`
- `redacted=true`
- `review_status`
- `trusted_as_canonical=false`
- `raw_message_committed=false`
- `usernames_committed=false`

Generated full candidate lists and unsafe-link rejection lists remain ignored under `experiments/results/discord-promotion/stage3o/`. Wiki sync reports remain ignored under `experiments/results/wiki-sync/stage3o/`.

## Stage 3Q Discord Review Bundle Records

Stage 3Q adds schemas for generated redacted message records, generated topic shard records, generated review lead records, and the committed aggregate review-bundle summary.

Committed aggregate fields include:

- `bundle_id`
- `html_file_count`
- `redacted_message_count`
- `topic_shard_count`
- `review_lead_count`
- `public_link_count`
- `method_claim_count`
- `numeric_observation_count`
- `visual_observation_count`
- `debunk_count`
- false privacy flags for raw logs, raw messages, usernames, private URLs, AI upload, live API use, scraping, and solve claims

Generated redacted streams, topic shards, JSONL indexes, and local HTML review indexes remain ignored under `experiments/results/discord-review-bundles/stage3q/`.

## Stage 4A Discord Full Review Bundle Records

Stage 4A adds schemas for generated full-review channel records, redacted message records, shard
records, index records, bundle summaries, Discord image references, and LP page gallery records.

Committed schema IDs:

- `discord-full-review-channel-record-v0`
- `discord-full-review-message-record-v0`
- `discord-full-review-shard-record-v0`
- `discord-full-review-index-record-v0`
- `discord-full-review-summary-v0`

## Stage 4B Source-Lock And Visual Intake Records

Stage 4B adds schemas for source triage, source health, visual observation intake, negative-control records, and disabled future manifest records.

Committed schema IDs:

- `stage4b-source-triage-record-v0`
- `source-health-record-v0`
- `stage4b-visual-observation-record-v0`
- `negative-control-record-v1`
- `stage4b-disabled-experiment-manifest-v0`

Generated triage diagnostics remain ignored under `experiments/results/source-lock-triage/stage4b/`.
- `lp-page-gallery-record-v0`
- `discord-image-reference-v0`

## Stage 4C Visual Annotation Records

Stage 4C adds schemas for visual annotation tasks, region annotation templates, cuneiform reading candidates, dot-pattern ambiguity tasks, delimiter tasks, visual negative-control annotation tasks, and the annotation pack summary.

Committed schema IDs:

- `visual-annotation-task-v0`
- `visual-region-annotation-v0`
- `cuneiform-reading-candidate-v0`
- `dot-pattern-annotation-v0`
- `delimiter-annotation-v0`
- `visual-negative-control-annotation-v0`
- `visual-annotation-pack-summary-v0`

Committed records live under `data/observations/visual/`. Generated site files and templates remain ignored under `experiments/results/visual-annotation/stage4c/`.

## Stage 4D Bounded Numeric Verifier Records

Stage 4D adds generated schemas for bounded numeric manifests, bounded numeric result records, numeric negative-control result records, and delimiter handedness audit records.

Committed schema IDs:

- `bounded-numeric-manifest-v0`
- `bounded-numeric-result-record-v0`
- `numeric-negative-control-result-v0`
- `delimiter-handedness-audit-record-v0`

Generated result files remain ignored under `experiments/results/bounded-numeric/stage4d/`.

## Stage 4E Source Delta Audit Records

Stage 4E adds committed schemas for source-delta audit records, source-path candidate records, source-variant comparison backlog records, image-compression artefact observations, and disabled future image/stego provenance manifests.

Committed schema IDs:

- `source-delta-audit-record-v0`
- `source-path-candidate-record-v0`
- `source-variant-comparison-record-v0`
- `image-compression-artifact-observation-v0`
- `future-image-artifact-manifest-v0`

Committed records live under `data/observations/archive/`, `data/locks/third-party/`, `data/observations/visual/`, and `experiments/manifests/stage4e-disabled/`. They must keep `raw_file_committed=false`, `binary_committed=false`, `font_committed=false`, `trusted_as_canonical=false`, and `solve_claim=false`.

Generated path indexes, source-delta reports, duplicate/unique candidate JSONL files, and warnings remain ignored under `experiments/results/source-delta/stage4e/`. Raw cache contents under `third_party/CicadaSolversIddqd/` remain ignored except for README/.gitkeep.

## Stage 4F Stego Audio Fixture Source Records

Stage 4F adds committed schemas for historical OutGuess fixture source records, audio fixture source records, source-health records, historical stego fixture manifests, and toolchain requirement records.

Committed schema IDs:

- `stego-fixture-source-record-v0`
- `audio-fixture-source-record-v0`
- `fixture-source-health-record-v0`
- `historical-stego-fixture-manifest-v0`
- `toolchain-requirement-record-v0`

Committed records live under `data/observations/stego/` and `data/locks/third-party/`. Disabled future manifests live under `experiments/manifests/stego/stage4f-disabled/`.

Generated fixture candidate reports, source-gap JSONL files, and warnings remain ignored under `experiments/results/stego-fixtures/stage4f/`. Raw images, audio, binaries, fonts, archives, and extracted payloads remain uncommitted.

## Stage 4N Stego Audio Positive-Control Readiness Records

Stage 4N adds committed schemas for stego readiness, audio readiness, fixture-cache records,
expected-output records, toolchain readiness, and positive-control summaries.

Committed schema IDs:

- `stego-positive-control-readiness-v0`
- `audio-positive-control-readiness-v0`
- `stego-fixture-cache-record-v0`
- `stego-expected-output-record-v0`
- `stego-toolchain-readiness-v0`
- `stego-positive-control-summary-v0`

Generated readiness reports remain ignored under `experiments/results/stego-positive-controls/stage4n/`.
Local fixture cache bytes remain ignored under `third_party/StegoPositiveControls/`.

## Stage 4O CPU Batch Adapter Expansion Records

Stage 4O adds committed schemas for adapter coverage, parity expectations, solved-fixture streams,
scoring compatibility, and the aggregate adapter-expansion summary.

Committed schema IDs:

- `cpu-batch-adapter-coverage-v0`
- `cpu-batch-parity-expectation-v0`
- `cpu-batch-adapter-expansion-summary-v0`
- `cpu-batch-solved-fixture-stream-v0`
- `cpu-batch-scoring-compatibility-v0`

Generated Stage 4O result, coverage, parity, scoring, and summary records remain ignored under
`experiments/results/cpu-batch/stage4o/`. The committed aggregate summary lives under
`data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml`.

## Stage 4P Result Store Score Summary Unification Records

Stage 4P adds committed schemas for unified result records, unified score-summary records, source
inventory records, method-status joins, cross-stage reports, and aggregate unification summaries.

Committed schema IDs:

- `unified-result-record-v0`
- `unified-score-summary-record-v0`
- `result-source-inventory-v0`
- `result-method-status-join-v0`
- `cross-stage-comparison-report-v0`
- `result-store-unification-summary-v0`

Generated Stage 4P source inventory, unified result JSONL, unified score-summary JSONL,
method-status join, cross-stage report, summary JSON, warnings, and any SQLite probes remain ignored
under `experiments/results/result-store-unification/stage4p/`. The committed aggregate summary lives
under `data/research/stage4p-result-store-score-summary-unification-summary.yaml`.

## Stage 4G Cookie Refresh Records

Stage 4G adds committed schemas for the cookie refresh manifest view, generated candidate records, and committed aggregate summary:

- `schemas/web/cookie-refresh-manifest-v0.schema.json`
- `schemas/web/cookie-refresh-candidate-record-v0.schema.json`
- `schemas/web/cookie-refresh-summary-v0.schema.json`

Candidate records log the experiment ID, source record, source basis, byte variant, UTF-8 candidate byte hash, digest, target cookie, exact-match flag, previous-pack duplicate flag, and all no-broadening policy flags. Generated records are not committed.

## Stage 4H CPU Batch Records

Stage 4H adds committed schemas for the CPU batch manifest, input stream, transform candidate, generated result record, run summary, and CPU/CUDA parity contract:

- `schemas/experiments/cpu-batch-manifest-v0.schema.json`
- `schemas/experiments/cpu-batch-input-stream-v0.schema.json`
- `schemas/experiments/cpu-batch-transform-candidate-v0.schema.json`
- `schemas/experiments/cpu-batch-result-record-v0.schema.json`
- `schemas/experiments/cpu-batch-run-summary-v0.schema.json`
- `schemas/experiments/cpu-cuda-parity-contract-v0.schema.json`

Result records log transform IDs, parameters, token counts, execution status, output hashes, optional structured score summaries, and all no-CUDA/no-solve policy flags. Generated CPU batch records are not committed.

Committed aggregate summaries live under:

- `data/observations/discord/stage4a-full-review-aggregate.yaml`
- `data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml`

Aggregate records contain only counts, generated output paths, source directory references, and
privacy flags. They must not contain raw messages, usernames, user IDs, message IDs, private URLs,
raw Discord HTML, generated site content, or copied LP page image bytes.

Generated redacted streams, channel shards, topic shards, indexes, static site files, copied LP page
images, thumbnails, contact sheets, and upload archives remain ignored under
`experiments/results/discord-full-review/stage4a/`.

## Stage 3R Discord Lead Promotion And Post-Discord Manifest Records

Stage 3R adds committed schemas for:

- `promoted_discord_source_record`
- `promoted_discord_observation_record`
- `negative_control_record`
- `post_discord_experiment_manifest`
- `gp_rune_claim_record`

Promoted source and observation records require false privacy flags for raw messages, usernames, and private URLs. Observation records keep `usable_as_experiment_seed=false` and `trusted_as_canonical=false`.

Negative-control records preserve known false-positive classes and require `solve_claim=false`.

Post-Discord manifests require `execution_enabled=false`, `cpu_only=true`, `cuda_enabled=false`, `cloud_execution=false`, `paid_services=false`, `generated_outputs_committed=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

Generated promotion-audit records remain ignored under `experiments/results/discord-lead-promotion/stage3r/`.

## Stage 3S Onion 7 Candidate Records

Stage 3S generated records are written only to ignored outputs under `experiments/results/post-discord/stage3s/`.

Candidate records include:

- `experiment_id=EXP-3R-003`
- `manifest_id`
- `value_space`
- `route`
- `direction`
- `reset_mode`
- `numeric_sequence`
- `numeric_sequence_mod29`
- `sequence_signature_sha256`
- `candidate_index`
- `input_slice_id`
- `transform_family=onion7_numeric_seed_pack`
- `transform_id=onion7_mod29_stream_subtract`
- score summary and calibrated confidence label
- `cuda_used=false`
- `no_solve_claim=true`
- `canonical_corpus_active=false`
- `page_boundaries_final=false`
- `trusted_as_canonical=false`

Generated `candidate_records.jsonl`, `top_candidates.jsonl`, `summary.json`, and warning/score files must not be committed. Research logs may summarize counts, top parameters, top score, and confidence only.

## Stage 3T GP/Rune Verification Records

Stage 3T generated records are written only to ignored outputs under `experiments/results/post-discord/stage3t/`.

Verification records include:

- `experiment_id=EXP-3R-004`
- `claim_id`
- `source_basis`
- `claim_type`
- `target_span`
- `claimed_value`
- `computed`
- `verification_status`
- `raw_message_committed=false`
- `username_committed=false`
- `private_url_committed=false`
- `cuda_used=false`
- `no_solve_claim=true`
- `canonical_corpus_active=false`
- `page_boundaries_final=false`
- `trusted_as_canonical=false`

Generated `gp_rune_claim_verification_records.jsonl`, per-status JSONL files, `summary.json`, and warnings must not be committed. Research logs may summarize status counts and representative claim IDs only.

## Stage 3U Cookie Signed-Variant Records

Stage 3U generated records are written only to ignored outputs under `experiments/results/post-discord/stage3u/`.

Candidate records include:

- `experiment_id=EXP-3R-001`
- `pack_id`
- `manifest_id`
- `candidate_id`
- `base_string_id`
- `base_string`
- `source_basis`
- `byte_variant`
- `encoding`
- `candidate_bytes_sha256`
- `digest_algorithm=sha256`
- `digest_hex`
- `target_cookie_id`
- `target_cookie_name`
- `exact_match`
- `solve_claim=false`
- `cuda_used=false`
- `cloud_execution=false`
- `trusted_as_canonical=false`

Generated `hash_candidate_records.jsonl`, `exact_matches.jsonl`, `summary.json`, and warnings must not be committed. Research logs may summarize counts and exact-match IDs only.

## Stage 3V OutGuess Regression Records

Stage 3V generated records are written only to ignored outputs under `experiments/results/stego/outguess/stage3v/`.

Committed schemas:

- `stego-artifact-record-v0`
- `outguess-regression-manifest-v0`
- `outguess-tool-record-v0`
- `outguess-extraction-record-v0`
- `outguess-regression-summary-v0`

Extraction records include tool availability, asset availability, attempt status, exit code, extracted payload hash and size, expected payload hash, payload-match flag, status, output paths, `raw_payload_committed=false`, `solve_claim=false`, and `cuda_used=false`.

Generated extraction JSONL, tool JSON, summary JSON, warnings, synthetic inputs, and extracted payloads must not be committed.

## Post-Discord Manifest Schemas

Committed post-Discord queue metadata uses `post-discord-experiment-manifest-v0` for disabled/explicit experiment manifests and `gp-rune-claim-record-v0` for exact GP/rune verifier claim records. These schemas keep execution disabled until a later bounded stage explicitly runs one manifest and require no-solve policy fields.

## Stage 0D-followup Record Types

Implemented/generated Stage 0D-followup record types include:

- `transcript_view_record`
- `alignment_gap_diagnostic`
- `page_boundary_confidence_audit`
- `stage0d_followup_alignment_summary`

These are diagnostic records only. They must include source hashes, confidence or reason labels where applicable, and non-canonical flags. Generated JSON/JSONL outputs under `data/normalized/alignment/` remain ignored.

## Stage 0E Corpus Schemas

Stage 0E adds schemas under `schemas/corpus/` for:

- `gematria-profile-v0`
- `glyph-variant-profile-v0`
- `separator-grammar-v0`
- `corpus_candidate_manifest`
- `corpus_token`
- `corpus_line`
- `corpus_page_candidate`
- `corpus_generation_warning`

Generated manifest and page records require `canonical_corpus_active=false`, `page_boundaries_final=false`, `canonical_page_boundary=false`, and `trusted_as_canonical=false` where applicable.

## Stage 1A Solved Fixture Schemas

Stage 1A adds schemas under `schemas/corpus/` for:

- `solved-page-fixture-v0` (`solved_page_fixture`)
- `solved_page_reproduction_record`
- `solved_page_reproduction_summary`

Fixture and reproduction records require provenance hashes and keep `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.
## Stage 1B Solved-Fixture Results

Stage 1B extends solved-page reproduction records with:

- `decoded_index_formula`
- `transform_parameters`
- `method_family=reverse_gematria`
- `method_family=rotated_reverse_gematria`

All reproduction records must keep `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`. Atbash-family generated outputs are stored under ignored solved-baseline directories and must not be committed.
## Stage 1C Reference And Vigenere Records

Stage 1C adds generated reference summary records:

- `reference_method_note`
- `tooling_reference_note`
- `stage1c_reference_source_summary`

Stage 1C also extends `solved_page_reproduction_record` with Vigenere-specific fields:

- `key_text`
- `key_indices`
- `skip_rule_applied_count`

All reproduction records continue to require `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Stage 1D Prime-Stream And Payload Records

Stage 1D extends `solved_page_fixture` records with optional `payload_checks` for fixture-declared payloads.

Stage 1D extends `solved_page_reproduction_record` with:

- `prime_values_used_count`
- `stream_values_used_count`
- `first_prime_values`
- `first_stream_values_mod29`
- `payload_check_results`

All reproduction records continue to require `trusted_as_canonical=false`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Stage 2A Registry And Manifest-Run Records

Stage 2A adds `solved-baseline-run-manifest-v0` for manifest-addressable solved-baseline regression runs.

Solved-fixture reproduction records now include registry metadata:

- `registry_id`
- `registry_sha256`
- `transform_id`
- `canonical_transform_id`
- `search_performed=false`
- `cuda_used=false`
- `scoring_used=false`

Manifest-run outputs include `solved_baseline_manifest_run_record` JSONL and `solved_baseline_manifest_run_summary` JSON. They must keep `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`, and generated files under `experiments/results/solved-baselines/` remain ignored.

## Stage 2B Experiment Result Store Schemas

Stage 2B adds result schemas under `schemas/results/`:

- `experiment-run-record-v0`
- `experiment-run-summary-v0`
- `experiment-event-record-v0`
- `experiment-artifact-record-v0`
- `experiment-result-store-manifest-v0`
- `sqlite-result-store-v0`

Solved-baseline imports require `canonical_corpus_active=false`, `page_boundaries_final=false`, `search_performed=false`, `scoring_used=false`, `cuda_used=false`, and `trusted_as_canonical=false`.

Generated result-store outputs include JSONL records and `results.sqlite3` under `experiments/results/result-store/`. They are ignored and must not be committed.

## Stage 2D Consistency Summary

Stage 2D may generate `consistency_check_suite_result` JSON summaries under `experiments/results/consistency/`. These summaries are generated outputs and are ignored by Git.

## Stage 2E Exploratory Dry-Run Schemas

Stage 2E adds committed schemas under `schemas/experiments/`:

- `exploratory-experiment-manifest-v0`
- `exploratory-dry-run-plan-v0`
- `exploratory-transform-space-v0`
- `exploratory-safety-gate-v0`
- `exploratory-corpus-slice-v0`

Generated `exploratory_dry_run_plan` records are ignored planning outputs under `experiments/results/exploratory-dry-runs/`. They are not candidate result rows and do not contain candidate plaintexts.

## Stage 2F CPU Execution Schemas

Stage 2F adds committed schemas under `schemas/experiments/`:

- `cpu-execution-manifest-v0`
- `cpu-execution-plan-v0`
- `cpu-execution-result-v0`
- `synthetic-corpus-record-v0`
- `execution-safety-gate-v0`

Generated `cpu_execution_plan`, `cpu_execution_result`, and execution summary records are ignored outputs under `experiments/results/cpu-execution/`. They are limited to synthetic and solved-fixture-only execution and require false search, candidate-generation, scoring, CUDA, canonical corpus, page-boundary, and canonical trust flags.

## Stage 2G Proposal And Approval Schemas

Stage 2G adds committed schemas under `schemas/experiments/`:

- `experiment-proposal-v0`
- `experiment-review-packet-v0`
- `experiment-approval-record-v0`
- `experiment-review-checklist-v0`

Generated `experiment_review_packet` records are ignored outputs under `experiments/results/proposal-reviews/`. Approval examples committed in Stage 2G are pending or denied only; no approved approval records are committed.

## Stage 2H Approval-Gated Execution Schemas

Stage 2H adds committed schemas under `schemas/experiments/`:

- `approval-gated-execution-request-v0.schema.json`
- `approval-gated-execution-plan-v0.schema.json`
- `approval-gated-execution-result-v0.schema.json`

Approval-gated execution records bind a proposal, a scope-bound approval record, and an output directory. Stage 2H permits approved execution only for synthetic and solved-control requests. Generated approval execution records are ignored under `experiments/results/approval-gated-execution/`; no approved unsolved-page approval records are committed.

## Stage 2I Approval-Readiness Packet Schema

Stage 2I adds `approval-readiness-packet-v0` under `schemas/experiments/`.

Generated `approval_readiness_packet` records summarize a real exploratory proposal, pending approval status, candidate-count bounds, risk summary, blocking conditions, and the exact human decision still required. They require false approval/execution/search/candidate-generation/scoring/CUDA/canonical flags. These packets are ignored outputs under `experiments/results/approval-readiness/` and are not approvals, execution records, candidate outputs, or solve evidence.

## Stage 2J Bounded Auto-Run Schemas

Stage 2J adds:

- `operator-policy-v0.schema.json`
- `bounded-experiment-queue-v0.schema.json`
- `bounded-experiment-item-v0.schema.json`
- `policy-check-result-v0.schema.json`
- `bounded-auto-run-result-v0.schema.json`

The operator policy records standing limits for local CPU experiments. Queue records list bounded items, policy-check records explain pass/fail/warning outcomes, and generated `bounded_auto_run_result` records summarize execution, deferral, or blocking outcomes.

Generated bounded auto-run records are ignored under `experiments/results/bounded-auto-runs/`. Stage 3A permits `search_performed=true` and `scoring_used=true` only for policy-passing bounded local CPU candidate enumeration summaries. They must keep `cuda_used=false`, `solve_claim_made=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Stage 3A Bounded Candidate And Minimal Scoring Schemas

Stage 3A adds:

- `bounded-candidate-record-v0`
- `bounded-experiment-run-summary-v0`
- `minimal-triage-score-v0`

Generated `bounded_candidate_record` rows are ignored output under `experiments/results/bounded-auto-runs/stage3a/`. They include transform family, transform parameters, candidate index, input slice ID, normalized output text, output hash, minimal score summary, ranking features, and explicit safety flags.

Minimal triage score records are deterministic local CPU scoring summaries. They are sorting metadata only and are not solve evidence.

## Stage 3B Refined Triage And Inspection Outputs

Stage 3B extends `minimal-triage-score-v0` with length-normalized score fields, separator-aware word counts, vowel-band checks, repeated-symbol penalties, tiny impossible-bigram penalties, feature explanations, confidence labels, and `no_solve_claim=true`.

Candidate-inspection and rerank outputs are generated records under `experiments/results/bounded-auto-runs/stage3b/`. They may include reranked top-k JSONL and summary JSON, but those files remain ignored outputs and must not be committed. Committed research logs may include top score metadata and transform parameters only, not full candidate text dumps.

## Stage 3C Scoring Calibration Schemas

Stage 3C adds:

- `scoring-control-record-v0`
- `scoring-calibration-summary-v0`
- `crib-check-result-v0`

Generated calibration records are ignored under `experiments/results/scoring-calibration/stage3c/`. They record positive, null, negative, and candidate score summaries, tiny crib hits, calibrated labels, score ranges, thresholds, and explicit `solve_claim=false` / `cuda_used=false` flags.

## Stage 3D Bounded Vigenere Candidate Records

Stage 3D reuses `bounded-candidate-record-v0` and `bounded-experiment-run-summary-v0` for the small explicit-key Vigenere preview. Candidate records add Stage 3D fields through schema `additionalProperties`:

- `key_text`
- `key_indices`
- `calibrated_confidence_label`
- `crib_hits`
- `crib_hit_count`
- `calibration_position`

Generated records remain ignored under `experiments/results/bounded-auto-runs/stage3d/`. They must keep `cuda_used=false`, `solve_claim=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Stage 3E Method Backlog And Dry-Run Records

Stage 3E adds committed experiment schemas:

- `method-backlog-v0`
- `method-backlog-item-v0`
- `stage3e-queue-item-v0`

The method backlog records evidence basis, exact parameters, candidate-count estimates, implementation status, required controls, and generated-output policy for bounded future methods. Stage 3E queue items require `cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

Generated `stage3e_queue_dry_run_summary` records are ignored under `experiments/results/bounded-auto-runs/stage3e/`. They record declared and calculated candidate counts, policy status, executor-support status, deferred reasons, and `executed_count=0` for this ingestion stage. They are not candidate outputs or solve evidence.

## Stage 3F Vigenere Key-Pack Records

Stage 3F reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the LP evidence-key Vigenere pack. Candidate records include:

- `transform_family=vigenere_key_pack`
- `transform_id=vigenere_explicit_key`
- `key_text`
- `key_indices`
- `transform_parameters.reset_mode`
- `transform_parameters.advance_mode`
- calibrated score fields and crib hits
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3F summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `key_count`, `reset_modes`, `advance_modes`, and `confidence_distribution`.

Generated Stage 3F files remain ignored under `experiments/results/bounded-auto-runs/stage3f/`. They are candidate leads only and not solve evidence.

## Stage 3G Prime Offset Sweep Records

Stage 3G reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the p56-local prime-minus-one offset sweep. Candidate records include:

- `transform_family=prime_stream_offset_sweep`
- `transform_id=prime_minus_one_stream`
- `transform_parameters.offset`
- `transform_parameters.direction`
- `transform_parameters.reset_mode`
- `transform_parameters.prime_index_policy`
- calibrated score fields and crib hits
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3G summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `prime_candidate_count`, `reset_modes`, and `confidence_distribution`.

Generated Stage 3G files remain ignored under `experiments/results/bounded-auto-runs/stage3g/`. They are candidate leads only and not solve evidence. Stage 3G also adds a future Mersenne/perfect-number queue item, which Stage 3J later promotes to runnable through a bounded executor.

## Stage 3H Reset/Advance Ablation Records

Stage 3H reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for reset/advance ablation. Candidate records include:

- `base_transform_id`
- `base_transform_family`
- `reset_mode`
- `advance_mode`
- `transformable_token_count`
- `metadata_support_status`
- calibrated scoring fields and crib-hit fields

The generated Stage 3H summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `reset_advance_candidate_count`, `negative_control_count`, `metadata_support_status`, and `confidence_distribution`.

Family-specific negative controls are generated as ignored JSONL records in `negative_control_records.jsonl`. They are false-positive controls only, not candidate solve evidence.

## Stage 3I Historical Vigenere Key-Pack Records

Stage 3I reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the historical motif Vigenere key pack. Candidate records include:

- `transform_family=vigenere_key_pack`
- `transform_id=vigenere_explicit_key`
- `key_text`
- `key_indices`
- `evidence_family=historical_motif_key_pack`
- `transform_parameters.reset_mode`
- `transform_parameters.advance_mode`
- `transform_parameters.evidence_family`
- calibrated scoring fields and crib-hit fields
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3I summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `key_count`, `reset_modes`, `advance_modes`, and `confidence_distribution`.

Generated Stage 3I files remain ignored under `experiments/results/bounded-auto-runs/stage3i/`. They are candidate leads only and not solve evidence.

## Stage 3J Mersenne Probe Records

Stage 3J reuses `bounded_candidate_record` and `bounded_experiment_run_summary` for the finite-sequence Mersenne/perfect-number probe. Candidate records include:

- `transform_family=mersenne_prime_stream`
- `transform_id=mersenne_prime_stream_tiny`
- `stream_variant`
- `exponent_sequence_id`
- `exponent_sequence`
- `offset`
- `direction`
- `reset_mode`
- `stream_signature_sha256`
- calibrated scoring fields and crib-hit fields
- `cuda_used=false`
- `solve_claim=false`

The generated Stage 3J summary includes `expected_candidate_count`, `executed_candidate_count`, `deferred_candidate_count`, `mersenne_candidate_count`, `stream_variants`, `directions`, `reset_modes`, `unique_stream_signature_count`, `duplicate_stream_signature_count`, and `confidence_distribution`.

Duplicate stream signatures are expected because the declared eight-exponent sequence is cyclic. They must be reported, not silently deduplicated.

Generated Stage 3J files remain ignored under `experiments/results/bounded-auto-runs/stage3j/`. They are candidate leads only and not solve evidence.

## Stage 3K Archive And Visual Registry Records

Stage 3K adds committed schemas under `schemas/history/` and `schemas/visual/` for:

- `source_archive_record`
- `source_lock_record`
- `cookie_hash_record`
- `image_artifact_record`
- `visual_numeric_observation`
- `visual_observation_reading`
- `image_analysis_summary`

Committed record files live under `data/observations/` and `data/locks/third-party/liber-primus-pages/`. Generated scan summaries remain ignored under `experiments/results/archive-visual-registry/stage3k/`.

All Stage 3K records keep `trusted_as_canonical=false`; visual observations keep `usable_as_experiment_seed=false`; cookie/hash records do not claim preimages.

## Stage 3L Hash Preimage Records

Stage 3L adds committed schemas under `schemas/web/` for:

- `hash_preimage_candidate_pack`
- `hash_preimage_candidate_record`
- `hash_preimage_match_record`
- `hash_preimage_run_summary`

Candidate records log the exact literal text before UTF-8 encoding, byte variant, byte-string SHA-256, target cookie, digest, and exact-match status.

Generated records remain ignored under `experiments/results/hash-preimage/stage3l/`. They are bounded preimage-test records only and not solve evidence.

## Stage 3M Image Analysis Records

Stage 3M adds committed schemas under `schemas/visual/` for:

- `image_analysis_record`
- `image_threshold_summary`
- `image_symmetry_record`
- `image_bitplane_summary`
- `image_component_summary`
- `visual_feature_candidate`
- `image_analysis_run_summary`

Generated records remain ignored under `experiments/results/image-analysis/stage3m/`.

All Stage 3M records keep `trusted_as_canonical=false` and `solve_claim=false`. Visual feature candidate records also keep `usable_as_experiment_seed=false`; they are human-review aids only and not image-derived seed manifests.

## Stage 3N Discord Ingestion Records

Stage 3N adds committed schemas under `schemas/history/` for:

- `discord_archive_record`
- `discord_html_file_lock`
- `discord_extracted_link`
- `discord_attachment_candidate`
- `discord_method_claim_candidate`
- `discord_numeric_observation_candidate`
- `discord_ingestion_summary`

Generated link, attachment, method-claim, numeric-observation, local-review, and per-file lock
records remain ignored under `experiments/results/discord-ingestion/stage3n/`.

Committed aggregate records under `data/locks/third-party/discord-chats/` and
`data/observations/discord/` contain aggregate counts and false privacy flags only. Raw logs,
message bodies, usernames, AI upload, live API use, and scraping are prohibited by schema and
validation.

## Stage 3P Image Transform Records

Stage 3P adds committed schemas under `schemas/visual/` for:

- `image_transform_record`
- `image_transform_metric_record`
- `visual_transform_candidate`
- `contact_sheet_record`
- `image_transform_run_summary`

Generated records remain ignored under `experiments/results/image-transforms/stage3p/`.

All Stage 3P records keep `trusted_as_canonical=false` and `solve_claim=false`. Transform and candidate records also keep `usable_as_experiment_seed=false`; they are human-review artefacts only and not image-derived seed manifests.

The consistency checks cross-reference committed schemas, manifests, registry metadata, documentation status, ignored-output policy, and result-store records when generated outputs are present.

## Stage 4I Scoring Consolidation Records

Stage 4I adds committed schemas under `schemas/scoring/` for:

- `scorer-record-v0`
- `scoring-calibration-profile-v0`
- `score-summary-record-v0`
- `confidence-label-record-v0`
- `scorer-compatibility-map-v0`
- `scoring-calibration-report-v0`

Committed records live under `data/scoring/`. Generated scorer inventories and report renderings remain ignored under `experiments/results/scoring-consolidation/stage4i/`.

All Stage 4I records keep scoring as triage metadata only. Score summary records require `solve_claim=false`, `trusted_as_canonical=false`, and `cuda_used=false`.
# Stage 4Q Benchmark Schemas

Stage 4Q adds benchmark planning schemas:

- `cpu-benchmark-plan-v0`
- `cpu-benchmark-smoke-record-v0`
- `benchmark-environment-record-v0`
- `cuda-parity-benchmark-readiness-v0`
- `stage4q-benchmark-parity-summary-v0`

These schemas require `cuda_used=false`, `cuda_required=false`, `gpu_benchmark_performed=false`, `cuda_implementation_added=false`, `solve_claim=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, `raw_data_processed=false`, `broad_experiment_executed=false`, and `generated_outputs_committed=false`.

# Stage 5A CUDA Planning Schemas

Stage 5A adds CUDA planning schemas:

- `cuda-target-plan-record-v0`
- `cuda-parity-scaffold-record-v0`
- `cuda-implementation-gate-record-v0`
- `cuda-non-target-record-v0`
- `cuda-planning-summary-v0`

These records require planning-only/no-solve flags and reject CUDA implementation, GPU benchmark, speedup claim, raw-data, generated-output, canonical-corpus, and page-boundary drift.

# Stage 5AA Prime-Minus-One CUDA Synthetic Schemas

Stage 5AA adds prime-minus-one CUDA synthetic schemas:

- `prime-minus-one-cuda-synthetic-kernel-implementation-record-v0`
- `prime-minus-one-cuda-synthetic-run-record-v0`
- `prime-minus-one-cuda-synthetic-parity-record-v0`
- `prime-minus-one-cuda-device-subset-audit-record-v0`
- `prime-minus-one-cuda-synthetic-result-store-preflight-record-v0`
- `prime-minus-one-cuda-synthetic-p56-blocker-record-v0`
- `prime-minus-one-cuda-synthetic-scored-experiment-deferral-record-v0`
- `prime-minus-one-cuda-synthetic-next-stage-decision-record-v0`
- `stage5aa-prime-minus-one-cuda-synthetic-summary-v0`

All Stage 5AA schemas require synthetic-only scope, no solve claim, no generated-output publication, no raw-data processing, no p56/full-p56 execution, no unsolved-page CUDA, no benchmark, and no scored experiment execution.

# Stage 5Z Prime-Minus-One CUDA Contract Schemas

Stage 5Z adds prime-minus-one CUDA contract schemas:

- `prime-minus-one-cuda-contract-record-v0`
- `prime-minus-one-cuda-kernel-abi-record-v0`
- `prime-minus-one-cuda-host-runner-contract-record-v0`
- `prime-minus-one-cuda-buffer-contract-record-v0`
- `prime-minus-one-cuda-validation-vector-record-v0`
- `prime-minus-one-cuda-future-parity-plan-record-v0`
- `prime-minus-one-cuda-result-store-compatibility-record-v0`
- `prime-minus-one-cuda-full-p56-blocker-record-v0`
- `prime-minus-one-scored-experiment-deferral-record-v0`
- `prime-minus-one-cuda-implementation-readiness-gate-record-v0`
- `prime-minus-one-cuda-next-stage-decision-record-v0`
- `stage5z-prime-minus-one-cuda-contract-summary-v0`

These records require contract-only/no-solve flags and reject native execution, CUDA execution, CUDA source modification, new CUDA kernels, GPU benchmarks, speedup claims, raw-data processing, generated-output publication, codex-output publication, canonical-corpus activation, and page-boundary finalisation.

Stage 5BU adds compact lineage-path repair and validation records only. It does not publish generated result bodies, byte streams, decoded bytes, score summaries, SQLite databases, or local reports.

Stage 5BW adds compact inactive-sidecar proposal, manifest-supersession preflight, active-lineage preservation, no-active-ingestion, no-byte-stream, and guardrail records only. It does not publish generated result bodies, byte streams, decoded bytes, score summaries, SQLite databases, local reports, or active String 4 inputs.

Stage 5BY adds compact inactive planning-manifest scaffold, no-execution planning-ingestion sidecar, source-digest duplicate-review, filename-equivalence, Stage 5BD preservation, no-active-ingestion, no-byte-stream, and guardrail records only. It does not publish generated result bodies, byte streams, decoded bytes, score summaries, SQLite databases, local reports, or active String 4 inputs.
