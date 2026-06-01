# Testing

Stage 5CO extends coverage with real approval-record readiness-package schemas, Stage 5CN warning integration, future operator approval/Deep Research acceptance/combined-gate/activation-decision readiness preflight checks, missing-requirements and transition-sequence validation, Stage 5CM boundary preservation, Stage 5CK/5CI/5CG/5CE/5CC/5BD preservation checks, no-active/no-byte/no-execution gate checks, credential-redaction/no-secret policy preservation, review-packaging-warning checks, CLI validation paths, 8-worker parallel-validation evidence, and ignored-output checks for `experiments/results/token-block/stage5co/` and `codex-output/**`.

## Test policy

Tests protect reproducibility and prevent false-positive drift.

## Unit tests

Unit tests cover deterministic parsing, schema validation, manifest safety, bounded executor behavior, fake-tool wrappers, scoring helpers, and consistency policies.

## Integration tests

Integration tests cover raw-data-free CLI paths, manifest validation, synthetic execution paths, generated-output ignore rules, and local CI reproduction scripts.

## Golden tests

Golden solved-baseline tests reproduce the committed known solved fixtures through the CPU transform registry and manifest path. They are regression evidence, not new solve claims.

Stage 0B adds conditional real-workbook tests that run only when the ignored legacy workbook is locally present.

## Property tests

Property tests will later check transform invariants, inverse behavior, and edge cases.

Synthetic workbook parser tests cover inventory, solved-delta extraction, modulo validation, Prime Sums booleans, formula inventory, deterministic output, and CLI behavior.

## Fuzz tests

Fuzz tests will later target parsers, manifest loading, corpus normalization, and transform composition.

## CPU/GPU parity tests

Every CUDA kernel must match a CPU reference implementation across representative inputs and edge cases.

## Manifest determinism tests

Manifests must replay to the same outputs under pinned inputs and fixed seeds.

## Documentation consistency tests

Documentation and anti-drift checks verify core policy statements such as raw-data immutability, generated-output ignore rules, current completed stage, canonical corpus inactive status, page-boundary review status, CUDA deferral, Discord privacy, and no-solve-claim policy.

Stage 5AB extends this coverage with dynamic stage-id parsing, operational Markdown staleness scanning, source-of-truth records, website-deferral checks, stale `Existing CUDA code` cap checks, `libreprimus consistency check-doc-staleness`, CI consistency integration, and ignored-output checks for `experiments/results/doc-staleness/stage5ab/` plus `codex-output/**`.

Stage 5AH hardens this coverage with stage-ledger truncation checks, README regression tests for ledgers that stop at Stage 5N, operational-file-map coverage auditing, current/next-stage consistency reports, active Stage 5AH source-of-truth records, and ignored-output checks for `experiments/results/doc-staleness/stage5ah/` plus `codex-output/**`.

Stage 5AI extends coverage with curated research-bundle schemas, local source-card and content-index builders, website-ingest and Deep-Research pack metadata, unclassified-source provisional classification, missing-source planning, guardrail and next-stage-decision checks, CLI validation paths, and ignored-output checks for `research-inputs/stage5ai/`, `experiments/results/research-bundles/stage5ai/`, `third_party/**`, and `codex-output/**`. It runs no Deep Research, network fetch, online clone, OCR/AI/ML, CUDA, benchmark, scored experiment, website expansion, or hypothesis execution.

Stage 5AK extends coverage with community-facts local inventory schemas, ordered attachment indexes, claim records, correction logs, arithmetic-preflight checks, source-card/content-index updates, Deep-Research pack readiness updates, publication guardrails, next-stage-decision checks, CLI validation paths, and ignored-output checks for `research-inputs/stage5ak/`, `experiments/results/research-bundles/stage5ak/`, `experiments/results/source-harvester-community-facts/stage5ak/`, `third_party/UsefulFilesAndIdeas/community-facts/**`, and `codex-output/**`. It runs no Deep Research, network fetch, live scrape, online clone, Google Drive storage, OCR/AI/ML, image forensics, stego/audio tooling, CUDA, benchmark, scored experiment, website expansion, or hypothesis execution.

Stage 5AL extends coverage with website-ingest schemas, metadata package validation, publication-gate checks, private Deep Research export checks, private-content blocking, next-stage decision checks, CLI validation paths, and ignored-output checks for `research-inputs/stage5al/`, `experiments/results/website-ingest/stage5al/`, and `codex-output/**`. It runs no Deep Research, network fetch, live scrape, online clone, Google Drive storage, OCR/AI/ML, image forensics, stego/audio tooling, CUDA, benchmark, scored experiment, website publication, or hypothesis execution.

Stage 5AM extends coverage with website-render schemas, static renderer generation, required page/data/asset checks, no external dependency checks, noindex/robots checks, privacy/publication audits, publication-gate preservation, safe search-index checks, upload manifest checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `website-export/stage5am/`, `experiments/results/website-render/stage5am/`, `research-inputs/stage5al/`, and `codex-output/**`. It runs no Deep Research, network fetch, live scrape, online clone, Google Drive storage, OCR/AI/ML, image forensics, stego/audio tooling, CUDA, benchmark, scored experiment, public website publication, or hypothesis execution.

Stage 5AN extends coverage with deep-research-export schemas, content-pack generation, hosted private-content export generation, combined SFTP webroot generation, safe local-source extract metadata, publication-gate audits, upload instructions, consumption guides, next-stage decision checks, CLI validation paths, and ignored-output checks for `deep-research-content-packs/stage5an/`, `website-export/stage5an/`, `third_party/**`, `research-inputs/**`, and `codex-output/**`. It runs no Deep Research, network fetch, live scrape, online clone, Google Drive storage, OCR/AI/ML, image forensics, stego/audio tooling, CUDA, benchmark, scored experiment, public website publication, or hypothesis execution.

Stage 5AR extends coverage with original-image coordinate-lock schemas, image-variant classification checks, source-backed 10/13/9 page-split checks, 256 pixel-coordinate record checks, bounding-box validation, case-ambiguity policy checks, null-control/DWH context updates, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5ar/`, raw page images, raw image drops, and `codex-output/**`. It runs no Deep Research, OCR/AI/ML, semantic image interpretation, hidden-content image forensics, LP-page OutGuess, stego execution, decode attempt, hash/preimage search, CUDA, benchmark, scored experiment, or hypothesis execution.

Stage 5AT extends coverage with token case-review schemas, active ambiguity class checks, grouped challenge-set checks, canonical-transcription challenge checks, crop-manifest checks, decision-template checks, review-pack builder checks, variant-classifier repair checks, doc-drift repair checks, null-control and DWH context checks, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `human-review-packs/stage5at/token-case-review/`, `experiments/results/token-block/stage5at/`, raw page images, generated crops, generated review packs, and `codex-output/**`. It runs no Deep Research, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content image forensics, LP-page OutGuess, stego execution, decode attempt, hash/preimage search, CUDA, benchmark, scored experiment, or hypothesis execution.

Stage 5AU extends coverage with review-pack usability audit schemas, crop-geometry policy checks, deterministic glyph-candidate crop checks, crop-quality diagnostics, v2 review-pack builder checks, UI coverage checks for all 203 case-review challenges and all 212 canonical-transcription challenges, blank decision-template checks, null-control/DWH context checks, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `human-review-packs/stage5au/token-case-review-v2/`, `experiments/results/token-block/stage5au/`, raw page images, generated crops, generated overlays, generated review packs, and `codex-output/**`. It runs no Deep Research, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content image forensics, LP-page OutGuess, stego execution, decode attempt, hash/preimage search, CUDA, benchmark, scored experiment, or hypothesis execution.

Stage 5AV extends coverage with decision-ingest schemas, decision-file validation checks, possible-token parsing, reviewer-extra token preservation, primary-60 mappability classification, compact branch-manifest checks, canonical non-update checks, null-control/DWH update checks, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`, `experiments/results/token-block/stage5av/`, raw page images, generated variant outputs, and `codex-output/**`. It runs no token experiments, variant byte-stream generation, DWH/hash search, decode attempt, OCR/AI/ML, LLM/vision token reading, hidden-content forensics, stego, CUDA, benchmark, scored experiment, or hypothesis execution.

Stage 5AW extends coverage with possible-token parser repair tests, malformed-fragment audit checks, repaired reviewer-extra token checks, visual-placeholder unmappable classification, primary-60 impact recalculation checks, repaired branch-manifest checks, canonical non-update checks, null-control/DWH update checks, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5aw/`, `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`, raw page images, generated variant outputs, and `codex-output/**`. It runs no token experiments, variant byte-stream generation, DWH/hash search, decode attempt, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content forensics, stego, CUDA, benchmark, scored experiment, or hypothesis execution.

Stage 5AY extends coverage with preflight source-input schemas, Stage 5AW repaired branch-manifest consumption checks, branch-eligibility classification checks, bounded variant-family checks, null/alphabet/reading-order/page-split/source-control checks, branch-count budget checks, future result schema preview checks, execution-gate checks, DWH blocking checks, guardrail checks, Stage 5AX validation linkage checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5ay/`, raw page images, human-review packs, generated variant outputs, and `codex-output/**`. It runs no token experiments, variant byte-stream generation, DWH/hash search, decode attempt, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content forensics, stego, CUDA, benchmark, scored experiment, or hypothesis execution.

Stage 5AZ extends coverage with preflight manifest-integrity schemas, duplicate family-ID detection, repaired unique family-record checks, taxonomy-membership checks for `unresolved_as_current_only`, Stage 5AW/Stage 5AV source-state checks, branch-budget preservation checks, execution-gate manifest-integrity coverage, Deep Research readiness checks, DWH/hash-search blocking, guardrail checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5az/`, raw page images, human-review packs, generated variant outputs, and `codex-output/**`. It runs no token experiments, variant byte-stream generation, DWH/hash search, decode attempt, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content forensics, stego, CUDA, benchmark, scored experiment, public website expansion, or hypothesis execution.

Stage 5BD extends coverage with dry-run policy schemas, active-manifest lock checks, deterministic run-plan ID policy/registry checks, dry-run plan and family counter checks, future result-path validation checks, fixture-only result example checks, execution-gate dry-run validation, no-byte-stream proof checks, Stage 5BB validation-evidence consolidation checks, archive marker policy checks, DWH dry-run context checks, guardrail checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bd/`, `deep-research-repo-zips/stage5bd/`, raw page images, human-review packs, generated variant outputs, fixture byte streams, and `codex-output/**`. It runs no token experiments, real byte-stream generation, variant materialisation, DWH/hash search, hash comparison, decode attempt, scoring, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content forensics, stego, CUDA, benchmark, scored experiment, public website expansion, or hypothesis execution.

Stage 5BF extends coverage with historical-route source-lock schemas, local archive location preference checks, archive tree and inventory summaries, annual route inventories for 2012 through 2017, high-priority artifact family checks, trust-classification policy and records, PGP/stego/OutGuess/OpenPuff/MP3/magic-square/hex-JPEG/onion/book-code/network-byte-channel/Liber Primus candidate checks, historical technique taxonomy checks, token-block planning impact checks, DWH historical context checks, guardrails, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/historical-route/stage5bf/`, `deep-research-content-packs/stage5bf/`, `deep-research-repo-zips/stage5bf/`, `third_party/CicadaSolversIddqd/**`, and `codex-output/**`. It runs no network clone, live scrape, online PGP fetch, OCR/AI/ML/LLM-vision, hidden-content image forensics, stego tools, token experiments, byte-stream generation, DWH/hash search, CUDA, benchmark, scored experiment, public website expansion, or hypothesis execution.

Stage 5BK extends coverage with iddqd-v2 source-root and tree metadata checks, byte-string source-lock checks, String 1-3 Stage 5BJ crosswalk checks, String 4 page49-51 context checks, transcription/translation/key-lineage metadata checks, positive-control context checks, planning constraint and source-gap severity checks, Stage 5BJ errata checks, token-block lineage preservation checks, Codex handoff policy checks, CLI validation paths, and ignored-output checks for `experiments/results/historical-route/stage5bk/`, `experiments/results/token-block/stage5bk/`, `third_party/CiadaSolversIddqd_v2/**`, `third_party/CicadaSolversIddqd_v2/**`, and `codex-output/**`. It runs no token experiments, byte-stream generation, variant materialisation, DWH/hash/preimage search, decode attempt, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or hypothesis execution.

Stage 5BM extends coverage with Stage 5BL findings-integration schemas, String 4 source-restatement checks, primary-60 inverse policy checks, Stage 5AP mismatch analysis checks, Stage 5AW branch-membership checks, ambiguity-class coverage checks, planning-constraint checks, source-gap severity and historical-family granularity updates, Stage 5BJ errata supersession, DWH quarantine, token-block lineage preservation, future dry-run planning impact, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bm/`, `experiments/results/historical-route/stage5bm/`, `third_party/CiadaSolversIddqd_v2/**`, `third_party/CicadaSolversIddqd_v2/**`, and `codex-output/**`. It runs no token experiments, byte-stream generation, variant materialisation, DWH/hash/preimage search, decode attempt, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or hypothesis execution.

Stage 5BN extends coverage with target-position schemas, Stage 5AW option-gap checks, local spreadsheet target-row checks, coordinate-context checks, source-evidence synthesis checks, inactive addendum checks, source-gap closure/status checks, planning-constraint and lineage checks, DWH quarantine and guardrail checks, Codex handoff checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bn/`, `experiments/results/historical-route/stage5bn/`, `human-review-packs/stage5bn/`, `third_party/3N_3p_Bases_49-51.jpg.xlsx`, and `codex-output/**`. It confirms Stage 5AW still does not support active `0l`, the local target row supports `0l`, the addendum remains inactive/review-only, and no token experiments, byte-stream generation, variant materialisation, DWH/hash/preimage search, decode attempt, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or hypothesis execution ran.

Stage 5BO extends coverage with corrected decision-template source-lock schemas, compact token-case errata parsing, exact case-preserving possible-token diffs, inactive errata-aware option-universe checks, String 4 after-errata branch membership checks, Stage 5BN addendum integration checks, source-gap closure checks, guardrail checks, Codex handoff checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bo/`, `experiments/results/historical-route/stage5bo/`, `human-review-packs/stage5au/token-case-review-v2/decision-template*.yaml`, and `codex-output/**`. It confirms case `199` and case `198` corrections are represented, String 4 becomes a full branch match only in inactive planning metadata, active Stage 5AW/5AY/5AZ/5BD records remain unchanged, and no token experiments, byte-stream generation, variant materialisation, DWH/hash/preimage search, decode attempt, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or hypothesis execution ran.

Stage 5BS extends coverage with Stage 5BR findings-integration schemas, reviewable stage-marker/validation-evidence/source-digest/gap records, planning-ingestion gate checks, future-runner citation policy checks, inactive-sidecar policy checks, active-ingestion blocker checks, Stage 5BD plan preservation checks, active-manifest preservation checks, DWH quarantine and guardrail checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bs/` and `codex-output/**`. It confirms String 4 remains inactive, active input and dry-run ingestion are false, future-runner citation is fail-closed, Stage 5BD records remain valid, canonical transcription and active manifests remain unchanged, and no token experiments, byte-stream generation, variant materialisation, DWH/hash/preimage search, decode attempt, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or hypothesis execution ran.

Stage 5BQ extends coverage with Stage 5BP findings-integration schemas, inactive String 4 planning-context records, operator-errata sidecar status, fail-closed dry-run constraint updates, no-active-ingestion proof, future dry-run requirements, active-manifest preservation, Stage 5BD lineage preservation, source-gap severity and DWH quarantine reaffirmation, guardrail checks, Codex handoff checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bq/` and `codex-output/**`. It confirms String 4 remains inactive, active input and dry-run ingestion are false, Stage 5BD records remain valid, canonical transcription and active manifests remain unchanged, and no token experiments, byte-stream generation, variant materialisation, DWH/hash/preimage search, decode attempt, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or hypothesis execution ran.

Stage 5AX extends coverage with parallel-validation schema checks, command-classification checks, serial-only scheduler protections, subprocess log separation, deterministic pytest sharding, xdist detection and fallback behavior, result/failure aggregation, worker-limit checks, safety audit checks, CLI/script checks, ignored-output checks for `experiments/results/ci/parallel-validation/stage5ax/`, and Stage 5AY next-stage decision checks. It runs no token experiments, variant byte-stream generation, DWH/hash search, decode attempt, OCR/AI/ML, LLM/vision token reading, semantic image interpretation, hidden-content forensics, stego, CUDA, cryptanalytic benchmark, scored experiment, or hypothesis execution.

Stage 5AP coverage remains in place for token-block source-lock schemas, canonical 32x8 transcription checks, logical coordinate checks, primary-60 alphabet and byte-mapping preflight checks, null-control and DWH context checks, page-image metadata provenance checks, OutGuess toolchain/matrix/guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5ap/`, `experiments/results/stego-controls/stage5ap/`, raw page images, raw image drops, and `codex-output/**`.

Stage 5AJ extends coverage with UsefulFiles local inventory schemas, workbook extraction summaries, important-link parsing, source-card/content-index updates, extraction-fidelity policy, redaction policy, scraper-capture policy, Deep-Research pack readiness updates, guardrail and next-stage-decision checks, CLI validation paths, and ignored-output checks for `research-inputs/stage5aj/`, `experiments/results/research-bundles/stage5aj/`, `experiments/results/source-harvester-usefulfiles/stage5aj/`, `third_party/UsefulFilesAndIdeas/**`, and `codex-output/**`. It runs no Deep Research, network fetch, live scrape, online clone, Google Drive storage, OCR/AI/ML, image forensics, stego/audio tooling, CUDA, benchmark, scored experiment, website expansion, or hypothesis execution.

Stage 5AC extends coverage with prime-minus-one CUDA synthetic reporting schemas, record builders, CLI commands, bounded-p56 preflight checks, full-p56 blocker preservation, scored-experiment deferral checks, Stage 5AB doc-staleness validation, deterministic next-stage decision checks, and ignored-output checks for `experiments/results/prime-minus-one-cuda-synthetic-reporting/stage5ac/` plus `codex-output/**`. It does not run CUDA, CMake, native parity, p56 CUDA, or benchmarks.

Stage 5AD extends coverage with bounded p56 CUDA parity schemas, run/parity record builders, result-store and score-summary preflight checks, full-p56 blocker preservation, scored-experiment deferral checks, device-subset audit checks, deterministic mismatch next-stage decisions, no-GPU `--skip-cuda` CLI validation paths, and ignored-output checks for `experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/` plus `codex-output/**`. It allows only the bounded vector run and still treats CUDA hash parity as correctness metadata, not benchmark or solve evidence.

Stage 5AD-fix extends coverage with bounded p56 mismatch schemas, hash-lineage builders, token/stream/formula trace checks, hash-material/reference-contract checks, root-cause and repair-readiness records, guardrail checks, next-stage decision checks, CLI validation paths, and ignored-output checks for `experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix/` plus `codex-output/**`. It runs no CUDA and treats the mismatch as reference-contract diagnostics, not performance or solve evidence.

Stage 5AG extends coverage with local source inventory schemas, missing-root graceful handling, synthetic file/directory inventory, ZIP archive listing without extraction commits, unsupported archive recording, SHA-256 hashing, duplicate detection, image metadata probes, manifest-local linkage, local unclassified source records, source-lock candidate classification, deterministic research-bundle readiness, guardrail records, next-stage decision determinism, CLI validation paths, and ignored-output checks for `experiments/results/source-harvester-local/stage5ag/`, `third_party/**`, `source-harvester-output/**`, `harvest-output/**`, `research-inputs/**`, and `codex-output/**`. It runs no live network fetch, online clone, CUDA, benchmarks, scored experiments, or hypothesis execution.

Stage 5AF extends coverage with source-harvester schemas, source-manifest validation, required source ID checks, manual-export flag checks for Google/Dropbox/Colab sources, dry-run planning, fetch/download guardrails, output-root rejection for committed paths, local archive/image/hash inventory fixtures, static HTML extraction, research-bundle scaffold generation, next-stage decision determinism, CLI validation paths, and ignored-output checks for `experiments/results/source-harvester/stage5af/`, `source-harvester-output/`, `harvest-output/`, `research-inputs/`, and `codex-output/**`. It runs no live network fetch, CUDA, benchmarks, scored experiments, or raw archive processing.

Stage 5AE extends coverage with corrected formula-parity schemas, Stage 5AD historical-failure preservation checks, corrected formula hash checks, reference-contract/hash-material policy checks, result-store and score-summary integration checks, method-status non-upgrade checks, generated-body policy checks, full-p56 and scored-experiment deferrals, archive/source-lock deferral checks, deterministic next-stage selection, CLI validation paths, and ignored-output checks for `experiments/results/prime-minus-one-bounded-p56-corrected-reporting/stage5ae/` plus `codex-output/**`. It runs no CUDA and does not reclassify Stage 5AD as passed.

Stage 4K extends this coverage with source-lock snapshot validation, allowlist/rejection tests,
snapshot-policy tests, GitHub commit-address parser tests, generated-output/cache ignore tests, and
state-drift checks for the Stage 4L ledger.

Stage 4L extends coverage with promotion-ledger schema checks, promotion-gate tests that keep visual,
cuneiform, dot, cookie, and stego/audio records from becoming executable seeds prematurely,
manifest-readiness tests that keep execution disabled, CLI build/validate checks, and ignored-output
checks for `experiments/results/observation-promotion/stage4l/`.

Stage 4M extends coverage with image-preflight schemas, deterministic synthetic image metadata and
compression metrics, source-variant blocked-status checks, review-only artifact candidates, blocked
bigram/Fibonacci-421 readiness, CLI build/validate checks, and ignored-output/raw-image checks for
`experiments/results/image-preflight/stage4m/`, `third_party/LiberPrimusPages/`, and
`data/raw/images/Fib421.jpg`.

Stage 4N extends coverage with stego/audio positive-control schemas, fixture classification,
cache policy, toolchain detection that does not execute tools, expected-output blockers, synthetic
control readiness, CLI build/validate checks, and ignored-output/raw-cache checks for
`experiments/results/stego-positive-controls/stage4n/` and `third_party/StegoPositiveControls/`.

Stage 4O extends coverage with CPU batch adapter expansion schemas, deterministic solved-fixture
stream building, missing-fixture skips, adapter coverage records, parity expectation hashes, score
summary compatibility, Stage 4O CLI commands, Stage 4H command preservation, and ignored-output/raw
data checks for `experiments/results/cpu-batch/stage4o/`.

Stage 4P extends coverage with unified result schemas, Stage 4I score-label validation, source
inventory missing-output and raw-required skips, deterministic score-summary unification,
method-status joins, cross-stage report counts, Stage 4P result-store CLI commands, existing
result-store command preservation, ignored-output checks, raw-data checks, and SQLite non-staging
checks for `experiments/results/result-store-unification/stage4p/`.

Stage 5C extends coverage with CUDA build/device schemas, no-GPU-safe build profile checks,
toolchain detection that tolerates missing CUDA, device detection that tolerates no GPU, optional
smoke-build records that do not execute CUDA tests by default, CLI build/validate checks, and
ignored-output/codex-output checks for `experiments/results/cuda-build/stage5c/` and
`codex-output/`.

Stage 5D extends coverage with native CPU backend schemas, C++ backend and deterministic threading
unit tests, Python/native parity checks, threading hash equality across multiple thread counts,
validation rejections for CUDA/performance/solve-claim drift, CLI run/validate checks, and
ignored-output/codex-output checks for `experiments/results/native-cpu/stage5d/` and
`codex-output/`.

Stage 5E extends coverage with first CUDA kernel contract schemas, contract selection tests,
native parity adapter mapping checks, implementation-readiness guardrails, CLI command checks,
validation rejections for CUDA/source/performance/solve-claim drift, and ignored-output/codex-output
checks for `experiments/results/cuda-kernel-contract/stage5e/` and `codex-output/`.

Stage 5V extends coverage with native Candidate Batch ABI conformance schemas, raw-data-free
conformance fixtures, token-buffer rules, key/stream schedule shape records, score-vector and top-k
shape checks, compact result-store conformance, implementation-status blockers, next-stage decision
guardrails, CLI build/validate checks, and ignored-output/codex-output checks for
`experiments/results/cuda-candidate-batch-abi-conformance/stage5v/` and `codex-output/`.

Stage 5W extends coverage with prime-minus-one source inventory schemas, source-backed stream
contract rules, deterministic prime schedule records, Candidate Batch ABI mapping checks, native
parity preparation blockers, result-store preflight records, guardrail checks, next-stage decision
records, CLI build/validate checks, and ignored-output/codex-output checks for
`experiments/results/prime-minus-one-native-contract/stage5w/` and `codex-output/`.

Stage 5X extends coverage with prime-minus-one native run schemas, no-GPU Python-reference execution
checks, native parity records, result-store and score-summary preflight records, full-p56 blocker
checks, guardrails, next-stage decisions, CLI build/validate checks, and ignored-output/codex-output
checks for `experiments/results/prime-minus-one-native-parity/stage5x/` and `codex-output/`.

Stage 5Y extends coverage with prime-minus-one compact reporting schemas, parity-report records,
Stage 4P result-store integration, Stage 4I score-summary integration, method-status impact,
generated-body policy, full-p56 blocker preservation, CUDA contract readiness gates, bounded
scored-experiment readiness, guardrails, next-stage decisions, CLI build/validate checks, and
ignored-output/codex-output checks for
`experiments/results/prime-minus-one-native-reporting/stage5y/` and `codex-output/`.

Stage 5AA extends coverage with prime-minus-one CUDA synthetic schemas, record builders, CLI commands, a no-GPU-safe skip path, the local synthetic CUDA parity path, p56/full-p56 blockers, scored-experiment deferrals, and ignore-policy checks. The optional CUDA run is scoped to one synthetic vector and is not required for CI.

Stage 5Z extends coverage with prime-minus-one CUDA contract schemas, CUDA-C style kernel ABI
records, host-runner contract records, buffer contract records, validation-vector records,
future-parity plan records, result-store compatibility records, full-p56 blocker records,
scored-experiment deferral records, implementation-readiness gates, next-stage decisions, CLI
build/validate checks, guardrail rejection tests for CUDA execution/source changes/kernels/solve
claims, and ignored-output/codex-output checks for
`experiments/results/prime-minus-one-cuda-contract/stage5z/` and `codex-output/`.

Stage 5F extends coverage with synthetic CUDA kernel implementation schemas, no-GPU-safe build
records, optional local synthetic parity records, C++/CUDA synthetic parity tests, CLI
build/validate/summary checks, validation rejections for real Liber Primus data, benchmarking,
performance/speedup, generated-output, and solve-claim drift, and ignored-output/codex-output checks
for `experiments/results/cuda-kernel/stage5f/` and `codex-output/`.

Stage 5G extends coverage with CUDA parity-reporting schemas, no-GPU-safe report builders,
device-code subset audit checks, solved-fixture-safe preflight blockers, CLI
build/validate/summary checks, validation rejections for real Liber Primus data, benchmarking,
performance/speedup, generated-output, and solve-claim drift, and ignored-output/codex-output checks
for `experiments/results/cuda-parity-reporting/stage5g/` and `codex-output/`.

Stage 5H extends coverage with Gematria shift contract schemas, numeric mod-29 native fixture
checks, solved-fixture-safe mapping blockers, score-summary parity planning, CLI
build/validate/summary checks, validation rejections for CUDA execution, new kernels,
generated-output, and solve-claim drift, and ignored-output/codex-output checks for
`experiments/results/gematria-shift-contract/stage5h/` and `codex-output/`.

Stage 5I extends coverage with Gematria CUDA preparation schemas, CUDA-C ABI planning, validation
vectors, implementation checklist guardrails, CLI build/validate/summary checks, validation
rejections for CUDA execution, new kernels, CUDA source changes, production Gematria CUDA readiness,
generated-output, codex-output, and solve-claim drift, and ignored-output/codex-output checks for
`experiments/results/gematria-cuda-prep/stage5i/` and `codex-output/`.

Stage 5J extends coverage with Gematria CUDA kernel schemas, implementation/build/parity records,
optional local synthetic parity, no-GPU-safe consistency temp outputs, conservative device-code
subset checks, CLI build/validate/summary checks, validation rejections for real Liber Primus CUDA
data, solved/unsolved page CUDA use, production Gematria CUDA readiness, benchmarking,
performance/speedup, generated-output, codex-output, and solve-claim drift, and ignored-output
checks for `experiments/results/gematria-cuda-kernel/stage5j/` and `codex-output/`.

Stage 5U extends coverage with Candidate Batch ABI schemas, token-buffer contract checks,
transform-parameter family coverage, key-schedule and stream-schedule contract tests, Stage 4I
score-vector contract checks, deterministic top-k contract checks, backend-surface guardrails,
result-store compatibility tests, Stage 5T ABI gap closure checks, next-stage decision checks,
CLI build/validate/summary checks, validation rejections for CUDA/source/benchmark/generated-output
and solve-claim drift, and ignored-output/codex-output checks for
`experiments/results/cuda-candidate-batch-abi/stage5u/` and `codex-output/`.

Stage 5K extends coverage with Gematria CUDA parity-reporting schemas, Stage 5J parity report
records, CUDA device-code audit records, solved-fixture-safe preflight records, score-summary
preflight records, CLI build/validate/summary checks, validation rejections for CUDA execution,
new kernels, CUDA source changes, solved/unsolved page CUDA use, production Gematria CUDA readiness,
benchmarking, performance/speedup, generated-output, codex-output, and solve-claim drift, and
ignored-output checks for `experiments/results/gematria-cuda-parity-reporting/stage5k/` and
`codex-output/`.

Stage 5T extends coverage with solved-family CUDA readiness schemas, solved-family inventory
checks, parity-matrix checks that keep original transform semantics distinct from current
shift-score parity, kernel-readiness rankings that do not authorize implementation, candidate
batch ABI gap records, benchmark-readiness planning-only records, no-unsolved guardrail records,
deterministic next-stage decision tests, CLI build/validate/summary checks, and ignored-output,
raw-data, SQLite, and codex-output checks for
`experiments/results/cuda-solved-family-readiness/stage5t/` and `codex-output/`.

## Stage 3W State-Drift Tests

Stage 3W tests cover the state-drift checker, stale current-stage phrase detection, historical-reference allowances, required CUDA/corpus/page-boundary/raw-output/Discord privacy facts, pyproject metadata, persistent doc current-state coverage, and CLI integration through `libreprimus consistency check-state-drift`.

## Stage 3X CLI Command-Surface Tests

Stage 3X tests cover the modular CLI package layout, the thin public `python -m libreprimus.cli` entrypoint, preserved root command groups, selected high-risk subcommands, help output, and the rule that no `python/libreprimus/cli/` package may exist while `cli.py` remains the public module.

## Stage 3Y Research Synthesis Tests

Stage 3Y tests cover the durable staged plan, research synthesis schemas, method-family status records, method-retirement references, Deep Research influence records, direction-change records, `libreprimus research-synthesis` CLI commands, and state-drift integration for `docs/roadmap/staged-plan.md`.

The local validation stack now includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```

## Stage 3Z Onboarding And Source-Of-Truth Tests

Stage 3Z tests cover onboarding docs, Stage 4A direction in the staged plan, direction-change records, AGENTS doc freshness policy, private/generated data maps, and state-drift integration for the new onboarding maps.

## Stage 4A Discord Full Review Bundle Tests

Stage 4A tests cover full-review schemas, synthetic Discord-like HTML parsing, redaction of
usernames/IDs/message IDs/private Discord URLs, public-link preservation, low-signal message
retention, huge-channel shard splitting, multi-topic classification, image and attachment reference
indexes, synthetic LP page-gallery thumbnails, static-site generation, Deep Research manifests, SFTP
instructions, aggregate privacy checks, Wiki publish diagnostics, generated-output ignore rules, and
CLI build/validate/summary paths using synthetic fixtures.

Stage 4A follow-up tests cover static review-site privacy hardening: noindex metadata, all-disallow
`robots.txt`, site privacy notice, SFTP upload checklist, optional `.htaccess` guidance, deterministic
site manifests, validation failures when noindex metadata is missing, and Wiki publish blocker
reporting.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review validate --results-dir experiments/results/discord-full-review/stage4a
```

## Stage 4B Source-Lock Triage Tests

Stage 4B tests cover source-lock schemas, allowlisted URL classification, unsafe Discord/CDN rejection, duplicate URL normalization, visual observation guardrails, negative-control records, disabled manifest flags, CLI run/validate behavior on synthetic Stage 4A indexes, and ignore policy for generated triage outputs, raw Discord logs, and raw page images.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-triage validate `
  --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml `
  --source-health data/locks/third-party/stage4b-source-health-records.yaml `
  --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
  --cookie-source-records data/observations/web/stage4b-cookie-candidate-source-records.yaml `
  --manifest-dir experiments/manifests/stage4b-disabled
```

## Stage 4C Visual Annotation Tests

Stage 4C tests cover visual annotation schemas, cuneiform candidate guardrails, dot-pattern ambiguity, delimiter reset-boundary blocking, visual negative-control tasks, generated static annotation-site pages, blank template generation, CLI build/validate behavior on synthetic records/images, and ignore policy for generated annotation outputs, raw page images, and raw Discord logs.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli visual-annotation validate `
  --task data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --summary data/observations/visual/stage4c-annotation-pack-summary.yaml
```

## Stage 4D Bounded Numeric Tests

Stage 4D tests cover bounded numeric schemas, no-fudge policy rejection for nearest-prime and arbitrary adjustment operations, deterministic route builders, delimiter metadata audit behavior, cuneiform deferral when coordinates/readout are absent, visual negative-control ambiguity metrics, CLI run/validate behavior on synthetic records, and ignore policy for generated bounded-numeric outputs, raw Discord logs, and raw page images.

## Stage 4E Source-Delta Audit Tests

Stage 4E tests cover source-delta schemas, path classification for LP images, `lp_outguessed`, audio candidates, and font metadata-only paths, validation guardrails for raw/font commits, image-compression artefact future-preflight records, disabled future manifests, CLI behavior against a synthetic local git tree, network-disabled deferred records, and ignore policy for the local cache and generated reports.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-delta-audit validate `
  --source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
  --source-health data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml `
  --image-artifact data/observations/visual/stage4e-image-compression-artifact-observations.yaml `
  --manifest-dir experiments/manifests/stage4e-disabled
```

## Stage 4F Stego Audio Fixture Tests

Stage 4F tests cover stego/audio fixture schemas, fixture classification for `lp_outguessed`, Interconnectedness MP3, `4gq25.jpg`, and font metadata-only paths, validation guardrails for raw/binary/audio/image/font commits, disabled future manifests, toolchain requirement separation, CLI behavior on synthetic records, and ignore policy for generated fixture reports and raw caches.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-fixtures validate `
  --outguess-fixtures data/observations/stego/stage4f-outguess-fixture-source-records.yaml `
  --audio-fixtures data/observations/stego/stage4f-audio-fixture-source-records.yaml `
  --source-health data/locks/third-party/stage4f-stego-fixture-source-health.yaml `
  --toolchain data/observations/stego/stage4f-toolchain-requirements.yaml `
  --manifest-dir experiments/manifests/stego/stage4f-disabled
```

## Stage 4N Stego Audio Positive-Control Tests

Stage 4N tests cover readiness schemas, `lp_outguessed` classification, MP3/audio and image fixture
classification, cache policy guardrails, missing expected-output blockers, synthetic-ready controls,
toolchain-unavailable handling, CLI behavior on synthetic records, and ignore policy for generated
reports and raw caches.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego-positive-controls validate `
  --outguess-readiness data/observations/stego/stage4n-outguess-positive-control-readiness.yaml `
  --audio-readiness data/observations/stego/stage4n-audio-positive-control-readiness.yaml `
  --fixture-cache data/observations/stego/stage4n-fixture-cache-records.yaml `
  --expected-output data/observations/stego/stage4n-expected-output-records.yaml `
  --toolchain data/observations/stego/stage4n-toolchain-readiness.yaml `
  --summary data/observations/stego/stage4n-positive-control-summary.yaml
```

## Stage 4G Cookie Refresh Tests

Stage 4G tests cover cookie-refresh schemas, source-backed candidate loading, manifest-declared variant and algorithm enforcement, fuzzy/partial rejection, deterministic byte variants, deduplication, cap failures, exact-match and non-match hash behavior, CLI behavior on synthetic records, generated output ignore policy, raw Discord/page-image ignore policy, and no-solve/CUDA/hashcat flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cookie-refresh validate `
  --results-dir experiments/results/cookie-refresh/stage4g `
  --summary data/observations/web/stage4g-cookie-refresh-summary.yaml
.\.venv\Scripts\python.exe -m pytest -q tests/python
```

## Stage 4H CPU Batch Tests

Stage 4H tests cover CPU batch schemas, deterministic synthetic input streams, transform adapter dispatch, adapter-missing handling, deterministic batch runner records, stable output hashes, scoring adapter unavailable/scored paths, parity contract fields, CLI run/validate/adapter-coverage commands, generated output ignore policy, raw data ignore policy, and no-solve/CUDA flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-manifest `
  --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-results `
  --results-dir experiments/results/cpu-batch/stage4h
.\.venv\Scripts\python.exe -m pytest -q tests/python
```

## Stage 4O CPU Batch Adapter Expansion Tests

Stage 4O tests cover adapter coverage schemas, solved-fixture-safe stream records, explicit missing
fixture skips, deferred adapter reasons, parity expectation hashes, score-summary compatibility,
Stage 4O CLI commands, Stage 4H command preservation, generated output ignore policy, raw data
ignore policy, and no-solve/CUDA flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-stage4o `
  --results-dir experiments/results/cpu-batch/stage4o `
  --summary data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml
.\.venv\Scripts\python.exe -m pytest -q tests/python
```

## Stage 4P Result Store Score Summary Unification Tests

Stage 4P tests cover unified result schemas, score-summary schemas, source inventory determinism,
optional generated-output missing records, raw-required source skips, Stage 4I confidence-label
preservation, score-unavailable warnings, method-status joins, cross-stage report counts, CLI
build/validate commands, existing result-store command preservation, generated output ignore policy,
raw data ignore policy, and SQLite non-staging rules.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-stage4p `
  --results-dir experiments/results/result-store-unification/stage4p `
  --summary data/research/stage4p-result-store-score-summary-unification-summary.yaml
.\.venv\Scripts\python.exe -m pytest -q tests/python
```

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric validate `
  --results-dir experiments/results/bounded-numeric/stage4d
```

## Stage 3O Promotion And Wiki Tests

Stage 3O tests cover Discord promotion redaction, public-safe URL filtering, review-only promotion records, README/tutorial coverage, Wiki source generation, Wiki validation scripts, and ignored raw/generated paths.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-promote validate-promoted --links data/observations/discord/promoted-public-source-links-stage3o.yaml --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml --allow-empty
.\scripts\github\validate-wiki-source.ps1
.\scripts\github\sync-tutorials-to-wiki.ps1 --DryRun
```

## Stage 3Q Discord Review Bundle Tests

Stage 3Q tests cover schema parsing, redaction of usernames/IDs/private URLs, preservation of public external URLs, topic classification, review lead construction, shard privacy headers, shard splitting, local review-index generation, CLI missing-input mode, aggregate privacy flags, and ignored generated shard paths.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review validate-bundles `
  --results-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing
```

## Stage 3R Discord Lead Promotion Tests

Stage 3R tests cover schema validation, public/private URL corroboration, Discord-only claim rejection, promoted source and observation records, negative-control classes, disabled manifest caps, CLI promote/build/validate behavior, privacy policy checks, and ignored generated outputs.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads validate `
  --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls data/observations/discord/stage3r-negative-control-records.yaml `
  --manifest-dir experiments/manifests/post-discord `
  --allow-empty
```

## Stage 3S Onion 7 Seed-Pack Tests

Stage 3S tests cover manifest validation, candidate cap checks, raw 4x4 table shape, deterministic route builders, mod-29 reduction, stream repetition, reset behavior, candidate record fields, CLI validation and execution against a synthetic manifest, ignored generated outputs, raw Discord ignore policy, and raw image ignore policy.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord summary `
  --results-dir experiments/results/post-discord/stage3s
```

## Stage 3T GP/Rune Claim Verifier Tests

Stage 3T tests cover manifest validation, claim-cap checks, claim deduplication, malformed and unsupported claim classification, missing-span handling, synthetic rune counts, transformable-rune counts, GP sums, mod-29 residues, derived cuneiform arithmetic, boundary-sensitive classification, CLI validation/execution against synthetic records, ignored generated outputs, raw Discord ignore policy, raw image ignore policy, and no-solve flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-gp-rune-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord gp-rune-summary `
  --results-dir experiments/results/post-discord/stage3t
```

## Stage 3U Cookie Signed-Variant Tests

Stage 3U tests cover manifest validation, candidate-cap checks, SHA-256-only enforcement, cookie-record loading, hex64 validation, deterministic byte variants, compact variants, deduplication, cap-exceeded failure, exact-match output generation, no partial/fuzzy matching, CLI validation/execution against synthetic records, ignored generated outputs, raw Discord ignore policy, raw image ignore policy, and no-solve/CUDA flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-cookie-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord cookie-signed-summary `
  --results-dir experiments/results/post-discord/stage3u
```

## Stage 3V OutGuess Regression Tests

Stage 3V tests cover stego schemas, manifest/artifact validation, missing-tool skips, missing-asset skips, fake OutGuess success and failure, exact expected-payload hash matching, expected-payload hash mismatch, no raw payload commits, no solve claims, CUDA-off flags, CLI detection/validation/run behavior, generated output ignore rules, third-party artefact ignore rules, raw Discord ignore rules, and raw page-image ignore rules.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-validate-manifest `
  --manifest experiments/manifests/stego/outguess-regression-v1.yaml `
  --artifacts data/observations/stego/outguess-artifacts-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-summary `
  --results-dir experiments/results/stego/outguess/stage3v
```

Legacy workbook tests include p56 prime-minus-one first-delta checks, Welcome `DIVINITY` delta checks, and direct-page zero-delta checks for solved fixture hints.

Legacy Pastebin tests include first-pair prime validation, empty-pair preservation, Parable anchor detection, page-boundary non-finalization, and local-real-file conditional tests.

Stage 0D tests cover rtkd parser preservation, scream314 reference parsing, signature indexing, Pastebin-to-transcript alignment, tentative page-boundary candidates, glyph variant `ᛂ`, CLI commands, and real-source conditional smoke checks.

## Stage 0A smoke tests

Stage 0A includes C++ and Python smoke tests only.

## Stage 0B workbook tests

Stage 0B parser tests are Python-only. CUDA and C++ behavior are unchanged.

## Stage 0C Pastebin tests

Stage 0C parser tests are Python-only. They verify that prime values are converted to decimal indices and that generated records remain non-canonical.

## Stage 0D alignment tests

Stage 0D parser and alignment tests are Python-only. They assert no canonical boundary activation, no canonical trust flag, raw glyph preservation, and timing metadata presence.

## Stage 0D-P documentation and GitHub checks

Stage 0D-P validates tutorial, issue seed, wiki source, and GitHub script existence. GitHub helper scripts support dry runs before mutating labels, issues, or wiki pages.

## Stage 0D-followup parser, alignment, and boundary tests

Stage 0D-followup tests cover transcript physical/logical/stream views, bounded stream-subsequence matching, gap diagnostics, stricter boundary confidence auditing, CLI commands, and real-source conditional smoke checks. Tests assert that empty-pair-only and word-length-only evidence cannot create high-confidence boundaries, all boundaries keep `canonical_page_boundary=false`, and all alignment records remain non-canonical.

## Stage 0E profile and corpus candidate tests

Stage 0E tests validate Gematria profile invariants, glyph variant profile policy, separator grammar rules, corpus tokenization, JSON schemas, synthetic candidate generation, real-source conditional generation, and CLI commands.

## Stage 1A solved fixture tests

Stage 1A tests validate fixture schemas, direct-translation decoding, span selection, provenance validation, synthetic reproduction, real-source conditional reproduction, and solved-fixture CLI commands. They assert that direct fixtures do not use Atbash, Vigenere, prime streams, search, or CUDA.
## Stage 1B Tests

Stage 1B adds tests for reverse Gematria and rotated reverse Gematria formulas, explicit rotation validation, fixture schema compatibility, synthetic Atbash-family reproduction, direct-fixture regression, CLI smoke behavior, and real-source conditional reproduction.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
```

C++ tests are not required for Stage 1B unless C++ files change.
## Stage 1C Tests

Stage 1C tests cover reference mirroring metadata, reference-method extraction, explicit-key Vigenere key conversion, subtract decryption, key-advance rules, fixture-declared cleartext-F pass-through, fixture schema validation, synthetic reproduction, CLI commands, and real-source conditional reproduction.

The Stage 1C smoke keeps Stage 1A direct and Stage 1B Atbash-family fixtures as regressions.

## Stage 1D Tests

Stage 1D tests cover deterministic prime generation, prime-minus-one / phi-prime equivalence, stream advancement rules, cleartext-F skip handling, payload hash checks, fixture schema validation, synthetic reproduction, CLI commands, and real-source conditional reproduction.

The Stage 1D smoke keeps Stage 1A direct, Stage 1B Atbash-family, and Stage 1C Vigenere fixtures as regressions. C++ tests are not required for Stage 1D unless C++ files change.

## Stage 2A Tests

Stage 2A tests cover transform registry metadata, SHA-256 locks, alias resolution, CPU dispatch, manifest schema validation, synthetic solved-baseline runner outputs, CLI commands, and real-source conditional smoke checks.

The Stage 2A smoke reproduces 10 known solved fixtures through registry dispatch. C++ tests are not required for Stage 2A unless C++ files change.

## Stage 2B Tests

Stage 2B tests cover result-store JSON schemas, JSONL sink determinism, SQLite table creation and duplicate handling, provenance capture, solved-baseline import, CLI commands, and real-source conditional smoke checks.

The Stage 2B smoke imports the Stage 2A all-known solved-baseline run into generated JSONL and SQLite result stores. C++ tests are not required for Stage 2B unless C++ files change.

## Historical snapshot: Stage 2C Tests

Stage 2C adds static workflow tests and CI script tests. They verify `.github/workflows/ci.yml` runs on push and pull requests, uses Python 3.12, runs Ruff and pytest, validates the transform registry and committed manifests, avoids secrets and artifact uploads, and keeps scripts raw-data-free.

Local CI reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
.\scripts\ci\validate-workflow-static.ps1
```

The GitHub Actions workflow also includes a CPU-only CMake smoke job with CUDA disabled.

Stage 2C-followup extends workflow tests to parse YAML with PyYAML, validate trigger and job structure, and reject flattened/minified workflow files.

Stage 2C-followup-2 adds post-push remote workflow verification scripts and strengthens static tests with an explicit minified workflow rejection sample.

Stage 2C-followup-3 adds `.gitattributes` static tests and canonical lock-hash line-ending tests. CI now verifies lock hashes before Python tests.

Stage 2C-followup-4 adds public documentation status tests for README, STATUS, and ROADMAP. These tests allow historical stage mentions but reject stale top-level current-status and next-milestone language.

Stage 2C-followup-5 adds remote Git blob verifier tests that require post-push workflow and `.gitattributes` checks to use `git show` as the authoritative remote source and treat raw URL mismatches as warnings.

## Stage 2D Consistency Tests

Stage 2D adds tests for consistency models, registry checks, manifest checks, schema checks, documentation checks, ignored-output checks, result-store checks, and CLI behavior.

## Stage 2E Dry-Run Planner Tests

Stage 2E adds tests for exploratory schemas, candidate-count estimators, safety gates, dry-run planner records, committed exploratory manifests, and `libreprimus experiment` CLI commands.

The tests assert that dry-run plans preserve disabled execution/search/candidate-generation/scoring/CUDA flags and do not include candidate plaintext fields.

## Stage 2F Bounded CPU Execution Tests

Stage 2F adds tests for CPU execution schemas, safety gates, synthetic execution, solved-fixture replay, blocked unsolved execution, CLI behavior, and committed manifest files.

The tests assert that synthetic direct, reverse, rotated reverse, Vigenere, and prime-stream examples pass; the blocked unsolved manifest fails; and search, candidate generation, scoring, and CUDA remain disabled.

## Stage 2G Proposal Approval Tests

Stage 2G adds tests for proposal schemas, approval records, approval gates, review packet generation, CLI behavior, and committed proposal files.

The tests assert that pending, denied, missing, invalid, expired, and mismatched approvals block execution; committed Stage 2G proposals are unapproved and non-executable; and review packets contain no candidate plaintext outputs.

## Stage 2H Approval-Gated Execution Tests

Stage 2H adds tests for approval-gated request schemas, approval gate behavior, approved synthetic and solved-control execution, blocked no-op real proposals, CLI behavior, and committed Stage 2H files.

The tests assert that proposal SHA, scope, expiry, approver, and constraints are checked; approved synthetic and solved-control requests pass; no approval, pending approval, denied approval, expired approval, wrong scope, mismatched SHA, and future-unsolved proposals block; and search, candidate generation, scoring, and CUDA remain disabled.

## Stage 2I Approval-Readiness Tests

Stage 2I adds tests for approval-readiness packet schemas, readiness analysis, packet generation, committed proposal files, CLI behavior, and no-execution guarantees.

The tests assert that the first real proposal remains pending and unapproved, candidate-count estimate and upper bound are `841`, generated packets contain no raw unsolved text or candidate plaintext, no approved Stage 2I approval records are committed, and approval-readiness commands do not invoke the execution runner.

## Stage 2J Bounded Auto-Run Tests

Stage 2J adds tests for operator policies, bounded queues, policy checking, bounded runner behavior, and `libreprimus bounded-experiment` CLI commands.

The tests assert that the `841` candidate Caesar plus affine item passes policy, the solved-baseline control passes policy, over-budget/CUDA/cloud/solve-claim/generated-output-commit items fail policy, blocked items do not run, generated outputs are ignored, and per-experiment approval is not required for policy-passing bounded local CPU items.

## Stage 3A Minimal Executor Tests

## Stage 3J Mersenne Probe Tests

Stage 3J adds tests for finite exponent-sequence loading, modular stream values, forward/reverse indexing, reset handling, cyclic exponent behavior, duplicate stream-signature detection, output record fields, CLI execution on synthetic input, generated-output ignore policy, and policy blocking when offsets expand without a matching candidate-count update.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python/test_stage3j_mersenne_stream_values.py tests/python/test_stage3j_mersenne_executor.py tests/python/test_stage3j_mersenne_cli.py tests/python/test_stage3j_mersenne_output.py tests/python/test_stage3j_queue.py
```

## Stage 3K Archive And Visual Registry Tests

Stage 3K adds tests for source/archive records, source-class vocabulary, noncanonical flags, synthetic image scanning, prime dimension helpers, missing-image handling, committed image lock validation, visual numeric observations, cookie/hash records, CLI commands, ignored raw images, ignored generated scan outputs, and trackable registry JSONL files.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3k
```

## Stage 3L Hash Preimage Tests

Stage 3L adds tests for cookie record loading, `hex64` validation, candidate pack validation, SHA-256-only enforcement, no-external-dictionary flags, byte variants, base29 rendering, SHA-256 known vectors, exact match detection, no fuzzy/partial matching, generated output schemas, CLI commands, ignored generated outputs, and `solve_claim=false`.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3l
```

## Stage 3M Image Analysis Tests

Stage 3M adds tests for synthetic grayscale statistics, threshold ratios, deterministic 4-connected component counts, symmetry metrics, bit-plane ratios, visual feature candidate flags, generated output schemas, CLI commands, missing-image raw-data-free mode, ignored generated outputs, ignored raw images, and `solve_claim=false`.

## Stage 3N Discord Ingestion Tests

Stage 3N adds tests for Discord ingestion schemas, synthetic HTML file locks, missing-directory
`--allow-missing` behavior, href/src/plaintext URL extraction, source-domain classification,
Discord attachment URL redaction, keyword-only method-claim extraction, numeric observation
extraction, aggregate privacy policy checks, CLI scan/validate/export commands, ignored generated
outputs, ignored raw Discord logs, and no live API or scrape requirements.

## Stage 3P Image Transform Tests

Stage 3P adds tests for transform schemas, grayscale/invert/threshold previews, RGB channel splits, bitplane previews, edge maps, split/mirror differences, component overlays, contact sheets, review index generation, visual transform candidate safety flags, CLI raw-image-free mode, ignored generated outputs, ignored raw page images, ignored raw Discord logs, and no OCR/AI/OpenCV dependency requirement.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3m
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3p
```

Stage 3A adds tests for minimal triage scoring, Caesar and affine enumeration counts, candidate output schemas, generated-output ignore policy, policy blocking, and `libreprimus bounded-run` CLI behavior.

The tests assert that scoring is deterministic, Caesar generates `29` candidates, affine generates `812` candidates, total candidate count is `841`, output indices stay in `0..28`, candidate records and run summaries validate, top-k output is bounded, CUDA stays false, solve claims stay false, and synthetic CLI runs work without raw corpus data.

## Stage 3B Inspection And Scoring Tests

Stage 3B adds tests for candidate inspection, refined triage scoring, Stage 3A reranking, reverse-direction Caesar/affine transforms, and the Stage 3B bounded queue.

The tests assert that candidate records load from JSONL, inspection summaries group by transform and score distribution, noisy candidates stay noisy, readable synthetic controls score better, tiny impossible-bigram and repeated-symbol penalties work, reranking can change top order, reverse Caesar and affine inverse formulas are correct, reverse affine produces `812` candidates, total reverse candidates remain `841`, generated outputs are ignored, and no solve claims are made.

## Stage 3C Scoring Calibration Tests

Stage 3C adds tests for positive-control loading, deterministic null controls, crib checks, calibration summaries, scoring CLI commands, and the Stage 3C bounded queue.

The tests assert that solved fixture controls load, null controls are deterministic and length-matched, negative controls remain noisy or garbage, crib hits do not imply solve claims, calibration summaries validate, confidence labels are assigned, noisy synthetic candidates stay noisy or garbage, readable synthetic controls classify as positive/plausible, generated outputs are ignored, and the next queue item stays under policy.

## Stage 3D Small Vigenere Key-List Tests

Stage 3D adds tests for exact key-list loading, key expansion rejection, Gematria key mapping, explicit-key Vigenere execution, CLI execution, output schema validation, ignored generated outputs, queue candidate counts, and policy blocking when declared keys exceed the candidate bound.

The tests assert that the Stage 3D key list remains exactly `LIBER`, `PRIMUS`, `DIVINITY`, and `CICADA`; the run produces exactly four candidates; candidate records include `key_text`, `key_indices`, calibrated confidence labels, `cuda_used=false`, and `solve_claim=false`; and generated Stage 3D outputs remain ignored.

## Stage 3E Method Backlog Tests

Stage 3E adds tests for method backlog schemas, bounded queue candidate counts, executor-support classification, dry-run CLI behavior, and no-scope-creep rules.

The tests assert that the Stage 3E/3G/3J backlog items validate, LP evidence Vigenere count is `48`, p56 local prime-minus-one offset count is `256`, historical Vigenere count is `56`, negative-control count is `100`, reset/advance ablation count is `64`, prime mod/gap count is `256`, Mersenne probe count is `192`, every item fits operator-policy limits, CUDA stays disabled, solve claims stay false, broad dictionary search and unconstrained skip masks are absent, dry-run output is ignored, and missing executors are reported instead of faked.

## Stage 3F Vigenere Key-Pack Tests

Stage 3F adds tests for the evidence-key Vigenere pack executor, CLI, generated output shape, and queue integration.

The tests assert that the LP evidence pack loads exactly 12 keys, rejects key expansion without a count update, computes `12 * 2 * 2 = 48` candidates, maps all keys through the Gematria profile, executes `none` reset, executes or explicitly defers `line` reset based on line metadata, executes or warns for `token_break_preserving` based on token-break metadata, writes key/reset/advance metadata in candidate records, keeps `cuda_used=false` and `solve_claim=false`, blocks candidate-count drift, and leaves generated outputs ignored.

## Stage 3G Prime Offset Sweep Tests

Stage 3G adds tests for deterministic prime generation, prime-minus-one stream values, offset/direction/reset candidate counts, forward and reverse stream indexing, reset-mode handling, CLI execution, generated output shape, Mersenne backlog metadata, and queue-runner integration.

The tests assert that the first ten primes are stable, the p56-local sweep computes `64 * 2 * 2 = 256` candidates, line reset executes with line metadata or defers with an explicit warning, candidate records include offset/direction/reset metadata, `cuda_used=false`, `solve_claim=false`, calibrated confidence labels are present, generated Stage 3G outputs are ignored, the Mersenne probe is promoted to Stage 3J runnable status, and offset expansion without a count update is blocked.

## Stage 3H Reset/Advance Ablation Tests

Stage 3H adds tests for the reset/advance state machine, transform adapters, family-specific negative controls, CLI execution, generated output shape, and queue policy.

The tests assert that reset `none` uses the whole sequence, reset `line` segments by line metadata, reset `word` and `clause` require metadata, missing metadata emits explicit warnings instead of fake segmentation, `runes_only` advances only transformable tokens, `token_break_preserving` preserves separators, Vigenere and prime-stream adapters work on synthetic tokens, the ablation count is `64`, executed plus deferred counts match, negative controls are deterministic, generated outputs are ignored, `cuda_used=false`, and `solve_claim=false`.

## Stage 3I Historical Vigenere Pack Tests

Stage 3I adds tests for the historical motif Vigenere key pack, generic key-pack CLI execution, generated output shape, evidence-family metadata, and queue support classification.

The tests assert that the historical pack loads exactly 14 declared keys, computes `14 * 2 * 2 = 56` candidates, maps all keys through the Gematria profile, rejects key expansion without a candidate-count update, executes reset `none`, executes or explicitly defers reset `line` based on line metadata, executes `runes_only`, executes or warns for `token_break_preserving`, writes `evidence_family=historical_motif_key_pack`, keeps `cuda_used=false`, keeps `solve_claim=false`, includes calibrated confidence labels, and leaves generated outputs ignored.

The consistency suite is raw-data-free. It validates generated result-store outputs only when they are present locally; missing generated outputs are warnings, not CI failures.

## Stage 4I Scorer Consolidation Tests

Stage 4I adds tests for scoring schemas, finite confidence labels, legacy compatibility mapping, scorer inventory records, Stage 3C calibration-profile fallback, CPU batch score-summary compatibility, CLI consolidation/validation/report commands, and ignored generated outputs.

The tests assert that score labels cannot imply solved/plaintext_verified, score summaries reject `solve_claim=true` and `cuda_used=true`, CPU batch score summaries map legacy labels through the compatibility layer, generated scoring-consolidation outputs are ignored, and raw data remains ignored.

## Stage 4J Observation Review Workflow Tests

Stage 4J adds tests for observation-review schemas, review-state transitions, promotion gates, quarantine records, path sanitisation, stale operational-document detection, CLI build/validate/check paths, and ignored output policy.

The tests assert that visual candidates without coordinates cannot promote, cuneiform readings without accepted review cannot promote, ambiguous dot readings cannot promote, Discord-derived records without public corroboration cannot promote, negative controls remain usable only as controls, scoring labels cannot become solve claims, absolute local paths are rejected unless explicitly marked as examples, generated observation-review outputs are ignored, and raw data remains ignored.
# Stage 4Q Validation

Stage 4Q validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli benchmark-planning validate-stage4q `
  --results-dir experiments/results/benchmarks/stage4q `
  --plan data/benchmarks/stage4q-cpu-benchmark-plan.yaml `
  --readiness data/benchmarks/stage4q-cuda-parity-readiness.yaml `
  --summary data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml
```

The consistency scripts also build Stage 4Q temp outputs in a raw-data-free location. Tests must not require CUDA, raw page images, raw Discord logs, stego/audio assets, generated benchmark records in Git, or `codex-output/**`.

# Stage 5A Validation

Stage 5A validation uses:

- `libreprimus cuda-planning build-target-plan`
- `libreprimus cuda-planning build-parity-scaffold`
- `libreprimus cuda-planning build-implementation-gates`
- `libreprimus cuda-planning validate-stage5a`
- `libreprimus cuda-planning summary`

The consistency scripts also build Stage 5A temp outputs in a raw-data-free location. Tests must not require CUDA, modify `.cu` or `.cuh` files, run GPU benchmarks, make speedup claims, commit generated CUDA planning reports, process raw data, or publish `codex-output/**`.

# Stage 5B Validation

Stage 5B validation uses:

- `libreprimus cuda-parity build-harness-plan`
- `libreprimus cuda-parity build-backend-capability`
- `libreprimus cuda-parity build-future-kernel-matrix`
- `libreprimus cuda-parity validate-stage5b`
- `libreprimus cuda-parity summary`

The consistency scripts also build Stage 5B temp outputs in a raw-data-free location. Tests must not require CUDA hardware, modify `.cu` or `.cuh` files, add transform kernels, run GPU benchmarks, make performance or speedup claims, commit generated CUDA parity reports, process raw data, or publish `codex-output/**`.

# Stage 5G Validation

Stage 5G validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting validate-stage5g `
  --parity-report data/cuda/stage5g-shift-score-parity-report.yaml `
  --device-code-audit data/cuda/stage5g-cuda-device-code-subset-audit.yaml `
  --preflight data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml `
  --summary data/cuda/stage5g-cuda-parity-reporting-summary.yaml `
  --results-dir experiments/results/cuda-parity-reporting/stage5g
```

The consistency scripts also build Stage 5G temp outputs in a raw-data-free, no-GPU-safe location.
Tests must not require CUDA hardware, add transform kernels, run GPU benchmarks, make speedup
claims, commit generated CUDA parity reports, process raw data, or publish `codex-output/**`.

# Stage 5H Validation

Stage 5H validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-shift-contract validate-stage5h `
  --contract data/cuda/stage5h-gematria-shift-score-contract.yaml `
  --fixtures data/cuda/stage5h-gematria-native-parity-fixtures.yaml `
  --mapping data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml `
  --score-summary-plan data/cuda/stage5h-gematria-score-summary-parity-plan.yaml `
  --summary data/cuda/stage5h-gematria-shift-contract-summary.yaml `
  --results-dir experiments/results/gematria-shift-contract/stage5h
```

The consistency scripts also build Stage 5H temp outputs in a raw-data-free, no-GPU-safe location.

# Stage 5I Validation

Stage 5I validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-prep validate-stage5i `
  --preparation data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --abi-plan data/cuda/stage5i-gematria-cuda-abi-plan.yaml `
  --validation-vectors data/cuda/stage5i-gematria-cuda-validation-vectors.yaml `
  --implementation-checklist data/cuda/stage5i-gematria-cuda-implementation-checklist.yaml `
  --summary data/cuda/stage5i-gematria-cuda-preparation-summary.yaml `
  --results-dir experiments/results/gematria-cuda-prep/stage5i
```

The consistency scripts also build Stage 5I temp outputs in a raw-data-free, no-GPU-safe location.
Tests must not require CUDA hardware, add transform kernels, run GPU benchmarks, make speedup
claims, commit generated Gematria shift reports, process raw data, or publish `codex-output/**`.

# Stage 5J Validation

Stage 5J validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-kernel validate-stage5j `
  --implementation data/cuda/stage5j-gematria-cuda-kernel-implementation.yaml `
  --build-records data/cuda/stage5j-gematria-cuda-kernel-build-records.yaml `
  --parity-records data/cuda/stage5j-gematria-cuda-synthetic-parity-records.yaml `
  --summary data/cuda/stage5j-gematria-cuda-kernel-summary.yaml `
  --results-dir experiments/results/gematria-cuda-kernel/stage5j
```

The consistency scripts also build Stage 5J temp outputs in a raw-data-free, no-GPU-safe location.
CI can skip CUDA builds, while local CUDA may record a passed build/parity run. Tests must not run
real Liber Primus data through CUDA, run GPU benchmarks, make speedup claims, commit generated
Gematria CUDA reports, process raw data, or publish `codex-output/**`.

# Stage 5K Validation

Stage 5K validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting validate-stage5k `
  --parity-report data/cuda/stage5k-gematria-cuda-parity-report.yaml `
  --device-code-audit data/cuda/stage5k-gematria-cuda-device-code-audit.yaml `
  --preflight data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml `
  --score-summary-preflight data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml `
  --summary data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml `
  --results-dir experiments/results/gematria-cuda-parity-reporting/stage5k
```

The consistency scripts also build Stage 5K temp outputs in a raw-data-free, no-GPU-safe location.
Tests must not require CUDA hardware, modify CUDA source, add kernels, run solved or unsolved page
data through CUDA, run GPU benchmarks, make speedup claims, commit generated Gematria CUDA parity
reports, process raw data, or publish `codex-output/**`.

# Stage 5L Validation

Stage 5L validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping validate-stage5l `
  --token-mapping data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml `
  --native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml `
  --output-hash-contract data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml `
  --score-summary-shape data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml `
  --summary data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-mapping/stage5l
```

The consistency scripts also build Stage 5L temp outputs in a raw-data-free, no-GPU-safe location.
Tests must not require CUDA hardware, modify CUDA source, add kernels, run solved or unsolved page
data through CUDA, run GPU benchmarks, make speedup claims, commit generated solved-fixture mapping
reports, process raw data, or publish `codex-output/**`.

# Stage 5M Validation

Stage 5M validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda validate-stage5m `
  --run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
  --parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml `
  --boundaries data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml `
  --summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-cuda/stage5m
```

The consistency scripts also build Stage 5M temp outputs in a raw-data-free, no-GPU-safe location
using `--skip-run`. Local CUDA may record the exact solved-fixture parity run when available, but CI
must not require CUDA hardware. Tests must not add kernels, change device arithmetic, run unsolved
page data through CUDA, run GPU benchmarks, make speedup claims, commit generated CUDA reports,
process raw data, or publish `codex-output/**`.

# Stage 5N Validation

Stage 5N validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting validate-stage5n `
  --parity-report data/cuda/stage5n-gematria-solved-fixture-cuda-report.yaml `
  --controlled-expansion-gate data/cuda/stage5n-gematria-controlled-expansion-gate.yaml `
  --boundary-review data/cuda/stage5n-gematria-cuda-boundary-review.yaml `
  --result-store-preflight data/cuda/stage5n-gematria-cuda-result-store-preflight.yaml `
  --no-unsolved-guardrail data/cuda/stage5n-gematria-no-unsolved-guardrail.yaml `
  --summary data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-cuda-reporting/stage5n
```

Stage 5N tests are no-GPU-safe. They must not run CUDA, add kernels, modify CUDA source, run
unsolved data, run benchmarks, make speedup claims, stage generated reports, or stage `codex-output/**`.

# Stage 5O Validation

Stage 5O validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-repeat validate-stage5o `
  --repeat-run data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml `
  --repeat-parity data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml `
  --result-store-preflight data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml `
  --score-summary-preflight data/cuda/stage5o-gematria-cuda-score-summary-preflight.yaml `
  --expansion-decision data/cuda/stage5o-gematria-cuda-expansion-decision.yaml `
  --summary data/cuda/stage5o-repeat-verification-result-store-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-cuda-repeat/stage5o
```

Stage 5O tests remain no-GPU-safe by using `--skip-run` for CI/temp paths. Local CUDA repeat
verification may run only the exact Stage 5M solved-fixture-safe buffers and must not add kernels,
modify CUDA source, run benchmarks, make speedup claims, stage generated reports, or stage
`codex-output/**`.

# Stage 5P Validation

Stage 5P validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-result-store validate-stage5p `
  --result-store-integration data/cuda/stage5p-gematria-cuda-result-store-integration.yaml `
  --score-summary-integration data/cuda/stage5p-gematria-cuda-score-summary-integration.yaml `
  --method-status-impact data/cuda/stage5p-gematria-cuda-method-status-impact.yaml `
  --generated-body-policy data/cuda/stage5p-gematria-cuda-generated-body-policy.yaml `
  --controlled-expansion-candidates data/cuda/stage5p-gematria-controlled-expansion-candidates.yaml `
  --summary data/cuda/stage5p-cuda-result-store-integration-summary.yaml
```

Stage 5P tests are no-GPU-safe. They cover schema guardrails, compact result-store records,
Stage 4I score-summary labels, method-status non-upgrade policy, generated-body publication blocks,
controlled expansion candidate records, CLI round trips, and ignored-output/codex-output safety.

# Stage 5Q Validation

Stage 5Q validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping validate-stage5q `
  --candidate-inventory data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml `
  --token-mapping data/cuda/stage5q-gematria-expansion-token-mapping.yaml `
  --native-parity data/cuda/stage5q-gematria-expansion-native-parity.yaml `
  --result-store-preflight data/cuda/stage5q-gematria-expansion-result-store-preflight.yaml `
  --expansion-gate data/cuda/stage5q-gematria-expansion-gate.yaml `
  --summary data/cuda/stage5q-expansion-candidate-mapping-summary.yaml
```

Stage 5Q tests are no-GPU-safe. They cover schema guardrails, exact Stage 5L/5M/5O duplicate
exclusion, direct-translation token mappings, blocked original-family fixtures, native parity
hashes, Stage 4P/Stage 4I preflight, controlled Stage 5R gate selection, CLI round trips, and
ignored output policy.

# Stage 5R Validation

Stage 5R validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-solved-fixture-cuda validate-stage5r `
  --run-records data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml `
  --parity-records data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml `
  --boundaries data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml `
  --result-store-preflight data/cuda/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml `
  --score-summary-preflight data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml `
  --summary data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml `
  --results-dir experiments/results/gematria-expanded-solved-fixture-cuda/stage5r
```

Stage 5R tests are no-GPU-safe. They cover schema guardrails, exact Stage 5Q candidate scope,
consumed-control and original-family exclusion, skipped-CUDA false-pass prevention, CUDA/native
hash equality requirements, Stage 4P and Stage 4I preflight records, boundary guardrails, CLI
round trips through `--skip-run`, ignored output policy, and deterministic next-stage decisions.

# Stage 5S Validation

Stage 5S validation uses:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-cuda-result-store validate-stage5s `
  --parity-report data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml `
  --result-store-integration data/cuda/stage5s-gematria-expanded-cuda-result-store-integration.yaml `
  --score-summary-integration data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml `
  --method-status-impact data/cuda/stage5s-gematria-expanded-cuda-method-status-impact.yaml `
  --generated-body-policy data/cuda/stage5s-gematria-expanded-cuda-generated-body-policy.yaml `
  --boundary-review data/cuda/stage5s-gematria-expanded-cuda-boundary-review.yaml `
  --next-step-decision data/cuda/stage5s-gematria-expanded-cuda-next-step-decision.yaml `
  --summary data/cuda/stage5s-expanded-cuda-result-store-integration-summary.yaml `
  --results-dir experiments/results/gematria-expanded-cuda-result-store/stage5s
```

Stage 5S tests are no-GPU-safe. They cover schema guardrails, exact three-record integration,
Stage 4P/Stage 4I compatibility, generated-body policy, method-status non-upgrade rules,
boundary review, deterministic Deep Research next-step selection, CLI round trips, and ignore
policy for generated reports, raw data, SQLite, and `codex-output/`.

Stage 5BU extends coverage with lineage-path erratum schemas, preserved active-lineage digest validation, Stage 5BS validator hardening, reviewability metadata checks, gate preservation checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bu/` and `codex-output/**`. It confirms the deprecated Stage 5AW preserved path is absent, the corrected path resolves, String 4 active input remains false, dry-run ingestion remains false, Stage 5BD records remain valid, and no token experiments, byte-stream generation, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5BW extends coverage with inactive-sidecar proposal schemas, manifest-supersession preflight validation, no-active-ingestion checks, active-lineage preservation checks, future-runner citation requirements, reviewability metadata checks, guardrail checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5bw/` and `codex-output/**`. It confirms Stage 5BV verdict `accept_with_warnings` is integrated, String 4 sidecar planning ingestion is proposed but inactive, manifest supersession is preflight-only, Stage 5AP/5AW/5AY/5AZ/5BB/5BD paths resolve, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5BY extends coverage with inactive planning-manifest scaffold schemas, no-execution sidecar validation, source-digest unique-path validation, Stage 5BW duplicate-row classification checks, record-family filename-equivalence checks, no-active-ingestion/no-byte-stream guardrails, Stage 5BD run-plan preservation checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5by/` and `codex-output/**`. It confirms Stage 5BX verdict `accept_with_warnings` is integrated, the Stage 5BY digest index has unique paths, String 4 remains inactive, manifest supersession is false, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5CA extends coverage with inactive-sidecar review contract schemas, exact future-runner citation-set validation, fail-closed trigger validation, activation-precondition validation, deterministic manifest-supersession preflight validation, sidecar gate checks, Stage 5BD run-plan preservation checks, active-lineage preservation checks, reviewability metadata checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5ca/` and `codex-output/**`. It confirms Stage 5BZ verdict `accept_with_warnings` is integrated, String 4 remains inactive, active input and dry-run ingestion stay false, manifest supersession is false, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5CC extends coverage with active-planning-input proposal preflight schemas, Stage 5CB findings integration, Stage 5CA exact-citation preservation, 17-item fail-closed trigger exact-set validation, 12-item activation-precondition exact-set validation, extension-policy non-gate-opening checks, active-planning-input no-authorization checks, no-byte-stream/no-execution transition-gate validation, sidecar gate checks, Stage 5BD run-plan preservation checks, active-lineage preservation checks, reviewability metadata checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5cc/` and `codex-output/**`. It confirms String 4 remains inactive, active input and dry-run ingestion stay false, active-planning input is not authorized, manifest supersession is false, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5CG extends coverage with post-review approval-gate integration schemas, Stage 5CF findings integration, Stage 5CE proposal/gate preservation, operator approval and Deep Research acceptance decision-scaffold validators, combined approval-gate non-satisfaction checks, Stage 5CE wording-review validation, no-byte-stream transition-gate validation, no-execution transition-gate validation, Stage 5BD run-plan preservation checks, active-lineage preservation checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5cg/` and `codex-output/**`. It confirms active planning input remains unselected and unauthorized, operator and Deep Research approval remain unsatisfied, String 4 active input and dry-run ingestion stay false, manifest supersession is false, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5CI extends coverage with approval-record template hardening schemas, Stage 5CH findings integration, Stage 5CG scaffold preservation, future operator approval and Deep Research acceptance template validators, combined approval-gate validation and non-satisfaction checks, activation-decision template validation, negative validation contracts, no-byte-stream transition-gate validation, no-execution transition-gate validation, Stage 5BD run-plan preservation checks, active-lineage preservation checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5ci/` and `codex-output/**`. It confirms templates are not approvals, the combined gate remains unsatisfied, activation is invalid now, active planning input remains unselected and unauthorized, String 4 active input and dry-run ingestion stay false, manifest supersession is false, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5CK extends coverage with approval-record validation fixture-pack schemas, Stage 5CJ findings integration, Stage 5CI template preservation, operator approval fixture validators, Deep Research acceptance fixture validators, activation-decision fixture validators, negative-validation matrix checks, activation-decision review-package checks, combined approval-gate non-satisfaction checks, no-byte-stream/no-execution transition-gate validation, Stage 5BD run-plan preservation checks, active-lineage preservation checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5ck/` and `codex-output/**`. It confirms fixture records are not actual approvals, the combined gate remains unsatisfied, activation is invalid now, active planning input remains unselected and unauthorized, String 4 active input and dry-run ingestion stay false, manifest supersession is false, Stage 5BD run-plan ID count stays `10`, byte-stream and execution flags remain false, and no token experiments, DWH/hash/preimage search, decode, stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, public website expansion, method-status upgrade, or solve claim ran.

Stage 5CM extends coverage with approval-readiness boundary schemas, Stage 5CL findings integration, Stage 5CK fixture preservation, fixture/template/scaffold/review-package versus real-record negative cases, end-to-end readiness-boundary validation, future real approval-readiness preflight checks, activation-decision gate hardening, credential-redaction/no-secret policy validation, sidecar-gate checks, Stage 5BD run-plan preservation checks, active-lineage preservation checks, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5cm/` and `codex-output/**`. It confirms no actual approval, Deep Research activation acceptance, activation decision, combined gate satisfaction, activation authorization, active-planning input authorization/selection, String 4 activation, byte-stream generation, execution, scoring, CUDA, benchmark, method-status upgrade, or solve claim occurred, and Stage 5CM-and-later local parallel validation is capped at `8` workers.

Stage 5CO extends coverage with real approval-record readiness package schemas, Stage 5CN findings integration, real operator approval readiness preflight, real Deep Research acceptance readiness preflight, real combined-gate readiness preflight, activation-decision transition planning, future transition sequence checks, current missing-requirements checks, real-record blocker checks, Stage 5CM boundary preservation, Stage 5CK/5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, credential-redaction preservation, review-packaging warning checks, no-active/no-byte/no-execution transition gates, CLI validation paths, and ignored-output checks for `experiments/results/token-block/stage5co/` and `codex-output/**`. It confirms no real approval records, Deep Research acceptance records, combined-gate satisfaction, valid activation decision, active-planning input authorization/selection, String 4 activation, byte-stream generation, execution, scoring, CUDA, benchmark, website expansion, method-status upgrade, or solve claim occurred, and Stage 5CO preserves the `8` worker cap for local validation.
