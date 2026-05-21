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

Current completed stage: Stage 5L - solved-fixture-safe Gematria shift_score token mapping and native parity fixture preparation.

Current work: Stage 5M - first solved-fixture-safe Gematria shift_score CUDA parity run, pending explicit future-stage approval. Stage 5M may consume Stage 5L token mappings and native parity records, but it must remain solved-fixture-safe, no-unsolved, no-benchmark parity work unless the prompt explicitly scopes otherwise.

Current project state:

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page campaigns: not started.
- CUDA: deferred until CPU references, stable scorer definitions, batch APIs, parity tests, and benchmarks exist.
- Existing CUDA code: scaffold/smoke infrastructure, the Stage 5F synthetic `shift_score_kernel`, Stage 5G reporting/device-code hardening, Stage 5H contract metadata, Stage 5I preparation metadata, and the Stage 5J synthetic numeric `gematria_mod29_shift_score_kernel` only unless code and tests say otherwise.
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
- Do not invent Gematria token values, token kinds, separator metadata, score-summary fields, or output hashes.
- Future solved-fixture-safe CUDA requires explicit future-stage approval and no-unsolved guardrails.
- Stage 5J synthetic parity does not authorize solved-page CUDA.
- Solved-fixture-safe CUDA requires explicit token mapping, score-summary parity, no-unsolved guardrails, and future-stage approval.
- Future Gematria CUDA kernel work must use raw numeric token buffers and transformable masks.
- Separator placeholders must not be transformed.
- Stage 5J implementation must compare the CUDA token-output hash against the Stage 5H native fixture hash.
- Stage 5F synthetic A-Z kernel behavior remains separate from Stage 5H/5I numeric Gematria records.
- The Stage 5F uppercase Latin synthetic hash must not be treated as a Gematria mod-29 fixture hash.
- Solved-fixture CUDA execution remains blocked until token-domain mapping, separator handling, score-summary parity, and explicit future-stage approval are recorded.
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
- Solved-fixture CUDA execution remains blocked by `need_explicit_future_stage_approval` until a later explicit stage records approval and no-unsolved guardrails.
- Generated Stage 5L reports under `experiments/results/gematria-solved-fixture-mapping/stage5l/` and `codex-output/**` handoffs remain ignored and must not be staged.

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
