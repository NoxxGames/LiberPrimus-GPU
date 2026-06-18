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

Current completed stage: Stage 6H - Current-state integrity repair and dot-angle / right-triangle number-triangle source-lock addendum, without execution.

Next routed stage: Stage 6I - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6I receives explicit Stage 6C/6D/6E/6F/6G/6H handoff inputs and remains without execution until a later prompt explicitly authorizes any Stage 7 work.

No Deep Research activation-acceptance record exists, the combined gate is not satisfied, no valid activation decision exists, and no active planning input authorization or selection exists. String 4 remains inactive; no target-priority selection, source-lock browser puzzle execution, direct source-record number-fact backfill, historical source-lock rewrite, triangle/Page32 route extraction, music route extraction, audio/stego/OCR/image forensics/AI interpretation, active ingestion, byte-stream generation, machine-code/VM execution, manifest supersession, execution, target-class validation, Tor access, DWH/hash/preimage search, decode, scoring, CUDA, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim is authorized.

Future Codex work must apply `docs/onboarding/codex-acceptance-criteria.md`.

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- CUDA: deferred.

Discord raw logs are not committed. Raw page images, raw historical stego artefacts, generated outputs, SQLite databases, and local reports remain ignored and uncommitted.

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

<!-- BEGIN stage5ef -->
## Stage 5EF Current-Truth Amendment

- Current completed stage: Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, diagnostic probe manifests, and enriched fact cards, without execution.
- Current work: Stage 5EI - Source-lock number-fact review batch 006, without execution. Stage 5EG inserted deterministic doc-staleness guardians before Lag5 source-lock and the previously deferred number-fact review batch 006.
- Authoritative current truth is `data/project-state/current-stage-state.yaml`.
- Broad Markdown docs are mirrors or historical evidence, not authoritative state.
- Stage 5EE originally routed Stage 5EF to number-fact review batch 006; that batch is now deferred to Stage 5EG.
- Stage 5EF creates no source-lock evidence, number-fact overlays, target selection, byte streams, execution, CUDA,
  scoring, benchmarks, website expansion, or solve claim.
<!-- END stage5ef -->

<!-- BEGIN stage5eg -->
## Stage 5EG Doc-Staleness Guard

- Current completed stage: Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, diagnostic probe manifests, and enriched fact cards, without execution.
- Current work: Stage 5EI - Source-lock number-fact review batch 006, without execution.
- Future closeout must run or explicitly report `python -m libreprimus.cli consistency audit-stale-current-claims --strict`.
- Project `.codex` hooks are declared only; they are not effective until operator trust.
- Read-only custom agents are available for explicit closeout review, but hooks use deterministic scanner commands, not agents.
- Stage 5EG creates no source-lock evidence, number-fact overlays, route extraction, byte streams, execution, CUDA, scoring, benchmarks, website expansion, or solve claim.
<!-- END stage5eg -->

<!-- BEGIN stage5eh -->
## Stage 5EH Lag5/Outguess/Byte-Control Source-Lock Addendum

- Current completed stage: Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, diagnostic probe manifests, and enriched fact cards, without execution.
- Current work: Stage 5EI - Source-lock number-fact review batch 006, without execution.
- Stage 5EH is metadata/source-lock/reviewability only: it inventories local Lag5 and iddqd-v2 source files, creates future probe manifests with `run_now=false`, and adds overlay-only NumberFactCards.
- Do not run OutGuess, StegDetect, F5 extraction/password search, XOR reconstruction, OCR, image forensics, route extraction, byte-stream generation, CUDA, scoring, benchmarks, Tor, or solve workflows from Stage 5EH records.
- `third_party/CiadaSolversIddqd_v2/lp_outguessed` is the canonical local lp_outguessed root unless a future validator proves otherwise; duplicate `xor.txt` candidates elsewhere are reviewability context only.
<!-- END stage5eh -->

<!-- BEGIN stage5ei -->
## Historical Stage 5EI Boundary

At the time of Stage 5EI closeout, Stage 6 - Diagnostic backlog census, discovery-probe readiness, result-bundle policy, and Stage 7/8/9 handoff, without execution was the next routed readiness stage.

Stage 6B later repaired the Stage 6 readiness metadata and routed final manifest work to Stage 6C.

Project-local `.codex` hooks are declared and operator-approved locally for Stage 5EI recording purposes. They remain deterministic scanner hooks, not custom-agent execution hooks: `blocking_hooks_effective_now=false`, `hook_execution_relies_on_deterministic_scanner=true`, and `custom_agents_invoked_by_hooks=false`.

Stage 5EI superseded the ordinary number-fact review batch 006. Do not run probes, route extraction, byte-stream generation, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, benchmarks, target selection, canonical corpus activation, page-boundary finalisation, or solve claims under the Stage 5EI records. Stage 6 must be readiness-only unless a later prompt explicitly changes scope.
<!-- END stage5ei -->

<!-- stage6:start -->
## Historical Stage 6 Boundary

At the time of Stage 6, Stage 6 - Diagnostic backlog census, discovery-probe readiness, result-bundle policy, and Stage 7/8/9 handoff, without execution was complete.

The routed follow-up at that time was Stage 6B. Stage 6 is diagnostic-backlog and archive-policy metadata only. It records bounded source-root census, future discovery probes, no-lossy Stage 7 archive policy, and Stage 8/9 triangle boundaries. It does not execute probes, generate route or byte streams, run OCR/image/stego/PGP/OutGuess/F5/StegDetect/CUDA/scoring/benchmarks, select targets, activate the canonical corpus, finalize page boundaries, or claim a solve.
<!-- stage6:end -->

<!-- stage6b:start -->
## Historical Stage 6B Boundary

At the time of Stage 6B, Stage 6B - Stage 6 diagnostic-readiness triage repair and hook stabilization, without execution was the latest completed stage.

The routed follow-up at that time was Stage 6C - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6B repaired Stage 6 probe-family/source/readiness metadata and made project-local Codex hooks report-only by default. It did not run probes, create the final Stage 7 manifest, create archives, execute tooling, generate route or byte streams, run CUDA/scoring/benchmarks, or make a solve claim.
<!-- stage6b:end -->

<!-- stage6c:start -->
## Historical Stage 6C Boundary

At the time of Stage 6C, Stage 6C - OUROBOROS / I=31 circumference / Page32 spiral geometry source-lock addendum, without execution was the latest completed stage.

Historical next routed work at Stage 6C closeout: Stage 6D - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6C source-locked the OUROBOROS/I31 circumference bridge as review-only metadata and preserved Stage 6B probe-map and hook repairs. It did not run probes, finalize Stage 7, create archives, generate route or byte streams, inspect images, run OCR/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6c:end -->

<!-- stage6d:start -->
## Historical Stage 6D Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution. Stage 6F repairs current-facing document integrity, hardens hook/preflight traceability, supersedes metadata-only traceability source dependency semantics, and keeps Stage 7 manifest work blocked until Stage 6G. It did not create a final Stage 7 manifest, run probes, generate result archives, execute routes or byte streams, run image/stego/OCR/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6d:end -->

<!-- stage6e:start -->
## Historical Stage 6E Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6E classified all stale-current warning-domain findings into named buckets, installed bounded report-only preprompt doc-staleness advisory behavior, source-locked finite bridge facts, superseded the stale Stage 6B Stage 6C token-block projection precondition, and built Stage 6F source-root/probe traceability inputs.

Stage 6E did not create a final Stage 7 manifest, finalize an archive-run contract, create a result archive, run probes, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6e:end -->

<!-- stage6f:start -->
## Historical Stage 6F Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6F repaired malformed/stale current mirrors, added file-content validators for high-risk docs, preserved Stage 6E source-lock payloads through a supersession layer, added preflight self-report exclusion, verified report-only hook behavior where local launcher tests can support it, recorded the Ciada/Cicada source-root alias policy, crosslinked the dju-bei backlog gap, and installed strict Codex acceptance criteria.

Stage 6F did not create a final Stage 7 manifest, finalize an archive-run contract, create result archives, run probes, add new theory records, add overlays, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6f:end -->

<!-- stage6g:start -->
## Historical Stage 6G Boundary

Historical completed stage at Stage 6G closeout: Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, hook confirmation, and acceptance-policy hardening, without execution.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution. Stage 6H is a dot-angle/right-triangle source-lock addendum because recent material remains chat-only pending source-lock. It is not final Stage 7 manifest work.

Future Codex work must apply `docs/onboarding/codex-acceptance-criteria.md`, review edited current-facing documents as whole final files, and keep all no-execution gates closed unless a later prompt explicitly opens them.
<!-- stage6g:end -->
