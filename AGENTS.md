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

Current completed stage: Stage 3X - CLI modularisation without behaviour change.

Current work: Stage 3Y - result synthesis and method-retirement ledger. Stage 3Y should synthesize existing results and retire or defer methods; it must not run new experiments, process raw data, change CUDA behavior, activate the canonical corpus, finalize page boundaries, or claim a solve unless explicitly scoped by a later prompt.

Current project state:

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page campaigns: not started.
- CUDA: deferred until CPU references, stable scorer definitions, batch APIs, parity tests, and benchmarks exist.
- Existing CUDA code: scaffold/smoke infrastructure only unless code and tests say otherwise.
- Raw data, generated outputs, SQLite databases, raw Discord logs, raw page images, raw historical stego artefacts, extracted payloads, and local deep-research reports are not committed.
- No solve claims are present.

## Source-of-truth files

Use `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` as primary operational truth. Use `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `DATASET.md`, `RESEARCH.md`, and `CIPHER_CATALOG.md` as research/workflow truth. Use `ARCHITECTURE.md`, `CUDA_NOTES.md`, `docs/architecture/**`, and `docs/ci/**` as architecture/CI truth. Tutorials and `docs/wiki-source/**` are public guidance; repository tutorials remain the source of truth and Wiki pages are mirrors.

When stage status changes, update `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` together. Long-lived operational docs must not describe obsolete stages as the current state. Historical references are allowed when clearly archival; do not rewrite `docs/development-logs/**` or `research-log/**` merely because they mention older stages.

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

## Stage 3V OutGuess Regression Rules

- OutGuess extraction outputs and payloads are generated and must not be committed.
- Missing OutGuess binary is not a failure when `--allow-missing-tool` is set.
- Missing historical assets are not a failure when `--allow-missing-assets` is set.
- Do not infer hidden meaning from non-empty payloads without expected hash and source validation.
- Do not run broad stego scans by default.
- Do not process raw Discord logs during stego stages.
- Raw historical artefacts under `third_party/CicadaArchive/` and `third_party/CicadaOutGuess/` must remain ignored except README and `.gitkeep`.

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
