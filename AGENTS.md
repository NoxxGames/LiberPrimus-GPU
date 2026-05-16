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

Stage 0D adds non-canonical transcript alignment and canonical transcript policy scaffolding on top of Stage 0C Pastebin ingestion.

## Source-of-truth files

Use `README.md`, `ARCHITECTURE.md`, `DATASET.md`, `EXPERIMENTS.md`, `CUDA_NOTES.md`, `RESULTS_SCHEMA.md`, and `STATUS.md` as persistent context.

## Corpus immutability rules

Raw source material belongs under `data/raw/` only when explicitly allowed by a later stage. Never normalize, patch, crop, OCR, transcribe, or deduplicate raw files in place.

Legacy workbook files under `data/raw/legacy-workbooks/` are immutable raw artefacts and must remain ignored by Git.

Legacy Pastebin files under `data/raw/legacy-pastebins/` are immutable raw artefacts and must remain ignored by Git.

Transcript files under `data/raw/transcripts/` are immutable raw artefacts and must remain ignored by Git.

## Coding standards

Prefer small, explicit modules with clear provenance boundaries. Avoid clever transformations without tests and documentation.

## C++ standards

Use C++20, namespace all project code under `libreprimus`, and keep Stage 0A code dependency-free.

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

## Prohibited actions

Do not download real corpus data in Stage 0A. Do not run brute force, long benchmarks, CUDA stress tests, or unbounded searches. Do not print secrets or credential-bearing environment variables.

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

## Public Documentation Wording Rules

- Do not use ambiguous non-goals wording for deferred roadmap work.
- README must not use a top-level `## Non-goals` section for temporary implementation boundaries.
- Use `Current boundaries and deferred work` for temporary public README boundaries.
- Public docs must distinguish permanent safety rules, current implementation boundaries, deferred future work, and completed work.
- README status and boundary sections must be updated when stages complete.
- Do not leave old Stage 0A boundary wording in top-level public documentation after later infrastructure stages implement parts of that work.
