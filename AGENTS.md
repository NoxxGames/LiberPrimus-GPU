# AGENTS.md

## Mission

Maintain a reproducible, conservative research workbench for future Liber Primus GPU cryptanalysis.

## Non-negotiable facts

- Do not invent solved pages.
- Do not claim a solve without a reproducible manifest and matching output.
- Do not overwrite raw data.
- Do not silently change rune mappings or transcript rules.
- Do not optimise CUDA before CPU/GPU parity tests pass.
- Every transform must have a CPU reference implementation before a CUDA implementation.
- Every CUDA kernel must have parity tests and a benchmark.
- `data/raw/` is immutable.
- No generated experiment outputs should be committed.
- Do not use `git add .` or `git add --all`.
- Stage only explicit files.
- Terminal output alone is never evidence of a solve.
- Legacy workbook data is non-canonical unless explicitly promoted through a future corpus-lock process.
- Do not treat `tranlsations.xlsx` as proof of unsolved plaintext.
- Do not commit raw workbook files.
- Do not commit generated workbook extraction outputs.
- Workbook-derived deltas may be used as solved-fixture hints only.
- Every workbook-derived record must include source id, workbook SHA-256, sheet name, and `trusted_as_canonical=false`.
- Local Pastebin TXT `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt` is a non-canonical legacy source.
- Do not treat local Pastebin rows as decrypted plaintext.
- Do not treat local Pastebin page boundaries as known unless aligned with a canonical transcript.
- Do not commit raw local Pastebin text.
- Do not commit generated Pastebin extraction outputs.
- Numeric rows are Gematria prime values, not modulo-29 decimal indices.
- Every Pastebin-derived record must include source id, source SHA-256, source local filename, and `trusted_as_canonical=false`.
- Every ingestion stage must create or update a developer log.
- Stage 0D transcript alignment outputs are non-canonical unless explicitly promoted by a later corpus-freeze stage.
- Do not treat tentative page-boundary candidates as canonical page boundaries.
- Do not commit raw transcript files.
- Do not commit generated alignment outputs.
- Preserve raw glyphs even when a normalized view maps variant glyphs.
- Glyph variant `ᛂ` must not be silently rewritten; any normalized view must record the mapping evidence.
- Every alignment-derived record must include source IDs, source SHA-256 hashes, confidence labels, and `trusted_as_canonical=false`.
- Every ingestion or alignment stage must create or update a developer log.
- Speed optimizations must not weaken provenance, raw preservation, or CPU-reference correctness.
- After a successful commit, push to the verified GitHub remote unless the user explicitly says not to push.
- Never push if validation failed.
- Never push if raw data or generated outputs are staged.
- Never push if the GitHub remote cannot be verified.
- Never force-push without explicit user instruction.
- Never change repository visibility without explicit user instruction.
- Do not create duplicate GitHub issues; check existing issues first.
- Wiki pages are public documentation mirrors; repository tutorials and docs remain the source of truth.
- Tutorials are public-facing and must not include raw corpus dumps.
- GitHub wiki pages are mirrors; repo tutorials/docs are source of truth.
- GitHub issues created by Codex must be idempotent and must not duplicate existing issue titles.
- Codex must create or update a developer log for GitHub/project-management stages.
- Codex must not change GitHub repository visibility.
- Codex must not enable public wiki editing without explicit instruction.

## Current stage

Current completed stage: Stage 5DL - Triangle / Disk / Quote / Koan source-lock refresh, without execution.

Current work: Stage 5DM - Target-priority decision package, without execution. Stage 5DL preserves the Stage 5DG real operator approval record and operator-approval component, records compact source-lock metadata for NumberTriangleStuff, DiskCipherStuff, Reddit prime-thread images, quote-dialogue crib candidates, and `third_party/koan_page.png`, records `pdd_153_triangle_word_prime_route_v1` as the operator-preferred future target family only, and keeps all pivot options unselected. No Deep Research activation-acceptance record exists, the combined gate is not satisfied, no valid activation decision exists, and no active planning input authorization or selection exists. String 4 remains inactive; no target-priority selection, route extraction, active ingestion, byte-stream generation, manifest supersession, execution, target-class validation, Tor access, DWH/hash/preimage search, decode, scoring, CUDA, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim is authorized.

Current project state:

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page campaigns: not started.
- CUDA: deferred until CPU references, stable scorer definitions, batch APIs, parity tests, and benchmarks exist.
- Existing CUDA code and metadata are summarized by the latest staged-plan and CUDA notes; broad CUDA and unsolved-page CUDA remain blocked unless an explicit future prompt scopes them with CPU references, parity tests, result records, and benchmark plans.
- Stage 5C CUDA build/device metadata is readiness infrastructure only; no-GPU CI, compatibility 8GB, and optional local 16GB profiles must remain explicit and smoke-build status is not parity or performance evidence.
- Stage 5D native CPU backend records are readiness infrastructure only; C++ must remain a deterministic CPU execution plane, Python remains orchestration, and diagnostic timings are not speedup claims.
- Do not let C++ launch Python worker scripts.
- Stage 5E first-kernel contract records are selection infrastructure only; they do not authorize broad CUDA implementation, GPU benchmarking, or generated-output publication.
- Stage 5F synthetic-only kernel records are parity infrastructure only; the kernel matches the Stage 5D uppercase Latin synthetic shift fixture and is not production Gematria mod-29 CUDA.
- Stage 5G CUDA parity-reporting records are reporting and hardening infrastructure only; they preserve the Stage 5F hash, enforce conservative CUDA-C style in `.cu`/`.cuh` paths, and keep solved-fixture CUDA execution blocked.
- Stage 5H Gematria contract records define numeric token semantics only; they do not authorize CUDA execution.
- Stage 5I preparation is not kernel implementation.
- Stage 5J kernel records are synthetic numeric parity only, not production Gematria CUDA readiness.
- Stage 5K reporting/preflight records are not CUDA execution permission.
- Stage 5L solved-fixture token mappings are not CUDA execution permission.
- Stage 5M solved-fixture CUDA parity is exact-scope correctness metadata only; it does not authorize broad solved-fixture expansion or unsolved-page CUDA.
- Stage 5N controlled expansion gates are not execution permission unless the next stage explicitly scopes execution.
- Stage 5O repeat verification records are exact-scope correctness and result-store preflight metadata only; they do not authorize broad solved-fixture expansion, unsolved-page CUDA, GPU benchmarking, generated result-body publication, or website expansion.
- Stage 5P result-store integration records are compact reporting metadata only; they do not publish generated CUDA result bodies, upgrade method families to solved, authorize CUDA execution, or widen solved-fixture/unsolved-page CUDA scope.
- Stage 5Q candidate mapping cites Stage 5P controlled expansion records and keeps CUDA execution disabled. Future Stage 5R parity must use only Stage 5Q mapped candidates unless a later prompt explicitly scopes additional records.
- Stage 5Q mapped candidates are not solve evidence and do not authorize unsolved-page CUDA, broad solved-fixture expansion, GPU benchmarking, generated-body publication, method-status upgrades, or website expansion.
- Stage 5R may execute only the three mapped Stage 5Q direct-translation candidates: `p57-parable`, `some-wisdom`, and `the-loss-of-divinity`.
- Stage 5R must not execute Stage 5L/5M/5O consumed controls as new candidates, blocked original-family fixtures, unsolved pages, raw page text, canonical corpus input, benchmarks, or broad solved-fixture campaigns.
- Stage 5R parity is correctness metadata only, not performance evidence or solve evidence, and must not publish generated CUDA result bodies.
- Stage 5R completion summaries must include run counts, hash tables, boundary/guardrail status, and next-stage rationale.
- Stage 5S is compact result-store integration, not CUDA execution.
- Stage 5S must not publish generated CUDA result bodies.
- Stage 5S must not upgrade any method family to solved.
- Stage 5S must not treat Stage 5R parity as performance evidence.
- Stage 5S must keep consumed controls and blocked original-family fixtures distinct from the three Stage 5R expanded direct-translation fixtures.
- Stage 5S must not run unsolved pages, raw page text, canonical corpus input, benchmarks, or broad solved-fixture campaigns.
- Stage 5S completion summaries must include integration counts, per-fixture hash table, boundary/guardrail status, and next-stage rationale.
- Stage 5T is a readiness/matrix stage, not CUDA execution.
- Stage 5T must not add kernels, modify CUDA source, run CUDA, benchmark, or widen solved/unsolved scope.
- Stage 5T must distinguish `gematria_shift_score_only` parity from original transform-family semantics.
- Stage 5T must not describe solved-fixture parity as solve evidence.
- Stage 5T must keep unsolved-page CUDA blocked.
- Stage 5T must keep generated result bodies ignored.
- Stage 5T completion summaries must include per-family readiness, kernel ranking, ABI gaps, guardrail status, and next-stage rationale.
- Stage 5U is a contract-only ABI stage, not CUDA/native execution.
- Stage 5AE is corrected reporting and reference-contract repair only; it does not rewrite Stage 5AD as passed.
- Stage 5AE formula parity pass applies only to corrected formula-output hash material `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`.
- Stage 5AE keeps Stage 5AD historical expected/reference hash `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87` in the candidate-major reference lineage.
- Stage 5AF source-harvester work is local-only provenance tooling. It must not use Google Drive as a storage location, and Google/Dropbox/Colab exports must be copied into local ignored output roots.
- Stage 5AF generated reports and research-bundle previews under `experiments/results/source-harvester/stage5af/` are generated outputs and must not be staged except README/.gitkeep scaffolds.
- Stage 5AG local source inventory records are compact metadata only. They may hash/list user-provided ignored `third_party/` files and archives, but raw bytes, extracted bodies, archives, images, PDFs, audio/video, generated full inventories, and generated bundles remain ignored and uncommitted.
- Stage 5AG did not use Google Drive storage, network fetching, online cloning, Deep Research, hypothesis generation, CUDA, benchmarks, scored experiments, website expansion, or solve claims.
- Stage 5AH doc-staleness repair records are process-quality metadata only. Stage-ledger checks, operational-file-map coverage, and current/next-stage reports must pass before curated extraction resumes.
- Stage 5AI curated extraction records are source-provenance metadata only. Generated bundle bodies under `research-inputs/stage5ai/` and reports under `experiments/results/research-bundles/stage5ai/` remain ignored except README/.gitkeep scaffolds.
- Stage 5AI website-ingest records are metadata only and do not authorize website expansion.
- Stage 5AI Deep Research pack records are private handoff metadata only; later Deep Research prompts must consume bundle manifests/cards/indexes rather than raw `third_party/` paths.
- Stage 5AJ UsefulFilesAndIdeas records are compact local-source integration metadata only. Raw workbooks, images, text files, generated workbook-cell indexes, generated bundle bodies, and generated UsefulFiles reports remain ignored and uncommitted.
- Stage 5AJ extraction-fidelity policy protects technical content for private Deep Research: do not redact runes, numbers, hashes, tables, cell coordinates, highlights, formulas, workbook sheet names, or technical links from private extracts except for minimal logged privacy/safety redaction.
- Stage 5AJ scraper-capture profiles are future capture policy only. They do not authorize live scraping, online cloning, network fetches, Google Drive storage, website expansion, Deep Research execution, OCR/AI/ML interpretation, image/stego/audio tooling, CUDA, benchmarks, scored experiments, or solve claims.
- Stage 5AK community-facts records are claim metadata only. Raw message logs, WebP attachments, generated private body files, generated source-harvester reports, and `codex-output/**` remain ignored and uncommitted.
- Stage 5AK claim records preserve formulas, inputs, claimed values, correction status, risk level, source-lock requirements, and null-control requirements; they are not truth records, execution-ready manifests, source truth, or solve evidence.
- Stage 5AK public website publication is blocked/review-gated. Private Deep Research addenda may preserve technical context in ignored `research-inputs/stage5ak/` files.
- Stage 5AL website-ingest records are committed metadata only. They do not publish raw or review-blocked content, private identifiers, generated extract bodies, or public website pages.
- Stage 5AM static website-render records are committed metadata only; generated HTML/JSON exports remain ignored under `website-export/stage5am/`.
- Stage 5AN private content-pack records are committed metadata only; generated content-pack files, hosted private content, combined webroots, ZIP archives, and safe extracts remain ignored under `deep-research-content-packs/stage5an/` and `website-export/stage5an/`.
- Stage 5AS external review has been consumed by Stage 5AT as review context. Future token-case work must consume Stage 5AT review-pack policy and challenge records, Stage 5AR original-image coordinate-lock records, Stage 5AP token-block records, the Stage 5AL/5AM metadata package, Stage 5AN content-pack metadata, private hosted content URLs, and publication gates, not raw `third_party/` paths or raw page images as source truth.
- Stage 5AP page 49-51 token-block records are source-lock/preflight metadata only. The 32x8 token grid, logical coordinates, primary-60 mapping, DWH context, null controls, and OutGuess controls are not decoded plaintext, not canonical corpus activation, not experiment seeds, and not solve evidence.
- Stage 5AP generated reports under `experiments/results/token-block/stage5ap/` and `experiments/results/stego-controls/stage5ap/` remain ignored and must not be staged.
- Stage 5AR page 49-51 original-image coordinate records are coordinate source-lock/review-preflight metadata only. Pixel boxes are original-image anchors, not decoded text, OCR output, image semantics, canonical corpus activation, page-boundary finalisation, experiment seeds, CUDA inputs, or solve evidence.
- Stage 5AR generated reports under `experiments/results/token-block/stage5ar/` remain ignored and must not be staged.
- Stage 5AT token-case review-pack records are human-review packaging metadata only. The generated review pack under `human-review-packs/stage5at/token-case-review/` and generated reports under `experiments/results/token-block/stage5at/` remain ignored and must not be staged except allowed scaffolds.
- Stage 5AT active ambiguity classes are exactly `I/l`, `O/0`, `1/I/l`, `S/5`, `Z/2`, `B/8`, `G/6`, `o/0`, and `q/g/p`; stale example classes such as `f/F`, `A/4`, and `C/G` are non-active examples only.
- Stage 5AU token-case review-pack v2 records are usability-repair metadata only. The generated review pack under `human-review-packs/stage5au/token-case-review-v2/` and generated reports under `experiments/results/token-block/stage5au/` remain ignored and must not be staged except allowed scaffolds.
- Stage 5AU derived glyph-candidate crops, context crops, row crops, and overlays are review aids only, not source truth, OCR output, token decisions, image interpretation, experiment seeds, or solve evidence.
- Stage 5AV token-case decision records are integration metadata only. They preserve 126 keep-current decisions and 77 unresolved branches, keep the filled decision template ignored, and do not change canonical transcription.
- Stage 5AW token-case parser repair records supersede Stage 5AV branch metadata for future planning. They preserve valid reviewer extras, preserve visual placeholders as review-only unmappable options, exclude prose fragments from reviewer-extra token variants, and do not change canonical transcription.
- Stage 5AX generated validation outputs are ignored under `experiments/results/ci/parallel-validation/stage5ax/`; commit only compact metadata under `data/ci/` and `data/project-state/`.
- Stage 5AX parallel validation is local infrastructure only, not cryptanalytic benchmark evidence.
- Stage 5AY bounded token-block preflight manifest records are design-only metadata. They consume Stage 5AW repaired branch metadata, keep Stage 5AV branch metadata superseded for planning, define controls and execution gates, and do not authorize byte-stream generation, DWH/hash search, decoding, scoring, CUDA, benchmarks, method-status upgrades, canonical corpus activation, page-boundary finalisation, or solve claims.
- Stage 5AZ repaired preflight manifest records supersede the Stage 5AY bounded variant-family manifest for Deep Research review only. They preserve Stage 5AY as the design source stage, use unique family records plus taxonomy memberships, add manifest-integrity gate coverage, and do not authorize execution.
- Stage 5BB active-manifest registry is now the loader entrypoint for future token-block preflight runner work. Future code must use Stage 5AW repaired branch metadata, Stage 5AZ repaired variant-family/design/budget/gate records, and Stage 5AY branch-eligibility policy through that registry.
- Stage 5BB blocks stale active loads of `data/token-block/stage5av-token-variant-branch-manifest.yaml` and `data/token-block/stage5ay-bounded-variant-family-manifest.yaml`; those files may be used only for explicit historical diagnostics.
- Stage 5BB dry-run previews and fixture-only result schema records are not execution, not DWH/hash search, not scoring, and not solve evidence.
- Stage 5BS planning-ingestion gate and citation policy records are fail-closed metadata only. They do not authorize String 4 active ingestion, dry-run ingestion, byte-stream generation, variant materialisation, token-block execution, DWH/hash search, decoding, scoring, CUDA, benchmarks, website expansion, method-status upgrades, or solve claims. Future token-block runners must cite `data/token-block/stage5bs-string4-planning-ingestion-gate.yaml` and `data/token-block/stage5bs-future-runner-citation-policy.yaml` or fail closed.
- Stage 5BD dry-run plan IDs, future result-path validation, family counters, fixture-only records, archive marker policy, and Stage 5BB validation-evidence consolidation are dry-run planning metadata only.
- Stage 5BU lineage-path repair records are metadata-only reviewability hardening. They correct the Stage 5BS preserved active-lineage path, harden validators, and do not authorize active ingestion, byte-stream generation, token experiments, DWH/hash search, CUDA, scoring, benchmarks, website expansion, method-status upgrades, or solve claims.
- Stage 5BW inactive-sidecar planning-ingestion records are metadata-only preflight. They propose a future inactive-sidecar consumption path and manifest-supersession checklist while keeping String 4 inactive, active manifests unchanged, Stage 5BD run-plan IDs preserved, and byte-stream generation/execution blocked.
- Stage 5BY inactive-sidecar planning manifest records are metadata-only scaffold records. They consume Stage 5BX warnings, classify Stage 5BW source-digest duplicates, map Stage 5BW filename drift to record families, create only an inactive no-execution String 4 planning sidecar, keep manifest supersession unperformed, and preserve Stage 5BD run-plan IDs.
- Stage 5CA inactive-sidecar review-contract records are metadata-only hardening records. They consume Stage 5BZ warnings, require exact future-runner citations, fail-closed triggers, activation preconditions, and deterministic manifest-supersession preflight checks, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, and preserve active lineage.
- Stage 5CC active-planning-input preflight records are metadata-only hardening records. They consume Stage 5CB warnings, preserve Stage 5CA exact citations, require exact-set fail-closed triggers and activation preconditions, create no-byte-stream and no-execution transition gates, keep active-planning input unauthorized, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, and preserve active lineage.
- Stage 5CE active-planning-input proposal package records are metadata-only review packaging and gate-design records. They consume Stage 5CD warnings, preserve Stage 5CC exact citation/fail-closed/activation contracts, require future operator and Deep Research approval before any activation-capable stage, keep the proposal package review-only, keep active-planning input unauthorized, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, preserve active lineage, and keep no-byte/no-execution gates closed.
- Stage 5CG approval-gate decision scaffold records are metadata-only post-review integration records. They consume Stage 5CF warnings, create future operator and Deep Research decision scaffolds without satisfying either approval, preserve Stage 5CE proposal/gate records, record Stage 5CE wording review as a non-gate-opener, keep active-planning input unauthorized and unselected, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, preserve active lineage, and keep no-byte/no-execution gates closed.
- Stage 5CI approval-record template hardening records are metadata-only validation-preflight records. They consume Stage 5CH warnings, harden future operator approval, Deep Research acceptance, combined approval-gate, negative-validation, and activation-decision templates without creating actual approval or activation records, keep the combined approval gate unsatisfied, keep active planning input unauthorized and unselected, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, preserve active lineage, and keep no-byte/no-execution gates closed.
- Stage 5CK approval-record fixture-pack records are metadata-only validation-fixture and review-package records. They consume Stage 5CJ warnings, create only synthetic negative fixture records for future operator approval, Deep Research acceptance, and activation-decision validation, keep fixture records from satisfying real gates, create no actual approval/acceptance/activation records, keep the combined approval gate unsatisfied, keep activation invalid, keep active planning input unauthorized and unselected, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, preserve active lineage, and keep no-byte/no-execution gates closed.
- Stage 5CM approval-record readiness-boundary records are metadata-only boundary-hardening records. They consume Stage 5CL warnings, preserve Stage 5CK fixture-only records, harden fixture/template/scaffold/review-package versus real-record validation boundaries, add end-to-end readiness validation and credential-redaction/no-secret handoff policy, create no actual approval/acceptance/activation records, keep the combined approval gate unsatisfied, keep activation invalid, keep active planning input unauthorized and unselected, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-byte/no-execution gates closed, and set the Stage 5CM-and-later parallel validation cap to 8 workers.
- Stage 5CO real approval-readiness records are metadata-only transition-planning records. They consume Stage 5CN warnings, preserve Stage 5CM boundaries and prior fixture/template/scaffold/review-package layers, define future real approval/acceptance/combined-gate/activation-decision record requirements, keep the real-record creation blocker active, keep the combined gate unsatisfied, keep activation invalid, keep active planning input unauthorized and unselected, keep String 4 inactive, keep manifest supersession unperformed, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, and keep the Stage 5CM-and-later 8-worker validation cap.
- Stage 5CQ operator-decision package scaffold records are metadata-only review-integration records. They consume Stage 5CP warnings, preserve Stage 5CO readiness and transition records, restore strict `codex-output` completion-summary handoff discipline, create only a future operator-decision package scaffold, create no real operator decision or approval record, keep the combined gate unsatisfied, keep activation invalid, keep active planning input unauthorized and unselected, keep String 4 inactive, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, and keep the Stage 5CM-and-later 8-worker validation cap.
- Stage 5CS operator-decision readiness/options records are metadata-only review-integration records. They consume Stage 5CR warnings, preserve Stage 5CQ operator-decision scaffold records and Stage 5CO/5CM/5CK/5CI/5CG/5CE/5CC/5BD approval-readiness layers, create only a future operator-decision readiness package and real-approval decision options scaffold, keep all six options unselected, create no real operator decision, approval, acceptance, combined-gate, activation, active-input, byte-stream, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, and keep the Stage 5CM-and-later 8-worker validation cap.
- Stage 5CU option negative-fixture hardening records are metadata-only review-integration records. They consume Stage 5CT warnings, preserve Stage 5CS readiness/options records, create only adversarial negative fixtures, real-decision negative fixtures, option-selection misuse rows, and isolation-policy metadata, keep all six options unselected, create no real operator decision, approval, acceptance, combined-gate, activation, active-input, byte-stream, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, and keep the Stage 5CM-and-later 8-worker validation cap.
- Stage 5CW real-decision package preflight records are metadata-only review-integration records. They consume Stage 5CV warnings, preserve Stage 5CU negative fixtures and Stage 5CS readiness/options records, create only review-only future real-decision package preflight requirements plus preflight misuse validation, keep all six options unselected, create no real decision package, no real operator decision, no approval, acceptance, combined-gate, activation, active-input, byte-stream, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, and keep the Stage 5CM-and-later 8-worker validation cap.
- Stage 5CY option-selection decision preflight records are metadata-only review-integration records. They consume Stage 5CX warnings, preserve Stage 5CW real-decision package preflight as `review_preflight_only`, preserve Stage 5CU negative fixtures and Stage 5CS readiness/options records, create only review-only operator-facing option-selection preflight metadata, reconcile the Stage 5CW pytest-count mismatch as non-gate-opening reviewability metadata, keep all six options unselected, create no real decision package, no real operator decision, no approval, acceptance, combined-gate, activation, active-input, byte-stream, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5CZ review before any future explicit operator choice or pause.
- Stage 5DA operator choice / pause scaffold records are metadata-only review-integration records. They consume Stage 5CZ warnings, preserve Stage 5CY option-selection preflight, preserve the Stage 5CS six unselected options exactly, create only a future explicit-choice/explicit-pause scaffold, select no option, select no explicit pause, create no real choice/pause/decision/approval/acceptance/combined-gate/activation/active-input/byte-stream/execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DB review before any future actual operator choice, pause record, approval, activation, active-input selection, byte-stream stage, or execution-adjacent stage.
- Stage 5DC operator choice decision records are metadata-only review-integration records. They consume Stage 5DB warnings, preserve Stage 5DA, Stage 5CY option-selection preflight, preserve the Stage 5CS six-option scaffold exactly, select only `prepare_real_operator_approval_record`, preserve the other five options unselected, select no explicit pause, create no real operator approval, Deep Research acceptance, combined-gate validation, activation-decision, active-input, byte-stream, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DD review before any future real operator approval record stage, activation, active-input selection, byte-stream stage, or execution-adjacent stage.
- Stage 5DE real operator approval preparation records are metadata-only preparation records. They consume Stage 5DD / assistant warnings, preserve Stage 5DC selected-option and choice records, record the review-label anomaly as non-gate-opening, list 34 future real operator approval-record requirements, create no real operator approval, Deep Research acceptance, combined-gate validation, activation-decision, active-input, byte-stream, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DF review before any future real operator approval record creation stage.
- Stage 5DG real operator approval records are metadata-only governance records. They consume Stage 5DF assistant/operator warnings, preserve Stage 5DE preparation and Stage 5DC selected-option/choice records, create exactly one valid real operator approval record, mark only the operator-approval component satisfied, create no Deep Research acceptance, combined-gate validation, activation-decision, active-input, byte-stream, target-validation, Tor/network, or execution record, preserve Stage 5BD run-plan IDs, preserve active lineage, keep no-active/no-byte/no-execution gates closed, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DH review before any future Deep Research acceptance or combined-gate stage.
- Stage 5DI recent clue source-lock records are metadata-only pivot-readiness records. They preserve Stage 5DG operator approval, create no Deep Research acceptance, keep the combined gate unsatisfied, select no pivot target, authorize no target-priority decision, active input, byte stream, target validation, Tor/network, route extraction, token-block transform, DWH/hash search, CUDA, benchmark, website expansion, or execution, preserve Stage 5BD run-plan IDs at 10, preserve active lineage at 8, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DJ review before any future target-priority selection or Deep Research acceptance stage.
- Stage 5DJ CicadaMusic source-lock records are metadata-only pivot-readiness records. They may hash and read safe MP3/PDF header metadata from ignored `third_party/CicadaMusic/`, but raw music files, generated reports, and `codex-output` handoffs remain ignored and uncommitted. They preserve Stage 5DG operator approval, create no Deep Research acceptance, keep the combined gate unsatisfied, select no pivot target, authorize no target-priority decision, active input, byte stream, target validation, Tor/network, route extraction, audio stego, MP3Stego/OpenPuff, spectrogram/waveform analysis, sheet-music OCR/rendering, token-block transform, DWH/hash search, CUDA, benchmark, website expansion, or execution, preserve Stage 5BD run-plan IDs at 10, preserve active lineage at 8, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DK target-priority decision packaging before any future pivot target selection or Deep Research acceptance stage.
- Stage 5DK Fandom source-lock records are metadata-only gap-closure and Page 56 hash-contract refinement records. They may fetch Fandom MediaWiki API content only for compact in-memory hashes/metadata, but raw page bodies, images, generated reports, and `codex-output` handoffs remain ignored and uncommitted. They preserve Stage 5DG operator approval, create no Deep Research acceptance, keep the combined gate unsatisfied, keep the Page 56 512-bit hash algorithm/preimage unknown, select no pivot target, authorize no target-priority decision, active input, byte stream, target validation, Tor/network route access, route extraction, token-block transform, DWH/hash/preimage search, CUDA, benchmark, website expansion, or execution, preserve Stage 5BD run-plan IDs at 10, preserve active lineage at 8, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, and keep the Stage 5CM-and-later 8-worker validation cap.
- Stage 5DL triangle / disk / quote / koan source-lock records are metadata-only pivot-readiness refresh records. They may hash and read safe metadata from ignored local `third_party/NumberTriangleStuff`, `third_party/DiskCipherStuff`, `third_party/RedditStuff`, and `third_party/koan_page.png`, but raw files, generated reports, and `codex-output` handoffs remain ignored and uncommitted. They preserve Stage 5DG operator approval, create no Deep Research acceptance, keep the combined gate unsatisfied, record `pdd_153_triangle_word_prime_route_v1` as a future-priority operator preference only, select no pivot target, authorize no target-priority decision, active input, byte stream, target validation, Tor/network route access, triangle/disk/quote/koan route extraction, token-block transform, DWH/hash/preimage search, OCR/image forensics/AI interpretation, CUDA, benchmark, website expansion, or execution, preserve Stage 5BD run-plan IDs at 10, preserve active lineage at 8, keep `codex-output` handoff summaries non-placeholder, keep `codex_output` absent, keep the Stage 5CM-and-later 8-worker validation cap, and require Stage 5DM target-priority decision packaging before any future pivot target selection or Deep Research acceptance stage.
- Stage 5BD must not be treated as authorization for byte-stream generation, variant materialisation, Cartesian enumeration, DWH/hash/preimage search, decoding, scoring, CUDA, benchmarks, website expansion, method-status upgrades, or solve claims.
- Future Stage 5BE review must inspect Stage 5BD dry-run implementation, archive/evidence hygiene, no-byte-stream proof, future result-path validation, and execution-gate enforcement before any execution-capable runner stage.
- Stage 5BF historical route records are source-lock and taxonomy metadata only.
- Stage 5BF consumes ignored local `third_party/CicadaSolversIddqd` files by hash/path metadata only; do not commit raw archive bytes.
- Stage 5BF does not execute historical techniques, PGP network verification, stego tools, OutGuess/OpenPuff/MP3Stego, DWH/hash search, token-block experiments, byte-stream generation, CUDA, benchmarks, website expansion, method-status upgrades, or solve claims.
- Historical Stage 5BG review consumed Stage 5BF archive location, inventory, trust-classification, technique-taxonomy, source-gap, DWH context, token-block planning-impact, and guardrail records before Stage 5BI narrowed the follow-up to Fandom/source-lock crosswalk closure.
- Stage 5BI Fandom source-lock triage records are metadata-only provenance and planning records.
- Fandom pages are secondary route context unless future page-body source locks explicitly promote exact bodies.
- Fandom images/media are secondary copies, not original artefacts; prefer `third_party/CicadaSolversIddqd`, Stage 5BF archive/hash metadata, and commit-addressed public refs for original/source-equivalent crosswalks.
- Stage 5BI 2014 256-byte surfaces are context only and must not be combined with page 49-51 or used as experiment inputs without a future explicit source-lock/execution stage.
- Stage 5BI local spreadsheet records are non-canonical local analysis metadata only; do not commit the workbook or cell bodies, and do not change canonical transcription from them.
- Stage 5BJ original/archive crosswalk closure records remain metadata-only provenance and planning records.
- Stage 5BK historical-route planning constraints are metadata-only planning records, not execution permission.
- Stage 5BK iddqd-v2 source locks are compact metadata over ignored local files; raw iddqd-v2 bodies, fonts, media, images, archives, and full byte strings must not be committed.
- Stage 5BK String 4 is page49-51 matrix-hex context only and must not replace Stage 5AP transcription or authorize byte-stream generation.
- Stage 5BJ exact 2014 512-hex source locks and Stage 5BK byte-string locks are not experiment inputs, not DWH/hash targets, and must not be combined with page 49-51 without a future explicit execution-gated stage.
- Stage 5BK keeps `codex-output/**` as the canonical ignored Codex handoff root; `codex_output/**` is deprecated historical context and must not be created or used for current handoffs.
- Stage 5BM String 4 branch-crosswalk repair is metadata-only review integration, not execution permission.
- Stage 5BM String 4 branch membership is `partial_branch_match`; the one unsupported position blocks active use pending Stage 5BN source-gap closure or human-review packaging.
- Stage 5BM must not be used to commit full String 4 hex bodies, decoded bytes, reconstructed token streams, generated diagnostics, raw iddqd-v2/archive/Fandom/spreadsheet files, or full surface bodies.
- Stage 5BM preserves Stage 5AP canonical transcription, Stage 5AW branch metadata, Stage 5AZ active manifest policy, and Stage 5BD dry-run records unchanged.
- Stage 5BN String 4 unsupported-position closure is target-only metadata, not execution permission.
- Stage 5BN found local spreadsheet support for `0l` at token index 199, but Stage 5AW active possible tokens remain `0I`, `0j`, `OI`, and `Oj`.
- Stage 5BN proposed an inactive review-only `0l` addendum; it did not mutate Stage 5AW/5AY/5AZ records, canonical transcription, or active token-block manifests.
- Stage 5BO token-case operator errata records are compact metadata over ignored local templates, not committed template bodies.
- Stage 5BO's errata-aware option universe is inactive planning metadata only and does not mutate Stage 5AW/5AY/5AZ/5BD active records.
- Stage 5BO reclassifies String 4 as `full_branch_match` for planning only; it is not active input, not a byte stream, not DWH/hash evidence, and not solve evidence.
- Stage 5BQ consumes the Stage 5BP review outcome as `accept_with_warnings` metadata and records String 4 as `inactive_branch_context_only`.
- Stage 5BQ keeps `string4_active_input_allowed=false` and `string4_dry_run_ingestion_allowed_now=false`; String 4 is not ingested into Stage 5BD dry-run plans.
- Stage 5BQ's operator-errata sidecar is inactive planning metadata only; it is not a canonical transcription change, active manifest change, DWH/hash target, byte stream, or solve evidence.
- Future Stage 5BR review must inspect Stage 5BQ inactive-branch dry-run planning constraints before any execution-capable token-block stage, and must not execute token-block experiments, generate byte streams, materialise variants, run DWH/hash search, decode, run stego/audio/image/OCR/AI/CUDA/scoring/benchmark work, publish website content, upgrade method status, or make solve claims.
- Stage 5BS consumes the Stage 5BR accept-with-warnings review as compact metadata and records a closed String 4 planning-ingestion gate.
- Stage 5BS keeps `string4_active_input_allowed=false`, `string4_dry_run_ingestion_allowed_now=false`, and `future_token_block_execution_remains_blocked=true`.
- Stage 5BS future runners must cite the Stage 5BS planning-ingestion gate and citation policy or fail closed.
- Stage 5BS reviewability metadata is committed, but the Stage 5BR Deep Research body and Codex completion summary remain ignored and uncommitted.
- Future Stage 5BZ review must inspect Stage 5BY findings integration, duplicate source-digest classification, filename-equivalence map, inactive-sidecar planning manifest scaffold, no-execution planning-ingestion sidecar, manifest-supersession preflight carry-forward, active-lineage preservation, Stage 5BD plan preservation, no-active-ingestion proof, no-byte-stream gate, and no-execution records before any planning-ingestion or execution-capable token-block stage.
- Stage 5AX keeps git, GitHub, network/remote, generated-output-writing, issue-update, commit, and push operations serial.
- Stage 5AX uses pytest-xdist only when available and otherwise falls back to deterministic subprocess sharding.
- Stage 5AY preflight design cites Stage 5AW repaired branch metadata and the Stage 5AX next-stage decision, does not use ignored review-pack bodies as committed input, and does not execute token experiments or DWH/hash searches. Future Stage 5BE review must consume Stage 5BD dry-run records, Stage 5BB active-manifest registry, no-execution runner scaffold, and Stage 5AZ repaired manifest-design/execution-gate records before any execution-stage decision.
- Candidate Batch ABI v0 defines shared token-buffer, transform-parameter, key-schedule, stream-schedule, score-vector, top-k, backend-surface, and result-store compatibility contracts only.
- Stage 5U must keep `gematria_shift_score_only` parity distinct from original transform-family semantics.
- Stage 5U must not add kernels, modify CUDA source, run CUDA, run native/CUDA CMake, benchmark, publish generated bodies, or widen solved/unsolved scope.
- Stage 5V implements/records native no-GPU Candidate Batch ABI conformance only.
- Stage 5V may modify native/Python no-GPU reference code but must not modify CUDA source.
- Stage 5V must not run CUDA, add CUDA kernels, benchmark, or widen solved/unsolved scope.
- Stage 5V generated result bodies remain ignored; commit only compact conformance metadata.
- Stage 5V keeps `gematria_shift_score_only` parity distinct from original transform-family semantics.
- Stage 5V does not mark unresolved family-specific formulas as implemented.
- Stage 5V completion summaries must include native adapter counts, fixture counts, output hashes, gap implementation status, guardrails, and next-stage rationale.
- Future Stage 5W work must prepare prime-minus-one stream native parity contracts before family-specific CUDA contracts, top-k reducers, or benchmark planning.
- Stage 5W prepares prime-minus-one native parity contracts only.
- Stage 5W must not run CUDA or modify CUDA source.
- Stage 5W must not invent p56 token values, plaintext, ciphertext, or stream formulas.
- Stage 5W may generate deterministic prime schedules only from an explicit committed contract.
- Stage 5W must keep generated bodies ignored and commit compact metadata only.
- Stage 5W must keep p56 solved-fixture parity distinct from unsolved-page execution.
- Stage 5W must not treat source-backed p56 readiness as a new solve.
- Stage 5W completion summaries must include source inventory, stream formula, schedule policy, p56 readiness, guardrails, and next-stage rationale.
- Stage 5X executes only no-GPU native parity scoped by Stage 5W records.
- Stage 5X may execute only `stage5w-mapping-synthetic-prime-control-v0` and `stage5w-mapping-p56-stage4o-bounded-v0`.
- Stage 5X must keep `stage5w-mapping-p56-full-fixture-blocked-v0` blocked until a full committed p56 cipher token buffer is explicitly scoped.
- Stage 5X native parity is no-GPU Python-reference execution, not CUDA execution and not native C++ execution.
- Stage 5X bounded p56 parity is not full p56 parity, not performance evidence, and not solve evidence.
- Stage 5Y integrated compact Stage 5X reporting and CUDA contract readiness metadata, but did not execute CUDA, modify CUDA source, add kernels, run benchmarks, publish generated bodies, upgrade methods, or make solve claims.
- Stage 5AA implemented and ran only the Stage 5Z synthetic prime-minus-one validation vector; p56/full-p56, unsolved pages, benchmarks, scored experiments, generated-body publication, method-status upgrades, website expansion, and solve claims remain blocked.
- Do not stage `codex-output/**`.
- Do not report CUDA parity records as speedup/performance evidence.
- Do not stage `codex-output/**`.
- Completion summaries must be detailed and include parity counts, gate decisions, guardrail status, and next-stage rationale.
- Do not invent Gematria token values, token kinds, separator metadata, score-summary fields, or output hashes.
- Future solved-fixture-safe CUDA expansion requires explicit future-stage approval and no-unsolved guardrails.
- Stage 5J synthetic parity does not authorize solved-page CUDA.
- Solved-fixture-safe CUDA requires explicit token mapping, score-summary parity, no-unsolved guardrails, and future-stage approval.
- Future Gematria CUDA kernel work must use raw numeric token buffers and transformable masks.
- Separator placeholders must not be transformed.
- Stage 5J implementation must compare the CUDA token-output hash against the Stage 5H native fixture hash.
- Stage 5F synthetic A-Z kernel behavior remains separate from Stage 5H/5I numeric Gematria records.
- The Stage 5F uppercase Latin synthetic hash must not be treated as a Gematria mod-29 fixture hash.
- Solved-fixture CUDA expansion remains blocked until Stage 5M parity records, separator handling, score-summary parity, and explicit future-stage approval are cited.
- Future Gematria CUDA parity must use numeric tokens `0..28`, preserve separators unshifted, and keep Stage 4I confidence labels triage-only.
- CUDA device/kernel code must use conservative CUDA-C style.
- Do not use STL, std::array, std::vector, std::string, exceptions, RTTI, lambdas, or dynamic allocation in `.cu` / `.cuh` kernel/device paths.
- Host-side C++ convenience code belongs outside CUDA kernel/device-facing files.
- Future CUDA implementation work must cite the Stage 5E selected contract, Stage 5D native output hashes, Stage 5F synthetic parity records, Stage 5G parity/device-code audit records, Stage 5H Gematria contract records, and deterministic threading records before adding or widening any kernel target.
- CUDA detection must be no-GPU-safe by default.
- The local 16GB GPU profile is optional and must not become a CI requirement.
- Do not use device detection or smoke-build results as performance evidence.
- Do not add or widen CUDA kernels outside an explicit implementation stage.
- Do not stage `codex-output/**`.
- Local CUDA tool paths are optional local hints only, never CI requirements.
- Raw data, generated outputs, SQLite databases, raw Discord logs, raw page images, raw historical stego artefacts, extracted payloads, and local deep-research reports are not committed.
- No solve claims are present.
- Stage 4A generated Discord full-review site, redacted streams, channel shards, topic shards, indexes, copied LP page images, thumbnails, contact sheets, and upload archives are generated outputs and must not be committed.
- Future Deep Research handoffs should use the Stage 4A redacted bundle/site, not raw Discord logs.
- Public or semi-public hosting of Stage 4A output must use `redacted_public` mode and should consider noindex headers, private URLs, or basic access controls.
- Stage 4D bounded numeric verifier outputs are generated and ignored under `experiments/results/bounded-numeric/stage4d/`.
- Numeric verifier stages must follow the no-fudge policy: keep raw and derived values separate, record formulas/sources for derived values, and reject nearest-prime, arbitrary +/-n, post-hoc row/column arithmetic, route expansion, and fuzzy matching.
- Cuneiform-derived seeds require accepted coordinate/readout annotations before execution; current cuneiform records remain deferred.
- Dot and delimiter ambiguity remains noncanonical unless reviewed and explicitly promoted; delimiter audits must not infer reset-boundary meaning.
- Stage 4E source-delta outputs are generated and ignored under `experiments/results/source-delta/stage4e/`.
- `third_party/CicadaSolversIddqd/` is an ignored local cache for optional cicada-solvers/iddqd audit material; commit only README and `.gitkeep`.
- Do not blind-mirror external repositories. Source-delta audits commit metadata/records, not raw binary/image/audio/font artefacts.
- Font binaries must not be committed or shared.
- Compression artefact observations are preflight/control-only and not solve evidence; star-like compression/noise features require source variants and negative controls before interpretation.
- Source-lock delta candidates such as `https://github.com/cicada-solvers/iddqd` must be handled by an explicit source-lock stage, not opportunistically processed.
- Stage 4F generated stego/audio fixture diagnostics are generated and ignored under `experiments/results/stego-fixtures/stage4f/`.
- Historical stego/audio fixture records are metadata/source-locks only unless a later explicit execution stage enables a bounded manifest.
- Do not run stego/audio tools during source-locking stages.
- OpenPuff and MP3Stego tool requirements must be documented before any execution stage.
- No raw binary, audio, image, font, archive, or extracted payload artefacts may be committed.
- Stage 4G generated cookie refresh records are generated and ignored under `experiments/results/cookie-refresh/stage4g/`.
- Cookie refreshes must remain exact-source-backed. Do not add arbitrary strings, Discord-only strings, dictionary words, fuzzy matching, partial matching, hashcat, GPU/CUDA, or broad cracking.
- If Stage 4G returns zero exact matches, do not rerun cookie work without newly source-locked exact candidate strings.
- Stage 4H generated CPU batch records are generated and ignored under `experiments/results/cpu-batch/stage4h/`.
- Future CUDA work must use the Stage 4H CPU batch parity contract.
- Future CUDA work must cite Stage 5B parity harness, parity fixture, backend capability, and future-kernel matrix records before implementation.
- Stage 5B backend capability records are planning metadata; the local 16GB profile is optional and must not be required by CI.
- Stage 5B future-kernel matrix rows are planned or blocked only. They do not mean CUDA kernels exist.
- Do not implement GPU code until CPU batch and scorer APIs are stable and parity tests exist.
- Any new transform adapter must include a synthetic batch test and deterministic output hash expectation.
- CLI behavior for `libreprimus cpu-batch` must remain stable unless a future stage updates docs, schemas, tests, and the parity contract together.
- Stage 4I generated scoring-consolidation records are generated and ignored under `experiments/results/scoring-consolidation/stage4i/`.
- Scoring is triage metadata, not solve evidence.
- New scorers require scorer records, confidence-label mapping, tests, and calibration notes.
- Future CUDA must preserve score-summary semantics before any GPU score is trusted.
- Score labels cannot imply `solved` or `plaintext_verified`.
- Stage 4J generated observation-review reports are generated and ignored under `experiments/results/observation-review/stage4j/`.
- Observation promotion requires review-state checks and explicit promotion records.
- Review-only observations cannot be used as experiment seeds.
- Visual observations require page/image references and coordinate/region evidence before seed promotion.
- Absolute local machine paths must not be committed in operational records; use repository-relative generated-output paths or mark troubleshooting examples as `example_path`.
- Current-state text should be centralized through `STATUS.md` and `docs/roadmap/staged-plan.md` rather than copied into volatile paragraphs.
- Stage 4K generated source-lock snapshot reports are generated and ignored under `experiments/results/source-lock-snapshots/stage4k/`.
- `third_party/SourceSnapshots/` is an ignored local cache for allowlisted public source snapshots; commit only README and `.gitkeep`.
- Public source locks must be allowlisted and declare explicit snapshot policy.
- Prefer commit-addressed GitHub references over branch URLs.
- Network use for source-lock snapshots must be explicit via `--allow-network`.
- Source locks do not imply canonical truth or solve evidence.
- Do not commit binaries, images, audio, fonts, PDFs, archives, raw Discord artefacts, raw page images, or broad mirrored repository content.
- Stage 4L generated observation-promotion reports are generated and ignored under `experiments/results/observation-promotion/stage4l/`.
- The promotion ledger is the gate between review decisions and future manifests.
- Future manifests must cite promotion-readiness records.
- Ready_for_manifest does not mean execution.
- Control-only observations must not be treated as true claims.
- Stage 4M generated image-preflight reports are generated and ignored under `experiments/results/image-preflight/stage4m/`.
- Image preflight metrics are not hidden-message evidence.
- Compression/star-like artefacts require source variants and controls.
- Do not promote image artefact observations to seeds.
- Bigram/Fibonacci-421 audit requires reproducible matrix and null controls before execution.
- Stage 4N generated stego/audio positive-control reports are generated and ignored under `experiments/results/stego-positive-controls/stage4n/`.
- Positive-control readiness is not tool execution.
- Historical stego/audio cases require cached or immutable assets plus expected output hashes before execution.
- Synthetic controls can be ready without historical artefacts.
- Do not run stego/audio tools in source-lock/readiness stages.
- Stage 4O generated CPU batch adapter outputs are generated and ignored under `experiments/results/cpu-batch/stage4o/`.
- CPU batch adapters must keep transform semantics unchanged and must not alter solved-baseline expected outputs.
- Missing CPU batch adapters require explicit deferred or unsupported-by-design reasons.
- Future CUDA must satisfy Stage 4O parity expectations before trust.
- Stage 4P generated result-store unification outputs are generated and ignored under `experiments/results/result-store-unification/stage4p/`.
- Result-store unification is read-only reporting infrastructure, not experiment execution.
- Score-summary unification must use Stage 4I labels and must not invent scorer semantics.
- Missing optional generated outputs must be recorded explicitly, not silently ignored.
- Cross-stage reports are triage/comparison aids only and cannot make solve claims.
- Do not commit generated result records, generated score-summary records, SQLite databases, or local reports.
- Future CUDA planning must reference Stage 4O parity expectations and Stage 4P unified result surfaces.
- Stage 4Q generated benchmark planning outputs are generated and ignored under `experiments/results/benchmarks/stage4q/`.
- CPU smoke timings are diagnostic only and must not be reported as performance evidence.
- Future CUDA planning must cite Stage 4Q benchmark plan and parity readiness records.
- `codex-output/**` is a local ignored completion-handoff area and must not be staged.
- `ready_for_manifest` means planning readiness only; it does not mean execution.
- Control-only observations must not be treated as true claims.
- Generated review sites must include noindex metadata, `robots.txt`, and a privacy notice by default.
- Upload only generated `site/` contents, never raw `third_party/` inputs.
- Wiki publish failures should be recorded with exact errors and manual recovery steps, but research stages should not fail solely because the GitHub Wiki remote is unavailable.
- Stage 4B source triage must not mirror noisy public-link indexes blindly.
- Public-link promotion requires an allowlisted domain, source class, evidence strength, false-positive risk, and recommended action.
- Visual observations must preserve ambiguity; cuneiform, dot, braille, constellation, and star readings must not be treated as facts.
- Dot/binary/braille/constellation claims must not become experiment seeds without annotation records, exact coordinates, alternate readings, and controls.
- Stage 4B disabled manifests stay disabled until a later explicit execution stage.
- Deep Research reports that change project direction must update `docs/roadmap/staged-plan.md` and the research synthesis records under `data/research/`.
- Stage 4C generated annotation sites, copied review images, grid overlays, and blank annotation templates are generated outputs and must not be committed.
- Visual annotation must not infer meaning; coordinates and readings are separate evidence layers.
- Empty/blank annotation templates are generated and ignored unless a later stage explicitly commits a schema fixture.
- Visual observations remain noncanonical and `usable_as_experiment_seed=false` until reviewed and promoted in a later explicit stage.
- Future stages changing visual-observation status must update `docs/roadmap/staged-plan.md` and the method-family/retirement ledgers under `data/research/`.

## Source-of-truth files

Use `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md` as primary operational truth. Use `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `DATASET.md`, `RESEARCH.md`, and `CIPHER_CATALOG.md` as research/workflow truth. Use `ARCHITECTURE.md`, `CUDA_NOTES.md`, `docs/architecture/**`, and `docs/ci/**` as architecture/CI truth. Tutorials and `docs/wiki-source/**` are public guidance; repository tutorials remain the source of truth and Wiki pages are mirrors.

When stage status changes, update `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md` together. Long-lived operational docs must not describe obsolete stages as the current state. Historical references are allowed when clearly archival; do not rewrite `docs/development-logs/**` or `research-log/**` merely because they mention older stages.

Every future Codex stage must update relevant `.md` and `.txt` files when stage status, roadmap direction, experiment priorities, method-family status, data policy, CLI behavior, source-of-truth hierarchy, Deep Research reports, or schema/result families change. Check `STATUS.md`, `ROADMAP.md`, `docs/roadmap/staged-plan.md`, `AGENTS.md`, `README.md`, `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `CIPHER_CATALOG.md`, relevant docs/reference pages, relevant tutorials, and `docs/wiki-source/**`. If no documentation needs updates, state why in the final report.

If a method family is retired, reopened, or reprioritised, update `docs/roadmap/staged-plan.md` and the research synthesis ledgers under `data/research/`.

If a direction change happens, update `data/research/project-direction-change-records-v0.yaml`.

If a new raw, private, local, or generated output path is introduced, update `.gitignore` if needed and document the path in `docs/onboarding/private-generated-data-map.md`.

When state matters, verify local `HEAD`, `origin/main`, and latest CI directly with Git/GitHub tooling. Do not rely on rendered GitHub pages, cached raw URLs, or memory for current repository state.

## Corpus immutability rules

Raw source material belongs under `data/raw/` only when explicitly allowed by a later stage. Never normalize, patch, crop, OCR, transcribe, or deduplicate raw files in place.

Legacy workbook files under `data/raw/legacy-workbooks/` are immutable raw artefacts and must remain ignored by Git.

Legacy Pastebin files under `data/raw/legacy-pastebins/` are immutable raw artefacts and must remain ignored by Git.

Transcript files under `data/raw/transcripts/` are immutable raw artefacts and must remain ignored by Git.

## Coding standards

Prefer small, explicit modules with clear provenance boundaries. Avoid clever transformations without tests and documentation.

## C++ standards

Use C++20, namespace all project code under `libreprimus`, and keep foundational C++ smoke code dependency-free.

## CUDA standards

CUDA is optional. Add CUDA only behind `LPGPU_ENABLE_CUDA`. Never add a kernel without CPU reference behavior, parity tests, and a benchmark plan.

## Python standards

Use Python >=3.12,<3.14. Keep Python orchestration code typed, testable, and independent of compiled bindings until a later stage.

## Testing standards

Smoke tests prove the scaffold. Future transform tests must include known inputs, negative controls, determinism checks, and parity tests.

## Documentation standards

Document policy before implementation. Record assumptions, evidence levels, manifest requirements, and stop conditions near the code they govern.

## How to add a future cipher module

Create a CPU reference transform first, document the hypothesis in `CIPHER_CATALOG.md`, add unit tests, add manifest examples, and only then consider acceleration.

## How to add a future CUDA kernel

Start from the CPU reference and write parity tests before optimization. Add a benchmark that records hardware, compiler, CUDA version, and dataset lock.

## How to add a future experiment

Add a YAML manifest under `experiments/manifests/` with corpus locks, transform chain, scorer configuration, null controls, output policy, and review steps.

## How to record results

Write generated results to ignored result locations. Preserve manifest ID, git commit, corpus locks, transform chain, score breakdown, hardware metadata, and reviewer notes.

## False-positive controls

Every plausible result must be compared with null controls, shuffled controls where appropriate, score baselines, and manual review criteria.

## Citation/source rules

Do not treat memory, screenshots, or terminal output as source evidence. Later corpus work must cite source URL, acquisition date, hash, license status, and transcript policy.

## Git/staging rules

Preserve remotes and branches. Do not stage build outputs, caches, virtual environments, generated result files, raw corpus data, downloaded installers, logs, or databases.

Do not stage or commit `deep-research-reports/**`; these are local review inputs only.

## Prohibited actions

Do not download real corpus data unless a future source-lock stage explicitly scopes it. Do not run brute force, long benchmarks, CUDA stress tests, or unbounded searches. Do not print secrets or credential-bearing environment variables.

## Stop conditions

Stop and report if a tool install requires reboot, a CUDA installer requires driver replacement, raw data would be modified, or the repository has conflicting tracked user changes.

## Stage 0D-followup Alignment Rules

- Stage 0D-followup alignment outputs are still non-canonical.
- No-match reduction is useful, but not required for corpus freeze unless evidence quality improves.
- Boundary confidence must never be high from empty-pair or word-length-only evidence.
- Every boundary candidate must include evidence and `canonical_page_boundary=false`.
- Alignment-gap reports are generated outputs and must not be committed.
- GitHub issue updates must be idempotent and must not create duplicate issues.
- Push after successful commit remains required when remote is verified.

## Stage 0E Profile And Corpus Candidate Rules

- Gematria profile v0 is the tooling source of truth for rune/index/prime mapping once Stage 0E passes.
- Latin labels are display aliases; index order is arithmetic truth.
- Glyph variants belong in glyph-variant profiles, not Gematria canonical entries.
- Separator grammar v0 preserves separators as tokens.
- `%` and `/` must not be treated as final canonical page boundaries.
- Corpus candidate outputs are generated and must not be committed unless explicitly promoted.
- `canonical_corpus_active=false` remains required until a later activation stage.
- Corpus candidate records must retain source SHA-256s and profile SHA-256s.
- Push after successful commit remains required when remote is verified.

## Stage 1A Solved Fixture Rules

- Solved-page golden fixtures are test expectations, not new solve claims.
- Direct-translation fixtures must not use Atbash, Vigenere, prime-stream, brute-force, or scoring logic.
- Fixture records must include source and profile SHA-256 provenance.
- Pending fixtures are allowed when reference text or span selection is ambiguous.
- Generated reproduction outputs are ignored and must not be committed.
- Passing Stage 1A does not activate canonical corpus.
- Push after successful commit remains required when remote is verified.

## Stage 1B Atbash-Family Fixture Rules

- Reverse Gematria / Atbash-family fixtures are known-solved baselines, not new solve claims.
- Rotated reverse fixtures must declare rotation explicitly.
- Stage 1B must not infer or search rotations.
- Stage 1B must not use Vigenere or prime-stream logic.
- Generated Atbash-family reproduction outputs are ignored and must not be committed.
- Passing Stage 1B does not activate canonical corpus.
- Push after successful commit remains required when remote is verified.

## Stage 1C Vigenere Fixture Rules

- Mirrored reference repositories are reference/provenance sources only.
- Do not commit mirrored raw reference files.
- Do not import `lipeeeee/gematria` as a dependency.
- Do not copy code from `lipeeeee/gematria` into production modules.
- Vigenere fixtures are explicit-key known-solved baselines, not new solve claims.
- Vigenere keys must be declared in fixture manifests.
- Stage 1C must not infer or search keys.
- Stage 1C must not use prime-stream logic.
- Generated Vigenere reproduction outputs are ignored and must not be committed.
- Passing Stage 1C does not activate canonical corpus.
- Push after successful commit remains required when remote is verified.

## Stage 1D Prime-Stream Fixture Rules

- p56 prime-minus-one fixtures are known-solved baselines, not new solve claims.
- Prime-minus-one and phi-prime are equivalent for prime inputs and must not be counted as separate search families.
- Stage 1D must not perform prime-stream offset, direction, sequence, scoring, or CUDA search.
- Payload tokens must be preserved and checked separately from plaintext.
- Payload tokens must not advance prime streams or keys.
- Generated prime-stream reproduction outputs are ignored and must not be committed.
- Passing Stage 1D does not activate canonical corpus.
- Push after successful commit remains required when remote is verified.

## Stage 2A CPU Transform Registry Rules

- CPU transform registry entries are CPU reference transforms only.
- Registry transforms must not enable search, scoring, or CUDA unless a future stage explicitly implements and tests that capability.
- Every transform must declare `supports_gpu=false` until GPU parity work exists.
- Manifest-addressable solved baselines are regression runs, not search campaigns.
- Manifests must not contain raw corpus dumps.
- Generated manifest-runner outputs are ignored and must not be committed.
- `phi_prime_stream` is an alias of `prime_minus_one_stream` for prime inputs.
- Push after successful commit remains required when remote is verified.

## Stage 2B Result Store Rules

- Result stores are generated outputs and must not be committed.
- SQLite databases and SQLite sidecar files must not be committed.
- Result records must preserve manifest SHA-256, registry SHA-256, git commit, source/profile/corpus IDs, and false canonical/search/CUDA/scoring flags.
- Solved-baseline result imports are regression evidence, not unsolved-page experiments.
- Future experiments must use the result-store foundation before large searches.
- Push after successful commit remains required when remote is verified.

## Stage 2C CI Rules

- GitHub Actions CI must remain raw-data-free unless a future stage adds safe committed fixtures.
- CI must not require CUDA.
- CI must not require secrets.
- CI must not upload generated raw, corpus, or result artifacts by default.
- CI failures must not be bypassed by deleting tests.
- New commands added for CI must have local reproduction instructions.
- GitHub workflow YAML must remain readable multi-line YAML.
- CI workflow changes require static workflow tests.
- After CI workflow changes, verify both the local workflow and the remote raw workflow line count after push.
- CI YAML must not be minified or flattened.
- Remote workflow verification must not depend solely on `gh`; use raw GitHub URL fetch as a fallback.
- Do not minify `.gitattributes`; it must remain readable multi-line attributes.
- Do not rewrite profile or registry JSON without regenerating SHA locks and metadata.
- Do not update `.sha256` files by hand without running lock validation.
- Canonical profile and registry JSON files must be LF-normalized.
- CI lock-hash failures must be fixed, not skipped.
- Public README, STATUS, and ROADMAP must be updated whenever stage status changes.
- CI must include tests preventing stale top-level public status.
- Do not leave old next-milestone text in README after a stage completes.
- Public-facing docs must be readable multi-line Markdown, not minified single-line blobs.
- After infrastructure changes, verify local files, `origin/main` Git blobs, and optionally GitHub API/raw URL views.
- Do not rely solely on `raw.githubusercontent.com` for remote truth; fetched Git blobs are authoritative.
- Run the remote Git blob verifier after CI workflow or `.gitattributes` changes.
- Push after successful commit remains required when remote is verified.

## Stage 2D Consistency Rules

- New schema, manifest, documentation, registry, or result-store changes must pass the consistency checks.
- Do not update README, STATUS, and ROADMAP inconsistently.
- Transform registry changes must update CIPHER_CATALOG and manifests as needed.
- New generated output paths must be ignored and covered by ignored-output checks.
- CI consistency checks must remain raw-data-free.
- Stage 2D does not enable search, scoring, CUDA, canonical corpus activation, or page-boundary finalization.
- Push after successful commit remains required when remote is verified.

## Stage 2E Exploratory Dry-Run Rules

- Exploratory experiment manifests in Stage 2E are dry-run only.
- Do not execute unsolved-page search from exploratory manifests.
- `execution_enabled`, `search_execution_enabled`, `candidate_generation_enabled`, `scoring_enabled`, and `cuda_enabled` must remain false.
- Candidate-count estimation is allowed; candidate enumeration is not.
- Future unsolved page slices require `review_required=true`.
- Generated exploratory dry-run outputs are ignored and must not be committed.
- Stage 2E does not activate canonical corpus or finalize page boundaries.

## Stage 2F Bounded CPU Execution Rules

- Stage 2F execution is limited to synthetic and solved-fixture-only scopes.
- Unsolved-page execution remains prohibited.
- `search_execution_enabled`, `candidate_generation_enabled`, `scoring_enabled`, and `cuda_enabled` must remain false.
- Do not convert dry-run exploratory manifests into real unsolved-page campaigns.
- Generated CPU execution outputs are ignored and must not be committed.
- Stage 2F does not activate canonical corpus or finalize page boundaries.

## Stage 2G Proposal Approval Rules

- Real unsolved-page execution requires an explicit human approval record.
- Stage 2G must not auto-approve proposals.
- Pending and denied approvals must block execution.
- Approved records must include proposal SHA-256, approver, timestamp, scope, constraints, and expiry.
- Generated review packets are ignored and must not be committed.
- Stage 2G does not execute proposals, generate candidates, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Stage 2H Approval-Gated Execution Rules

- Approved execution in Stage 2H is limited to synthetic and solved-control scopes.
- Never commit approved approval records for unsolved-page execution without explicit future instruction.
- Approved records must be scope-bound and expire.
- Approval-gated execution must still reject search, candidate generation, scoring, and CUDA unless a future stage explicitly changes that.
- Generated approval execution outputs are ignored and must not be committed.
- Stage 2H does not activate canonical corpus, finalize page boundaries, or claim unsolved pages solved.

## Stage 2I Approval-Readiness Rules

- Stage 2I approval-readiness packets are not approvals.
- No Stage 2I proposal may execute.
- No approved approval records for real unsolved proposals may be committed.
- Approval-readiness packets must not include candidate plaintext or raw unsolved text.
- Human approval must be explicit and separate from proposal creation.
- Approval packets must be self-contained.
- Do not ask the user to answer vague metadata-review questions without exact paths and summaries.
- Codex/tooling must perform mechanical checks automatically.
- Human decision should be approve/revise/deny, not manual YAML auditing.
- If a corpus metadata path is missing, recommend revision instead of asking the user to guess.
- Stage 2I does not activate canonical corpus, finalize page boundaries, or claim unsolved pages solved.

## Stage 2J Bounded Auto-Run Policy Rules

- User grants standing permission for bounded local CPU experiments within `experiments/policies/operator-policy-v0.yaml` limits.
- Do not require per-experiment approval for queue items that pass the standing operator policy.
- Approval workflow is optional/high-risk audit tooling, not the default path for normal bounded local CPU experiments.
- Over-budget, CUDA/GPU, cloud, paid-service, generated-output-commit, solve-claim, canonical-corpus, and page-boundary changes still require explicit instruction or remain blocked.
- Generated bounded auto-run outputs are ignored and must not be committed.
- If a policy-passing item lacks a safe executor, record a deferred result instead of faking candidates or solve evidence.

## Stage 3A Minimal Bounded Executor Rules

- Bounded CPU experiment outputs are generated and must not be committed.
- Minimal triage scores are not solve evidence.
- Top candidates are leads only.
- Do not claim a solve from a score, top-k record, or terminal output.
- Commit only summary-level research notes, not full candidate dumps.
- CUDA remains disabled until a future explicit CUDA stage adds CPU/GPU parity tests.
- Canonical corpus remains inactive and page boundaries remain reviewable.

## Stage 3B Lead Inspection And Scoring Rules

- Stage 3B top candidates are leads only.
- Minimal or refined triage scoring cannot justify solve claims.
- Full candidate dumps remain generated outputs and must not be committed.
- Research logs may summarize top transform parameters, scores, qualitative labels, and safety flags only.
- Reranking and reverse-direction comparisons must stay within the standing bounded CPU policy.
- CUDA, canonical corpus activation, page-boundary finalization, broad search campaigns, and solve claims remain out of scope.

## Stage 3C Scoring Calibration Rules

- Scoring calibration is required before widening search space.
- Null controls must be used when adding new scoring features.
- Crib hits are weak evidence only.
- Positive-control-like scores are not solve claims.
- Do not tune scoring to make a specific candidate look good.
- Generated calibration outputs are ignored and must not be committed.

## Stage 3D Small Vigenere Key-List Rules

- Small key-list Vigenere runs are explicit-list only.
- Do not expand key lists without a manifest update and candidate-count checks.
- Key-list hits are leads only, not solve claims.
- Full Stage 3D candidate outputs remain generated outputs and must not be committed.
- Calibrated confidence labels are triage metadata only.
- CUDA, canonical corpus activation, page-boundary finalization, broad key search, and solve claims remain out of scope.

## Stage 3E Method Backlog Rules

- Stage 3E backlog ingestion must not silently widen search scope.
- Method backlog queue items must include candidate counts, exact parameters, evidence basis, generated-output policy, and executor-support status.
- Items requiring missing executors must be marked deferred or dry-run-only, not faked as runnable.
- Do not run broad dictionary search, arbitrary skip masks, CUDA, cloud work, canonical corpus activation, page-boundary finalization, or solve claims from Stage 3E.
- Dry-run summaries under `experiments/results/bounded-auto-runs/stage3e/` are generated outputs and must not be committed.

## Stage 3F Evidence-Key Vigenere Pack Rules

- Evidence-key Vigenere pack runs are explicit-list only.
- Do not expand keys without a manifest update and candidate-count checks.
- Reset and advance modes must be recorded in candidate output.
- Missing line or token-break metadata must cause warnings or deferred candidates, not invented boundaries.
- Key-pack hits are leads only, not solve claims.
- Full Stage 3F candidate outputs under `experiments/results/bounded-auto-runs/stage3f/` are generated outputs and must not be committed.

## Stage 3G Prime Offset Sweep Rules

- Prime offset sweeps must remain bounded by committed queue parameters.
- Offsets, directions, and reset modes must be recorded in candidate output.
- Missing line metadata must cause warnings or deferred candidates, not invented boundaries.
- Mersenne/perfect-number stream probes are low-cost hypotheses, not high-priority evidence.
- Mersenne probes must stay tiny, documented, and executor-gated before execution.
- Do not broaden to arbitrary number sequences without backlog update and policy count validation.
- Prime-stream hits are leads only, not solve claims.
- Full Stage 3G candidate outputs under `experiments/results/bounded-auto-runs/stage3g/` are generated outputs and must not be committed.

## Stage 3H Reset/Advance Rules

- Reset/advance experiments must not invent missing metadata.
- Unsupported reset modes must be deferred with explicit reasons.
- Separator-aware improvements require controls against separator-randomised negatives.
- Family-specific negative controls must accompany new state-machine behaviour.
- Top candidates remain leads only, not solve claims.
- Full Stage 3H candidate and control outputs under `experiments/results/bounded-auto-runs/stage3h/` are generated outputs and must not be committed.

## Stage 3I Historical Vigenere Rules

- Historical motif Vigenere runs are explicit-list only.
- Historical keys must have evidence basis documented.
- Do not expand historical key packs into dictionary search without manifest and policy update.
- Historical key hits are leads only, not solve claims.
- Full Stage 3I candidate outputs under `experiments/results/bounded-auto-runs/stage3i/` are generated outputs and must not be committed.
- Visual/image-derived observations are future work and must be stored as reviewable observations before becoming experiment seeds.

## Stage 3J Mersenne / Perfect-Number Probe Rules

- Mersenne/perfect-number stream probes are weak-to-moderate evidence and must stay tiny.
- Do not expand Mersenne probes into arbitrary number-sequence search without backlog and policy update.
- Use only the finite committed exponent sequence unless a future manifest explicitly changes it.
- Duplicate stream signatures must be reported, not silently ignored.
- Mersenne hits are leads only, not solve claims.
- Full Stage 3J candidate outputs under `experiments/results/bounded-auto-runs/stage3j/` are generated outputs and must not be committed.
- Visual/image-derived observations are future work and must be stored as reviewable observations before becoming experiment seeds.

## Public Documentation Wording Rules

- Do not use ambiguous non-goals wording for deferred roadmap work.
- README must not use a top-level `## Non-goals` section for temporary implementation boundaries.
- Use `Current boundaries and deferred work` for temporary public README boundaries.
- Public docs must distinguish permanent safety rules, current implementation boundaries, deferred future work, and completed work.
- README status and boundary sections must be updated when stages complete.
- Do not leave old Stage 0A boundary wording in top-level public documentation after later infrastructure stages implement parts of that work.

## Stage 3K Archive And Visual Observation Rules

- Raw local page images under `third_party/LiberPrimusPages/` must not be committed.
- Visual observations are reviewable hypotheses, not experiment seeds by default.
- Cookie/hash records must not claim preimages without exact byte matches.
- Image-derived numeric readings must preserve ambiguity.
- Do not use AI, OCR, or third-party image interpretation as source of truth.
- No live Tor crawling in normal stages.
- Archive source records must include source class and `trusted_as_canonical=false`.

## Stage 3L Cookie Hash Preimage Rules

- Cookie hash tests must use exact byte-string logging.
- No fuzzy or partial hash claims.
- SHA-256 exact match is a preimage candidate only, not a solve claim.
- Do not run broad hash cracking without explicit instruction.
- Do not use GPU, CUDA, hashcat, cloud, live Tor, or external dictionaries unless explicitly requested and re-scoped.

## Stage 3M Deterministic Image Analysis Rules

- Deterministic image-analysis outputs are generated and must not be committed.
- Visual feature candidates are review aids only.
- Feature candidates are not experiment seeds until promoted through a reviewable observation record.
- Do not use OCR, AI, or ML image interpretation as source of truth.
- Do not infer ciphers from visual feature flags alone.
- Do not commit raw local page images.

## Stage 3N Discord HTML Ingestion Rules

- Admin-provided Discord HTML logs are sensitive local research material.
- Do not commit raw Discord logs, message bodies, usernames, user IDs, avatars, or private attachment URLs.
- Do not upload Discord logs to AI services.
- Do not scrape Discord, use live Discord APIs, user tokens, or self-bots.
- Extracted Discord claims are reviewable leads only, not facts or experiment seeds.
- Committed Discord records must be aggregate/redacted only.

## Stage 3O Discord Promotion And Wiki Rules

- Public docs and tutorials must stay current after each stage.
- Tutorials are mirrored to GitHub Wiki from repository source files.
- Repository tutorials are the source of truth; the Wiki is a mirror.
- Do not edit the Wiki only without syncing the change back to tutorials.
- Discord promoted records must remain redacted and reviewable.
- Do not promote Discord claims to facts.
- Do not commit raw Discord logs, message bodies, usernames, user IDs, message IDs, or private attachment URLs.

## Stage 3P Image Transform Rules

- Image transform outputs are generated and must not be committed.
- Visual transform candidates are review aids only.
- Do not promote visual transform candidates to experiment seeds automatically.
- Do not interpret split/mirror artefacts as meaning without observation review and controls.
- Do not use OCR, AI, or ML image interpretation as source of truth.
- Do not process Discord logs in image stages.
- Do not commit raw local page images, generated derived images, generated contact sheets, generated review HTML, or generated transform JSONL records.

## Stage 3Q Discord Review Bundle Rules

- Discord review bundles are generated outputs and must not be committed.
- Topic shards are AI-review aids, not committed evidence.
- Raw Discord logs must never be committed.
- Usernames, user IDs, message IDs, avatar URLs, and private Discord URLs must not be committed.
- Deep Research should receive generated redacted shards, not raw HTML logs.
- Extracted Discord leads are hypotheses only and must not be promoted to facts or experiment seeds automatically.

## Stage 3R Discord Lead Promotion Rules

- Discord lead promotion requires public-source corroboration or exact artefact/observation references.
- Discord-only claims are not facts.
- Negative controls should preserve known false-positive classes.
- Post-Discord manifests must remain disabled until explicitly run in a later stage.
- Do not execute Stage 3R manifests during the promotion stage.
- Do not promote raw Discord private content, message bodies, usernames, user IDs, message IDs, or private attachment URLs.
- Promoted observation records must remain `usable_as_experiment_seed=false` until a later bounded review stage changes that explicitly.

## Stage 3S Onion 7 Seed-Pack Rules

- Onion 7 raw table values and derived values must remain separated.
- Do not add speculative Onion 7 interpretations without a manifest and source-record update.
- Post-Discord experiments remain bounded, CPU-only, generated-output-ignored, and no-solve by default.
- Raw Discord logs and raw page images must not be touched by post-Discord text experiments except for ignore-policy checks.
- Stage 3S executes only `EXP-3R-003`; do not run `EXP-3R-001` or `EXP-3R-004` in the same stage.

## Stage 3T GP/Rune Claim Verifier Rules

- GP/rune claim verification must not search neighbouring spans to make claims true.
- Missing exact spans must be classified as `missing_source_span`.
- Discord-derived count claims are hypotheses until recomputed against locked data.
- Boundary-sensitive claims must remain `boundary_sensitive`, not forced true or false.
- Do not process raw Discord logs or raw page images during verifier stages.
- Stage 3T executes only `EXP-3R-004`; do not run `EXP-3R-001` or rerun `EXP-3R-003` in the same stage.

## Stage 3U Cookie Signed-Variant Rules

- Cookie hash packs must use exact byte-string logging.
- Do not make fuzzy, partial, or near-match hash claims.
- Do not use GPU, CUDA, hashcat, cloud, external dictionaries, or broad candidate expansion without explicit re-scoping.
- An exact preimage match is a historical artefact lead only, not a solve claim.
- Do not process raw Discord logs or raw page images during cookie stages.
- Stage 3U executes only `EXP-3R-001`; do not rerun `EXP-3R-003` or `EXP-3R-004` in the same stage.

## Stage 4G Cookie Exact-Candidate Refresh Rules

- Cookie refreshes must use source-backed exact strings only.
- Manifest-declared byte variants and algorithms are the complete scope.
- No fuzzy, partial, near-match, dictionary, hashcat, GPU/CUDA, cloud, or broad cracking is allowed.
- Generated candidate records, exact-match records, duplicates, warnings, and summary JSON under `experiments/results/cookie-refresh/stage4g/` are generated outputs and must not be committed.
- A zero-match result keeps cookie SHA-256 exact packs negative/deprioritised unless new exact source strings are source-locked later.
- An exact match would be an `exact_preimage_candidate` artefact lead only, not a Liber Primus solve claim.
- Do not process raw Discord logs or raw page images during cookie stages.

## Stage 3V OutGuess Regression Rules

- OutGuess extraction outputs and payloads are generated and must not be committed.
- Missing OutGuess binary is not a failure when `--allow-missing-tool` is set.
- Missing historical assets are not a failure when `--allow-missing-assets` is set.
- Do not infer hidden meaning from non-empty payloads without expected hash and source validation.
- Do not run broad stego scans by default.
- Do not process raw Discord logs during stego stages.
- Raw historical artefacts under `third_party/CicadaArchive/` and `third_party/CicadaOutGuess/` must remain ignored except README and `.gitkeep`.

## Stage 4N OutGuess/Audio Positive-Control Rules

- Positive-control readiness records are planning metadata, not extraction or solve evidence.
- Historical OutGuess, OpenPuff, MP3Stego, hexdump/string, and audio cases require cached or immutable assets, exact expected-output hashes, and documented toolchain state before any execution stage.
- Synthetic controls may be readiness-complete for CI without historical artefacts.
- Do not run stego/audio tools, broad scans, spectrogram analysis, or payload extraction during source-lock/readiness stages.
- Do not commit raw fixture artefacts, images, audio, binaries, fonts, archives, extracted payloads, or generated reports.

## Stage 4O CPU Batch Adapter Expansion Rules

- CPU batch adapters must keep transform semantics unchanged.
- Solved-fixture parity must not alter solved-baseline expected outputs.
- Missing adapters require explicit deferred or unsupported-by-design reasons.
- Future CUDA must satisfy Stage 4O parity expectations before trust.
- Stage 4O CPU batch outputs are generated records and must not be committed.
- Do not treat CPU batch parity records as unsolved-page experiment evidence or solve claims.

## Stage 4P Result-Store Score-Summary Unification Rules

- Result-store unification is read-only reporting infrastructure, not experiment execution.
- Score-summary unification must use the Stage 4I finite confidence-label vocabulary.
- Do not invent scorer semantics, score labels, or calibration profiles while normalizing old records.
- Missing optional generated outputs must be recorded explicitly as warnings.
- Cross-stage reports are triage/comparison aids only and cannot make solve claims.
- Generated unified result records, score-summary records, cross-stage reports, and SQLite files remain ignored and must not be committed.
- Future CUDA planning must cite Stage 4O parity expectations and Stage 4P unified result surfaces.

## Stage 4Q CPU Benchmark Parity Planning Rules

- Benchmark planning is not CUDA implementation or GPU benchmarking.
- CPU smoke diagnostics are raw-data-free plumbing checks, not performance claims.
- Future CUDA planning must cite Stage 4O parity expectations, Stage 4P unified result surfaces, and Stage 4Q parity readiness records.
- Blocked/deferred adapters must remain blocked until stable CPU-batch contracts exist.
- Cookie/hash, stego/audio, image/compression, and bigram records are non-CUDA transform targets unless a later stage explicitly re-scopes them.
- Generated benchmark records and `codex-output/**` completion handoffs remain ignored and must not be staged.

## Stage 5A CUDA Planning Parity Scaffolding Rules

- Stage 5A CUDA target-plan and scaffold records are planning metadata, not CUDA execution approval.
- Do not add or modify CUDA source, `.cu`, or `.cuh` files during planning/scaffolding-only stages.
- Do not run GPU benchmarks or make speedup/performance claims before exact CPU/GPU parity harnesses exist.
- Future CUDA harness work must cite Stage 5A target-plan records, parity scaffold records, non-target records, and implementation gates.
- Non-target records for Discord, image/OCR/AI, compression artefacts, bigram/Fibonacci-421, stego/audio, cookie/hash cracking, broad campaigns, and website expansion must remain out of CUDA scope unless a later explicit stage re-scopes them.
- Generated CUDA planning reports under `experiments/results/cuda-planning/stage5a/` and `codex-output/**` handoffs remain ignored and must not be staged.

## Stage 5J Gematria CUDA Kernel Rules

- Stage 5J may implement only `gematria_mod29_shift_score_kernel` for the synthetic numeric Gematria mod-29 shift fixture.
- The source contract is `gematria_mod29_shift_score_contract_v0`, with token domain `integers_0_to_28` and `(token + shift) % 29` arithmetic.
- Preserve non-transformable separators by mask and candidate-major output ordering.
- Do not run real Liber Primus data, solved pages, or unsolved pages through CUDA.
- Do not treat Stage 5J as production Gematria CUDA readiness.
- Do not run GPU benchmarks or make speedup/performance claims.
- CUDA-facing `.cu` and `.cuh` code must keep the conservative CUDA-C subset: raw pointers, POD data, explicit sizes, and no STL, exceptions, RTTI, lambdas, or dynamic allocation in device paths.
- Generated Gematria CUDA reports under `experiments/results/gematria-cuda-kernel/stage5j/` and `codex-output/**` handoffs remain ignored and must not be staged.

## Stage 5K Gematria CUDA Parity Reporting Rules

- Stage 5K reports the Stage 5J synthetic Gematria CUDA/native hash match; it is not execution approval.
- Stage 5K must not add CUDA kernels, modify CUDA source, run CUDA, run solved fixtures, run unsolved pages, run real Liber Primus data, run GPU benchmarks, claim speedups, or make solve claims.
- Stage 5K solved-fixture-safe records must keep `solved_fixture_cuda_execution_allowed=false` until a future explicit stage records token-domain mapping, score-summary parity, no-unsolved guardrails, and approval.
- Stage 5K generated reports under `experiments/results/gematria-cuda-parity-reporting/stage5k/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Local CUDA paths and local GPU memory profiles are optional diagnostics only and must not become CI requirements.

## Stage 5L Solved-Fixture Gematria Token Mapping Rules

- Stage 5L maps committed solved-fixture-safe Stage 4O streams into Gematria `0..28` token buffers; it is not CUDA execution approval.
- Stage 5L native parity records are CPU/native output-hash fixtures for future comparison only.
- Do not add or modify CUDA source, run CUDA, run solved or unsolved pages through CUDA, run real Liber Primus data, run GPU benchmarks, claim speedups, or make solve claims during Stage 5L-style work.
- Preserve token kinds, transformable masks, separator positions, candidate-major ordering, and Stage 4I triage-only score-summary vocabulary.
- Solved-fixture CUDA execution remains blocked by `need_explicit_future_stage_approval` except where a later explicit stage records approval and no-unsolved guardrails.
- Generated Stage 5L reports under `experiments/results/gematria-solved-fixture-mapping/stage5l/` and `codex-output/**` handoffs remain ignored and must not be staged.

## Stage 5M Solved-Fixture Gematria CUDA Parity Rules

- Stage 5M may run CUDA only over the exact five Stage 5L mapped solved-fixture-safe token buffers.
- Stage 5M must use only the existing `gematria_mod29_shift_score_kernel`.
- Do not add new CUDA kernels or change device kernel arithmetic during Stage 5M-style work.
- Host-side runner plumbing is allowed only to feed the exact Stage 5L generated input buffers into the existing kernel.
- Original transform-family semantics are not exercised; Stage 5M exercises only mapped numeric `gematria_shift_score_only` buffers.
- Do not run unsolved pages, raw Liber Primus text, raw Discord logs, raw page images, raw stego/audio, canonical corpus material, or broad production data through CUDA.
- Do not run GPU benchmarks, report timing as performance evidence, claim speedups, expand the website, activate the canonical corpus, finalize page boundaries, or make solve claims.
- Generated Stage 5M reports under `experiments/results/gematria-solved-fixture-cuda/stage5m/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5N may report Stage 5M parity and define controlled expansion gates; it must not silently widen CUDA execution.

## Stage 5N Solved-Fixture CUDA Reporting Rules

- Stage 5N reports Stage 5M parity; it must not run CUDA.
- Stage 5N controlled expansion gates do not authorize unsolved-page CUDA, broad solved-fixture CUDA, GPU benchmarks, speedup claims, or production campaigns.
- Exact repeat verification is the only approved future execution shape, and only if a later stage explicitly scopes it.
- Result-store and score-summary preflight must use Stage 4P and Stage 4I contracts and keep confidence labels triage-only.
- Generated Stage 5N reports under `experiments/results/gematria-solved-fixture-cuda-reporting/stage5n/` and `codex-output/**` handoffs remain ignored and must not be staged.

## Stage 5U Candidate Batch ABI Rules

- Stage 5U Candidate Batch ABI records are contract metadata only.
- Do not run CUDA, native/CUDA CMake, GPU benchmarks, broad solved-fixture campaigns, unsolved-page CUDA, raw data, generated-body publication, website expansion, or solve-claim workflows during Stage 5U-style work.
- Token buffers must preserve Gematria values `0..28`, token kinds, separator placeholders, transformable masks, fixture offsets, fixture lengths, and candidate-major ordering.
- Key schedules and stream schedules require declared reset/advance policies before execution.
- Score-vector contracts must stay Stage 4I-compatible and triage-only; top-k output must use deterministic tie rules.
- Backend-surface contracts must keep Python orchestration, native reference, CUDA host/device, result-store, and generated-body responsibilities distinct.
- Stage 5U closes Stage 5T ABI gaps by contract only; native implementation remains pending for Stage 5V.
- Generated Stage 5U reports under `experiments/results/cuda-candidate-batch-abi/stage5u/` and `codex-output/**` handoffs remain ignored and must not be staged.

## Stage 5V Native Candidate Batch ABI Conformance Rules

- Stage 5V native Candidate Batch ABI conformance records are no-GPU reference metadata only.
- The Python reference adapter may execute raw-data-free fixtures; C++ adapter implementation remains deferred unless a future stage explicitly scopes it.
- Do not run CUDA, native/CUDA CMake, GPU benchmarks, broad solved-fixture campaigns, unsolved-page CUDA, raw data, generated-body publication, website expansion, or solve-claim workflows during Stage 5V-style work.
- Do not modify `.cu` or `.cuh` CUDA source, add CUDA kernels, change device arithmetic, or report speedups.
- Token buffers must preserve Gematria values `0..28`, token kinds, separator placeholders, transformable masks, fixture offsets, fixture lengths, and candidate-major ordering.
- Score-vector and top-k conformance must remain Stage 4I-compatible and triage-only; result-store records must remain compact metadata with generated bodies ignored.
- `gematria_shift_score_only` parity remains distinct from original transform-family semantics, and unresolved family-specific formulas must stay blocked or shape-only.
- Generated Stage 5V reports under `experiments/results/cuda-candidate-batch-abi-conformance/stage5v/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5V selects Stage 5W prime-minus-one stream native parity contract preparation; CUDA kernels and benchmark planning remain blocked.

## Stage 5W Prime-Minus-One Native Contract Rules

- Stage 5W prime-minus-one stream native parity contract records are contract-preparation metadata only.
- Do not run CUDA, modify CUDA source, add CUDA kernels, run native/CUDA CMake, benchmark, process raw data, publish generated bodies, upgrade method families to solved, or make solve claims during Stage 5W-style work.
- Do not invent p56 token values, plaintext, ciphertext, stream formulas, or full fixture buffers; use committed solved-fixture-safe records only.
- Deterministic prime schedules may be generated only from explicit committed contracts.
- The bounded Stage 4O/5L p56 mapping may be prepared for future no-GPU native parity, but full p56 parity remains blocked until a full committed token buffer is explicitly scoped.
- Generated Stage 5W reports under `experiments/results/prime-minus-one-native-contract/stage5w/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5W selects Stage 5X prime-minus-one stream no-GPU native parity execution and result-store preflight; CUDA kernels and benchmark planning remain blocked.

## Stage 5X Prime-Minus-One Native Parity Rules

- Stage 5X prime-minus-one stream no-GPU native parity records are bounded Python-reference parity metadata only.
- Stage 5X executes only the Stage 5W ready synthetic control and bounded p56 mappings; full p56 remains blocked pending a full committed token buffer.
- Do not run CUDA, modify CUDA source, add CUDA kernels, run native/CUDA CMake, benchmark, process raw data, publish generated bodies, upgrade method families to solved, expand the website, or make solve claims during Stage 5X-style work.
- Stage 5X generated reports under `experiments/results/prime-minus-one-native-parity/stage5x/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5X selected Stage 5Y prime-minus-one native parity reporting and CUDA contract readiness gate; CUDA kernels and benchmark planning remained blocked.

## Stage 5Y Prime-Minus-One Native Reporting Rules

- Stage 5Y prime-minus-one native reporting records are compact metadata only.
- Stage 5Y consumes Stage 5X records and must not rerun native parity, execute CUDA, modify CUDA source, add kernels, run native/CUDA CMake, benchmark, process raw data, publish generated bodies, expand the website, upgrade method families to solved, or make solve claims.
- Stage 5Y preserves `stage5w-mapping-p56-full-fixture-blocked-v0` until a complete committed p56 cipher token buffer is explicitly scoped.
- Stage 5Y CUDA contract readiness means contract preparation only. It is not CUDA execution permission.
- Stage 5Y bounded scored-experiment readiness means future manifest-gate planning only. It is not experiment execution permission.
- Stage 5Y generated reports under `experiments/results/prime-minus-one-native-reporting/stage5y/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5Y selects Stage 5Z prime-minus-one CUDA contract preparation; CUDA kernels, CUDA execution, and benchmark planning remain blocked.

## Stage 5Z Prime-Minus-One CUDA Contract Rules

- Stage 5Z prime-minus-one CUDA contract records are contract metadata only.
- Stage 5Z consumes Stage 5Y compact reporting/readiness records and must not rerun native parity, execute CUDA, modify CUDA source, add kernels, run native/CUDA CMake, benchmark, process raw data, publish generated bodies, expand the website, upgrade method families to solved, or make solve claims.
- Stage 5Z kernel ABI records are future CUDA-C style contracts only; they are not `.cu`/`.cuh` implementation evidence.
- Stage 5Z preserves `blocked_full_p56_token_buffer_missing`; full p56 remains blocked until a complete committed p56 cipher token buffer is explicitly scoped.
- Stage 5Z scored-experiment deferral records mean future manifest-gate planning only. They are not scored experiment execution permission.
- Stage 5Z generated reports under `experiments/results/prime-minus-one-cuda-contract/stage5z/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5Z selects Stage 5AA prime-minus-one CUDA synthetic kernel implementation and parity; the next stage must stay synthetic-only unless its prompt explicitly scopes otherwise.

## Stage 5AA Prime-Minus-One CUDA Synthetic Rules

- Stage 5AA prime-minus-one CUDA records are synthetic-only correctness metadata.
- Stage 5AA may execute only `stage5z-validation-synthetic-prime-control-v0` through `prime_minus_one_stream_kernel_v0`.
- Do not run p56/full-p56 CUDA, unsolved pages, broad solved fixtures, scored experiments, GPU benchmarks, website expansion, raw data, generated-body publication, method-status upgrades, canonical-corpus activation, page-boundary finalisation, or solve claims during Stage 5AA-style work.
- The Stage 5AA local CUDA pass is not performance evidence and does not authorize broader CUDA execution.
- Stage 5AA preserves `blocked_full_p56_token_buffer_missing`; bounded-p56 CUDA parity needs Stage 5AC preflight before any execution.
- Stage 5AA generated reports under `experiments/results/prime-minus-one-cuda-synthetic/stage5aa/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5AA selected prime-minus-one CUDA synthetic parity reporting and bounded-p56 CUDA parity preflight when the synthetic hash matched; Stage 5AC completed that reporting/preflight under the post-staleness-repair stage name.

## Stage 5AB Document Staleness Hardening Rules

- Stage 5AB is a process-quality and stale-doc repair stage, not CUDA execution.
- Operational docs used Stage 5AB as a quality gate and now use the updated source-of-truth record to treat Stage 5AC as complete and Stage 5AD as the next selected work.
- Use `data/project-state/stage5ah-doc-staleness-source-of-truth.yaml` and `data/project-state/operational-file-map.yaml` when checking current/next-stage text. The Stage 5AB source-of-truth file is historical context only.
- Website expansion is deferred to a future unnumbered project, not Stage 6.
- Missing optional generated staleness reports are not evidence; generated reports under `experiments/results/doc-staleness/stage5ab/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5AB must not run native/CUDA execution, modify CUDA source, add kernels, run benchmarks, execute scored experiments, process raw data, publish generated bodies, upgrade method status, or make solve claims.

## Stage 5AH Doc Staleness Coverage Rules

- Stage 5AH is a process-quality and stale-doc coverage stage, not source extraction or CUDA execution.
- Stage 5AH repairs README stage-ledger truncation, current/next-stage consistency, and operational-file-map coverage before Stage 5AI curated extraction resumes.
- Use `libreprimus consistency check-stage-ledger-staleness`, `check-operational-file-map-coverage`, `check-current-next-stage-consistency`, and `validate-stage5ah-doc-staleness` for future current-state documentation changes.
- Stage 5AH generated reports under `experiments/results/doc-staleness/stage5ah/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5AH must not process raw third-party sources, fetch from the network, clone online repositories, use Google Drive storage, run Deep Research, run native/CUDA execution, modify CUDA source, add kernels, run benchmarks, execute scored experiments, expand the website, or make solve claims.

## Stage 5AI Curated Research Bundle Rules

- Stage 5AI is local source-curation metadata, not Deep Research execution or experiment execution.
- Stage 5AI generated bundle bodies under `research-inputs/stage5ai/` remain ignored; commit only compact metadata, schemas, docs, tests, and README/.gitkeep scaffolds.
- Stage 5AI generated reports under `experiments/results/research-bundles/stage5ai/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Website-ingest records from Stage 5AI are metadata only; public website-ready count remains `0` until a future publication review stage explicitly scopes website expansion.
- Stage 5AK Deep Research should consume Stage 5AI/5AJ bundle manifests, source cards, content indexes, known-question files, do-not-assume files, and extraction-fidelity/redaction policy, not raw `third_party/` paths.
- Stage 5AI must not fetch from the network, clone online repositories, use Google Drive storage, commit raw third-party material, run OCR/AI/ML/image forensics/stego/audio tools, generate or execute hypotheses, run CUDA, benchmark, execute scored experiments, activate the canonical corpus, finalise page boundaries, upgrade method status, or make solve claims.

## Stage 5AK Community Facts Integration Rules

- Stage 5AK is local curation, claim-record, arithmetic-preflight metadata, and Deep-Research-pack update work only, not Deep Research execution, website publication, OCR, AI/ML interpretation, image forensics, stego/audio execution, hypothesis generation/execution, CUDA execution, benchmarking, scored experimentation, corpus activation, page-boundary finalisation, method-status upgrade, or solve evidence.
- Raw `third_party/UsefulFilesAndIdeas/community-facts/` files and generated extracts under `research-inputs/stage5ak/` and `experiments/results/source-harvester-community-facts/stage5ak/` remain ignored; commit only compact metadata, schemas, docs, tests, logs, and `.gitkeep` scaffolds.
- Community number facts are claim records, not truth records. Future work must source-lock exact transcripts/profiles/images, declare count and coordinate policies, and add null/multiple-testing controls before any bounded verifier.
- Public website ingest remains metadata-only and conservative. Public website-ready count stays `0` until a future explicit publication-review stage scopes website expansion.
- Stage 5AL should run Deep Research source inventory and reliability review against curated Stage 5AI/5AJ/5AK metadata and private ignored handoffs, not raw message logs or raw images.

## Stage 5AJ UsefulFilesAndIdeas Integration Rules

- Stage 5AJ is local-source metadata and policy integration, not Deep Research execution, website publication, live scraping, OCR, AI/ML interpretation, image forensics, stego/audio execution, CUDA execution, benchmarking, scored experimentation, hypothesis generation/execution, corpus activation, page-boundary finalisation, method-status upgrade, or solve evidence.
- Raw `third_party/UsefulFilesAndIdeas/` files and generated extracts under `research-inputs/stage5aj/` and `experiments/results/source-harvester-usefulfiles/stage5aj/` remain ignored; commit only compact metadata, schemas, docs, tests, logs, and `.gitkeep` scaffolds.
- Private Deep Research extracts should preserve technical fidelity aggressively. Redact only minimal privacy/safety material and log every redaction; do not strip rune strings, numbers, hashes, URLs, formulas, sheet/cell coordinates, highlights, or table structure from private handoffs.
- Public website ingest remains metadata-only and conservative. Public website-ready count stays `0` until a future explicit publication-review stage scopes website expansion.
- Stage 5AK consumed the new local community-facts material as metadata only; Stage 5AL staged source reliability metadata from Stage 5AI/5AJ/5AK records and should not read raw local workbooks/images/text unless a future prompt explicitly scopes a local-only source-policy stage.

## Stage 5AL Website-Ingest Staging Rules

- Stage 5AL is metadata-only website-ingest and private Deep Research export staging, not public website publication or Deep Research execution.
- Future Deep Research prompts must consume `data/source-harvester/stage5al-deep-research-export.yaml`, `data/website-ingest/stage5al/`, and ignored `research-inputs/stage5al/` helper files rather than raw `third_party/` paths.
- Publication gates are mandatory. Public website-ready remains `0` until a future reviewed publication stage explicitly marks records safe.
- Do not commit raw third-party files, generated private export bodies, private community identifiers, raw message bodies, raw images, raw workbook bodies, SQLite databases, local absolute paths, or `codex-output/**`.
- Stage 5AL does not authorize OCR, AI/ML interpretation, image/stego/audio tooling, hypothesis generation/execution, CUDA, benchmarks, scored experiments, method-status upgrades, canonical corpus activation, page-boundary finalisation, or solve claims.
- Stage 5AM renders a private static metadata index from Stage 5AL records before Deep Research; Stage 5AN built the private content pack; Stage 5AP adds token-block source-lock metadata before the next focused review.

## Stage 5AM Static Research Website Renderer Rules

- Stage 5AM generated static site files are ignored under `website-export/stage5am/` and must not be staged.
- The static research index is metadata-only and review-gated; it is not public website publication.
- Do not publish raw/private bodies, generated extraction bodies, private IDs, local absolute paths, raw images, raw workbooks, archives, audio, video, or PDFs through the renderer.
- Stage 5AN built the private content pack before Deep Research; Stage 5AV and Stage 5AW route token-case work to Stage 5AY bounded preflight design using Stage 5AW repaired branch records, Stage 5AV decision/branch records, Stage 5AU review-pack v2 metadata, Stage 5AT policy/challenge records, Stage 5AR coordinate records, Stage 5AP token-block records, Stage 5AL/5AM/5AN metadata, and private hosted content URLs only.

## Stage 5AN Private Content Pack Rules

- Stage 5AN generated private content pack files are ignored under `deep-research-content-packs/stage5an/`; commit only README/.gitkeep scaffolds outside generated bodies and compact metadata under `data/deep-research-export/`.
- Stage 5AN hosted private-content and combined webroot files are ignored under `website-export/stage5an/` and must not be staged.
- The SFTP-ready upload root is `website-export/stage5an/webserver-root/`; copy the contents of that folder to the private server root if hosting is desired.
- Noindex and robots metadata are not access control. Use private hosting controls if generated extracts are uploaded.
- Stage 5AN private content is review-gated handoff infrastructure, not public website publication, not Deep Research output, not experiment execution, and not solve evidence.
- Future review should cite Stage 5AU review-pack v2 records, Stage 5AT review-pack records, Stage 5AR coordinate-lock records, Stage 5AP token-block records, and both `http://liberprimus-gpu-data.info/index.html` and `http://liberprimus-gpu-data.info/private-content/` when the user confirms the generated webroot is uploaded.

## Stage 5AP Token-Block Source-Lock Rules

- Stage 5AP page 49-51 token-block records are source-lock/preflight metadata only.
- The 32x8 token transcription, logical coordinates, primary-60 mapping, null controls, DWH context, and OutGuess controls are not decoded plaintext, canonical corpus activation, experiment seeds, hash targets, or solve evidence.
- Generated token-block and stego-control reports under `experiments/results/token-block/stage5ap/` and `experiments/results/stego-controls/stage5ap/` remain ignored.
- Stage 5AY bounded preflight design cites Stage 5AW repaired decision/branch records, Stage 5AV decision records, Stage 5AU review-pack v2 records, Stage 5AT review-pack records, Stage 5AR original-image coordinate records, and Stage 5AP source-lock, transcription, alphabet, mapping, null-control, DWH, and OutGuess guardrail records. Future Stage 5BE review must cite Stage 5BD dry-run planning records, Stage 5BB runner scaffold records, and Stage 5AZ repaired execution gates before any bounded token-block execution follow-up.

## Stage 5AR Original-Image Coordinate Lock Rules

- Stage 5AR page 49-51 original-image coordinate records are source-lock/review-preflight metadata only.
- Original local page images are coordinate truth for pixel boxes; screenshots, crops, modified images, web-rendered pages, and private generated images are not coordinate truth.
- Pixel coordinates are not OCR output, decoded text, semantic image interpretation, hidden-content forensics, experiment seeds, CUDA input permission, canonical corpus activation, page-boundary finalisation, or solve evidence.
- Stage 5AR generated coordinate reports under `experiments/results/token-block/stage5ar/` remain ignored and must not be staged except for allowed scaffold files.
- Stage 5AY bounded preflight design cites Stage 5AW repaired decision/branch records, Stage 5AV decision/branch records, Stage 5AU review-pack v2 records, Stage 5AT review-pack records, and Stage 5AR source-lock, image-variant, page-split, pixel-coordinate, case-policy, coordinate-validation, source-lock/null-control, DWH context, and guardrail records. Future Stage 5BE review must preserve the Stage 5BD no-byte-stream proof, Stage 5BB no-execution proof, and Stage 5AZ repaired no-execution guardrails unless a later prompt explicitly scopes execution.

## Stage 5AT Token Case Review Pack Rules

- Stage 5AT token case-review records are human-review packaging metadata only.
- Generated review-pack files under `human-review-packs/stage5at/token-case-review/` and generated reports under `experiments/results/token-block/stage5at/` remain ignored and must not be staged except allowed scaffolds.
- The Stage 5AP canonical transcription remains unchanged until reviewed human decisions are explicitly integrated by a future stage.
- Stage 5AT was audited by Stage 5AU as count-valid but not usable for reliable manual decisions; manual review should use the Stage 5AU v2 pack instead.

## Stage 5AU Token Case Review Pack V2 Rules

- Stage 5AU token case-review pack v2 records are local usability-repair metadata only.
- Generated v2 review-pack files under `human-review-packs/stage5au/token-case-review-v2/` and generated reports under `experiments/results/token-block/stage5au/` remain ignored and must not be staged except allowed scaffolds.
- Derived glyph-candidate crops, context crops, row context, page-strip context, and overlays are review aids only and must not be treated as source truth or automatic token decisions.
- Stage 5AU displays all 203 case-review challenges and all 212 canonical-transcription challenges but does not fill human decision fields.
- Stage 5AV consumed the filled local decision template; the template remains ignored and must not be staged.

## Stage 5AV Token Case Decision Integration Rules

- Stage 5AV decision records are local human-decision integration metadata only.
- Unresolved multi-option cases must stay unresolved branch metadata; do not force token identity.
- Canonical transcription remains unchanged unless a future explicit stage validates `change_token` decisions.
- The compact branch manifest is planning metadata only; do not enumerate full variants or generate variant byte streams in Stage 5AV.
- Stage 5AW decision-parser repair is parser metadata cleanup only and must not be reported as execution, token identity resolution, or canonical transcription change.
- Stage 5AX parallel validation must not run token experiments, DWH/hash searches, decode attempts, OCR, AI/ML, LLM vision, semantic image interpretation, hidden-content forensics, stego, CUDA, cryptanalytic benchmarks, scored experiments, or solve claims. Stage 5AY bounded preflight design inherits those no-execution boundaries unless explicitly scoped otherwise.

## Stage 5AC Prime-Minus-One CUDA Synthetic Reporting Rules

- Stage 5AC is reporting/preflight metadata only, not CUDA execution.
- Stage 5AC consumes Stage 5AA synthetic CUDA parity records and Stage 5AB doc-staleness records.
- Stage 5AC may mark only the bounded `stage5z-validation-p56-bounded-v0` vector ready for a future explicit Stage 5AD run.
- Stage 5AC must keep full p56 blocked until a full committed p56 cipher token buffer is explicitly scoped.
- Stage 5AC must keep scored experiments, benchmarks, unsolved-page CUDA, website expansion, generated-body publication, method-status upgrades, canonical-corpus activation, page-boundary finalisation, and solve claims blocked.
- Stage 5AC generated reports under `experiments/results/prime-minus-one-cuda-synthetic-reporting/stage5ac/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5AC selects Stage 5AD bounded p56 CUDA parity only because Stage 5AA synthetic parity passed and Stage 5AB doc-staleness checks are clean; this does not authorize full p56 or unsolved-page CUDA.

## Stage 5AD Bounded P56 CUDA Parity Rules

- Stage 5AD ran only `stage5z-validation-p56-bounded-v0` through the existing prime-minus-one CUDA kernel.
- Stage 5AD recorded `failed_hash_mismatch`: expected Stage 5X hash `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`, computed CUDA hash `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`.
- Stage 5AD did not add CUDA kernels, modify CUDA-facing `.cu` or `.cuh` source, alter device arithmetic, run full p56, run unsolved pages, benchmark, execute scored experiments, publish generated bodies, upgrade method status, or make a solve claim.
- Full p56 remains `blocked_full_p56_token_buffer_missing`; scored experiments remain `deferred_manifest_gate_required`; website expansion remains a future unnumbered project.
- Stage 5AD generated reports under `experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/` and `codex-output/**` handoffs remain ignored and must not be staged.
- Stage 5AD-fix has now diagnosed the mismatch; Stage 5AD itself remains preserved as a failed historical parity record.

## Stage 5AD-fix Bounded P56 Mismatch Rules

- Stage 5AD-fix recorded that the Stage 5AD CUDA/formula hash `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387` matches the Stage 5X formula hash.
- Stage 5AD-fix recorded that the Stage 5AD expected hash `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87` follows Stage 5L candidate-major reference material, not formula-output material.
- The primary root cause is `expected_hash_reference_lineage_mismatch`; reference-contract and hash-material policy repair are required, but CUDA kernel repair is not supported by current evidence.
- Stage 5AD-fix does not run CUDA, change CUDA source, add kernels, run full p56, run unsolved pages, benchmark, execute scored experiments, publish generated bodies, upgrade method status, or make a solve claim.
- Stage 5AE has now repaired corrected bounded p56 CUDA formula parity reporting and reference-contract metadata while preserving Stage 5AD as failed and without widening scope.
- Stage 5AF added Cicada Source Harvester tooling, local-only source-manifest records, clue-category records, research-bundle planning, and dry-run provenance summaries. Stage 5AG then inventoried local ignored third-party source material and wrote compact metadata/source-lock readiness records only. Neither stage performed live broad scraping, Google Drive storage, raw source commits, CUDA execution, benchmark, scored experiment, website expansion, or solve claim.
- Stage 5AD-fix generated reports under `experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix/` and `codex-output/**` handoffs remain ignored and must not be staged.

## Stage 3W State Consolidation Rules

- Stage 3W changes persistent context, checks, docs, tests, and metadata only.
- Do not add experiment functionality, execute experiments, process raw data, process Discord logs, process page images, run OutGuess extraction, use CUDA, activate canonical corpus, finalize page boundaries, or claim a solve.
- Keep `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` synchronized when stage status changes.
- Run `libreprimus consistency check-state-drift` before staging documentation-heavy changes.
- `deep-research-reports/**` is local review material and must never be staged, committed, or pushed.

## Stage 3X CLI Modularisation Rules

- Keep `python/libreprimus/cli.py` as the public `python -m libreprimus.cli` entrypoint.
- Do not create `python/libreprimus/cli/` while `cli.py` exists.
- CLI refactors must preserve command names, option names, help behavior, output shape, and exit semantics unless a later stage explicitly scopes a behavior change.
- Add or update command-surface tests whenever CLI commands are added, removed, renamed, or moved.
- Do not combine CLI modularisation with experiment execution, schema redesign, raw-data processing, CUDA work, canonical corpus activation, page-boundary finalization, or solve claims.
