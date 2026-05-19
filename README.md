# liberprimus-gpu

[![CI](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml/badge.svg)](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml)

## Mission

`liberprimus-gpu` is a reproducible research workbench for conservative Liber Primus cryptanalysis experiments. The project keeps corpus provenance, solved baselines, transform metadata, run records, and CI gates ahead of any exploratory search or GPU acceleration work.

## Current boundaries and deferred work

These are not permanent project exclusions unless marked as safety rules. They describe the current implementation boundary after Stage 4E source-lock delta audit infrastructure. Future experiments must stay bounded, reviewable, and reproducible before larger campaigns begin. CUDA and broad campaigns are deferred, not permanently excluded.

### Permanent safety rules

- No generated output is a solve by itself.
- No Liber Primus page is claimed solved; material that is still unsolved must not receive a solve claim without a pinned corpus, manifest, transform chain, reproducible output, tests, and review.
- Raw data must not be overwritten or committed.
- Generated outputs and SQLite databases must not be committed.

### Current boundaries

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page search campaigns: not started.
- Scoring campaigns: not started; Stage 3A/3B minimal triage scoring exists only for sorting and inspecting bounded 841-candidate CPU runs, Stage 3C calibration uses small local controls only, Stage 3D applies that scorer to a four-key explicit Vigenere preview only, Stage 3F applies it to the bounded 48-candidate LP evidence-key Vigenere pack only, Stage 3G applies it to a bounded 256-candidate p56-local prime-minus-one offset sweep only, Stage 3H applies it to a bounded 64-candidate reset/advance ablation with 100 negative controls only, Stage 3I applies it to a bounded 56-candidate historical motif Vigenere pack only, Stage 3J applies it to a bounded 192-candidate Mersenne/perfect-number stream probe only, and Stage 3S applies it to the bounded 72-candidate Onion 7 explicit seed pack only.
- Visual/image-derived observations: registry and deterministic feature summaries only, plus deterministic review transforms; Stage 3K records source locks and reviewable observations, Stage 3M records deterministic local image features, and Stage 3P generates ignored review transforms/contact sheets. No image-derived text experiments are executed.
- Cookie/hash preimage work: Stage 3L tests two explicit SHA-256 packs only, and Stage 3U tests the manifest-declared signed/public string variant pack only. Both use exact byte-string logging with no fuzzy, partial, dictionary, GPU, or solve claims.
- Stego/OutGuess work: Stage 3V adds a deterministic OutGuess regression harness only. Missing tools/assets are explicit skipped outcomes, generated payloads stay ignored, and no broad image scan or payload interpretation is performed.
- Discord source discovery: Stage 3N scans admin-provided local HTML exports only and commits aggregate/redacted records only. Stage 3O promotes a bounded, public-safe subset of redacted source-discovery records. Stage 3Q builds ignored redacted topic shards for local AI/deep-research review. Stage 3R audits those leads, promotes only corroborated public/source-observation records, preserves false positives as negative controls, and queues disabled post-Discord manifests. Raw logs, message bodies, usernames, and private attachment URLs are not committed.
- Full Discord review bundles: Stage 4A builds redacted chronological streams, channel shards, topic shards, indexes, an LP page gallery, and an SFTP-ready static site under ignored paths for Deep Research handoff. Raw Discord logs, usernames, user IDs, message IDs, private URLs, generated static site files, copied LP page images, thumbnails, archives, and generated bundle outputs are not committed.
- Source-lock and visual observation intake: Stage 4B promotes allowlisted public-source records only, records source-health metadata, preserves cuneiform/delimiter/dot/number-square/cookie observations as review-only and non-canonical, and stores false-positive classes as negative controls. No Stage 4B visual observation is an experiment seed.
- Visual annotation: Stage 4C creates cuneiform, delimiter, dot-pattern, number-square-reference, and visual negative-control annotation tasks plus a generated local annotation site and blank coordinate templates. Coordinates and readings are separate; no Stage 4C visual task is verified, canonical, or usable as an experiment seed.
- Bounded numeric verification: Stage 4D runs only no-fudge numeric and metadata audits. GP/rune batch002 skips without exact new spans, number-square routes skip without locked raw values, delimiter/dot audits infer no meaning, cuneiform seed execution remains deferred, and cookie pack v2 is deferred to a future explicit stage.
- Source-delta audits: Stage 4E records selected `cicada-solvers/iddqd` tree metadata only. It does not blind-mirror external repositories, commit raw images/audio/fonts/binaries, run stego tools, or infer meaning from compression artefacts.
- Post-Discord experiment execution: Stage 3S executes only `EXP-3R-003`, the bounded Onion 7 explicit seed pack. Stage 3T executes only `EXP-3R-004`, the GP/rune claim verifier. Stage 3U executes only `EXP-3R-001`, the cookie SHA-256 signed-variant pack. All keep generated records under ignored paths and make no solve claim.
- CUDA experiment campaigns: not started.
- Normal bounded local CPU experiments: allowed automatically when they pass `experiments/policies/operator-policy-v0.yaml`.
- Broad unsolved-page campaigns: not started.
- Approval packets: optional/high-risk audit tooling, not the default path for policy-passing bounded CPU items.
- Existing CUDA code is scaffold and smoke-test infrastructure only.

### Deferred future work

- Stage 4F historical OutGuess/audio fixture source-locking, using Stage 4E metadata.
- Later cookie exact-candidate refresh.
- Later CPU batch transform API extraction.
- Future visual numeric observations for base-60 or cuneiform-like numbers, binary dot patterns, symmetry/asymmetry, and page imagery must remain reviewable before becoming experiment seeds.
- Search campaigns.
- CUDA kernels after CPU references and parity tests exist.
- Benchmark campaigns after stable CPU/GPU baselines exist.

### Already implemented since Stage 0A

- Profile and corpus-candidate infrastructure.
- Ten known solved baseline fixtures.
- CPU transform registry.
- Solved-baseline manifest runner.
- JSONL/SQLite result-store foundation.
- Raw-data-free GitHub Actions CI.
- CI-gated consistency checks.
- CPU exploratory experiment dry-run planner.
- Bounded CPU execution harness for synthetic and solved-fixture-only runs.
- Exploratory experiment proposal and human-approval workflow.
- Approval-gated execution path for approved synthetic/solved controls.
- First real bounded exploratory approval-readiness packet.
- Standing bounded local CPU operator policy and queue scaffold.
- Minimal CPU Caesar plus affine executor and triage scoring for the first `841` candidate bounded queue item.
- Candidate lead inspection, refined triage scoring, reranking, and reverse-direction bounded comparison.
- Scoring calibration with positive controls, null controls, negative controls, tiny crib checks, and a conservative Stage 3D queue recommendation.
- Small explicit-key Vigenere preview for the four declared known-motif keys, with calibrated scoring and ignored generated outputs.
- Deep Research method backlog ingestion, deterministic Stage 3E queue counts, and dry-run executor-support classification.
- Reset/advance-aware Stage 3F LP evidence-key Vigenere pack executor and 48-candidate run.
- Bounded Stage 3G p56-local prime-minus-one offset sweep executor and 256-candidate run, plus a queued future Mersenne/perfect-number probe.
- Shared Stage 3H reset/advance state machine, 64-candidate ablation run, and 100 family-specific negative controls.
- Bounded Stage 3I historical motif Vigenere pack run for 14 declared keys and 56 candidates.
- Bounded Stage 3J Mersenne/perfect-number stream probe for the finite declared exponent sequence and 192 candidates.
- Stage 3K historical archive/source-lock, local image metadata, visual numeric observation, and cookie/hash artefact registry.
- Stage 3L bounded SHA-256 cookie-hash preimage packs for the two archived 2013 cookie artefacts.
- Stage 3M deterministic local image-analysis CLI and visual-feature summaries.
- Stage 3N admin-approved Discord HTML archive ingestion and source-discovery index.
- Stage 3O privacy-preserving Discord source promotion, expanded tutorials, and GitHub Wiki mirror source generation.
- Stage 3P deterministic image transform suite, contact sheets, and local visual review index.
- Stage 3Q redacted Discord AI-review bundles and topic shards.
- Stage 3R Discord lead promotion audit, negative controls, and first disabled post-Discord experiment manifests.
- Stage 3S bounded Onion 7 explicit seed-pack execution.
- Stage 3T bounded GP/rune claim verifier execution.
- Stage 3U bounded cookie SHA-256 signed-variant pack execution.
- Stage 3V OutGuess regression harness.
- Stage 3W project-state consolidation and anti-drift checks.
- Stage 3X CLI modularisation without behavior change.
- Stage 3Y result synthesis, staged plan, and method-retirement ledger.
- Stage 3Z source-of-truth / newcomer map.
- Stage 4A full Discord research-bundle extraction and static review site generation.
- Stage 4B website-derived source-lock triage and visual observation intake.
- Stage 4C cuneiform and dot annotation pack.
- Stage 4D bounded numeric verifier pack.
- Stage 4E cicada-solvers/iddqd source-lock delta audit.

## Architecture summary

The CPU side owns corpus management, manifests, hypothesis generation, branching search, result provenance, and manual review. The GPU side will only accelerate large regular batches of transform-and-score work after a CPU reference implementation, parity tests, and benchmarks exist.

## Where To Start

- [Start Here](docs/onboarding/start-here.md): plain-English current-state overview.
- [Source Of Truth Map](docs/onboarding/source-of-truth-map.md): which file answers which question.
- [Staged Plan](docs/roadmap/staged-plan.md): completed stages, current direction, planned work, deferred work, and method-retirement context.
- [Tutorial Index](tutorials/README.md): public workflow guides.

## Current status

Current status:

- Stage 2A: CPU transform registry and manifest-addressable solved-baseline runner complete.
- Stage 2B: JSONL/SQLite experiment result-store foundation complete.
- Stage 2C: raw-data-free GitHub Actions CI complete and lock-hash hardened.
- Stage 2D: CI-gated schema/docs consistency and manifest/result-store hardening complete.
- Stage 2E: CPU exploratory experiment manifest scaffold and dry-run planner complete.
- Stage 2F: bounded CPU execution harness for synthetic and solved-fixture-only runs complete.
- Stage 2G: exploratory experiment proposal and human-approval workflow complete.
- Stage 2H: approval-gated execution path for approved synthetic/solved controls complete.
- Stage 2I: first real bounded CPU exploratory experiment approval packet complete.
- Stage 2J: standing bounded CPU auto-run policy and queue scaffold complete.
- Stage 3A: minimal CPU Caesar plus affine executor and triage scoring complete.
- Stage 3B: Stage 3A lead inspection, scoring refinement, rerank, and reverse-direction comparison complete.
- Stage 3C: scoring calibration, null controls, positive controls, and tiny crib checks complete.
- Stage 3D: small Vigenere known-motif key-list preview complete.
- Stage 3E: Deep Research method backlog ingestion and bounded queue dry-run complete.
- Stage 3F: LP evidence-key Vigenere pack execution complete.
- Stage 3G: p56-local prime-minus-one offset sweep complete.
- Stage 3H: reset/advance ablation and family-specific negative controls complete.
- Stage 3I: historical motif Vigenere key-pack run complete.
- Stage 3J: Mersenne/perfect-number tiny stream probe complete.
- Stage 3K: archive and visual observation registry complete.
- Stage 3L: bounded cookie-hash preimage packs complete.
- Stage 3M: deterministic local image analysis complete.
- Stage 3N: admin-approved Discord HTML archive ingestion complete.
- Stage 3O: Discord source promotion and Wiki tutorial mirror complete.
- Stage 3P: deterministic image transform suite and visual review index complete.
- Stage 3Q: redacted Discord AI-review bundles and topic shards complete.
- Stage 3R: Discord lead promotion audit and first post-Discord manifest queue complete.
- Stage 3S: bounded Onion 7 explicit seed-pack execution complete.
- Stage 3T: bounded GP/rune claim verifier execution complete.
- Stage 3U: bounded cookie SHA-256 signed-variant pack execution complete.
- Stage 3V: OutGuess regression harness complete.
- Stage 3W: state consolidation and anti-drift hardening complete.
- Stage 3X: CLI modularisation without behavior change complete.
- Stage 3Y: result synthesis, staged plan, and method-retirement ledger complete.
- Stage 3Z: source-of-truth / newcomer map complete.
- Stage 4A: full Discord research-bundle extraction for Deep Research complete.
- Stage 4B: website-derived source-lock triage and visual observation intake complete.
- Stage 4C: cuneiform and dot annotation pack complete.
- Stage 4D: bounded numeric verifier pack complete.
- Stage 4E: cicada-solvers/iddqd source-lock delta audit complete.
- Known solved baselines: `10` passing through the registry/manifest path.
- Fixture breakdown: direct translation `4`, Atbash-family `3`, explicit-key Vigenere `2`, p56 prime-minus-one / phi-prime `1`.
- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad search/scoring/CUDA campaigns: not started.
- Latest bounded hash review: Stage 3L tested `1809` deduplicated SHA-256 candidate byte strings against the two archived cookie/hash targets for `3618` exact comparisons and found `0` exact matches; no solve claim.
- Latest image-analysis stage: Stage 3M analysed `58` ignored local page images, producing `406` component records, `58` symmetry records, `464` bitplane records, and `71` review-only feature candidates in ignored outputs. No OCR, AI/ML interpretation, image-derived search, or solve claim is made.
- Latest source-discovery stage: Stage 3O promoted `500` public source links, `200` method-claim candidates, and `200` numeric-observation candidates from the Stage 3N extraction into redacted review records. It rejected private/unsafe links, expanded public tutorials, and generated Wiki source pages. Raw Discord logs, message bodies, usernames, private URLs, and generated review indexes remain uncommitted; no solve claim.
- Latest visual review stage: Stage 3P processed `58` ignored local page images, emitted `2077` derived review images, `59` contact sheets, `58` review pages, and `6` review-only visual transform candidates under ignored outputs. No OCR, AI/ML interpretation, image-derived search, or solve claim is made.
- Latest Discord review stage: Stage 3Q generated `1700` redacted stream records, `17` topic shard files, and `900` review leads under ignored outputs, with an aggregate-only committed summary. Raw logs, message bodies, usernames, private URLs, AI upload, live API use, scraping, and solve claims remain absent.
- Latest Discord promotion stage: Stage 3R promoted `13` public source records and `11` review-only observation records, preserved `11` negative-control records, counted `25` unsafe/private or quarantined records, and created `3` disabled post-Discord manifests. No experiment was executed and no solve claim was made.
- Latest post-Discord experiment stage: Stage 3S executed `EXP-3R-003` only, producing `72` bounded Onion 7 candidates from `3` value spaces, `6` routes, `2` directions, and `2` reset modes. The top candidate scored `1.460714` with calibrated confidence `inconclusive`; generated outputs remain ignored and no solve claim is made.
- Latest GP/rune verifier stage: Stage 3T executed `EXP-3R-004` only, loading and deduplicating `25` exact claims. It classified `23` as verified and `2` as unsupported, with no unverified, boundary-sensitive, missing-source-span, malformed, or duplicate claims in the committed input set.
- Latest cookie signed-variant stage: Stage 3U executed `EXP-3R-001` only, generating `156` candidates before deduplication, testing `105` deduplicated byte strings against `2` cookie targets for `210` exact SHA-256 comparisons, and finding `0` exact matches.
- Latest stego regression stage: Stage 3V added the OutGuess harness, detected no local OutGuess binary, and recorded `6` missing-tool skips plus `1` disabled case across `7` manifest cases. No raw artefacts or payloads were committed.
- Latest consolidation stage: Stage 3W refreshed persistent project context, defined the source-of-truth hierarchy, and added anti-drift checks so long-lived docs cannot drift back to obsolete current-state claims.
- Latest maintainability stage: Stage 3X split the Python CLI into `cli_commands` domain modules while preserving `python -m libreprimus.cli` and adding command-surface tests.
- Latest synthesis stage: Stage 3Y added `docs/roadmap/staged-plan.md`, research synthesis records, method-family status and retirement ledgers, Deep Research influence records, direction-change records, and validation CLI commands.
- Latest onboarding stage: Stage 3Z added source-of-truth, Codex navigation, Deep Research handoff, contributor module, task-lane, and private/generated data maps.
- Latest Deep Research handoff stage: Stage 4A processed `43` local ignored Discord HTML exports into `520009` redacted messages, `1327` channel shards, `12` topic shards, and an ignored SFTP-ready static review site with `58` LP page images included as generated gallery assets. Raw logs, raw images, private URLs, and generated outputs remain uncommitted.
- Latest source-lock stage: Stage 4B promoted `20` allowlisted public source records, recorded `19` source-health records, added `6` review-only visual observations and `17` negative controls, and queued `7` disabled future manifests. No experiments were executed and no solve claim is made.
- Latest annotation stage: Stage 4C created `15` visual annotation tasks, including `1` cuneiform task, `1` dot task, `2` delimiter tasks, and `10` visual negative-control tasks. Generated annotation outputs remain ignored and no visual meaning is inferred.
- Latest bounded numeric stage: Stage 4D discovered `7` manifests, audited `3`, deferred or skipped `4`, verified `0` GP/rune claims because no exact new spans were present, audited `2` delimiter observations and `10` visual negative controls, skipped number-square routes because raw values are not locked, and deferred cuneiform/cookie execution.
- Latest source-delta stage: Stage 4E inspected `310` public `cicada-solvers/iddqd` tree paths, recorded `1` source-delta record, `12` source-health records, `1` image artefact future-preflight record, and `4` disabled future manifests without committing raw artefacts.
- Durable staged plan: [`docs/roadmap/staged-plan.md`](docs/roadmap/staged-plan.md).
- Next: Stage 4F historical OutGuess/audio fixture source-locking.

## How To Use This Repo

1. Set up Python 3.12 and a local virtual environment using the [Windows](tutorials/02-windows-setup.md) or [Linux](tutorials/03-linux-setup.md) tutorial.
2. Run the local validation stack before trusting a change:

```powershell
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

3. Keep local raw material local. Raw Discord logs, page images, transcript drops, workbooks, and Pastebin files are ignored by design.
4. Use generated outputs for local review only. Candidate dumps, image-analysis records, Discord extraction JSONL, SQLite databases, and local review indexes must not be committed.
5. Start with the [tutorial index](tutorials/README.md) for repo tours, solved baselines, bounded queues, image analysis, Discord archive ingestion, and source/observation registry workflows.
6. The GitHub Wiki mirrors tutorial pages for public browsing, but repository tutorial files are the source of truth.

Safe bounded CPU experiments use `experiments/policies/operator-policy-v0.yaml`; they remain CPU-only, budget-limited, and unable to claim solves. CUDA work waits for CPU references, parity tests, and explicit future scope.

## CI status

GitHub Actions runs at [NoxxGames/LiberPrimus-GPU Actions](https://github.com/NoxxGames/LiberPrimus-GPU/actions). CI is raw-data-free, CUDA-free, secret-free, and does not upload generated corpus or result artifacts by default. Real-source smoke checks remain local-only because ignored raw sources are not present on GitHub-hosted runners.

## Tutorials

Start with `tutorials/README.md`. The tutorials cover Windows and Linux setup, local data handling, current CLI tools, transcript alignment, hardware expectations, and Codex-assisted development.

## GitHub wiki

Wiki source pages live under `docs/wiki-source/` and are generated from `tutorials/`. The repository tutorials and docs are the source of truth; the GitHub wiki is a public mirror and must not contain raw data, generated dumps, or solve claims. Use `scripts/github/validate-wiki-source.ps1` and `scripts/github/sync-tutorials-to-wiki.ps1 --DryRun` before publishing.

## Issues and backlog

Issue templates live under `.github/ISSUE_TEMPLATE/`. Seed issues for future work live under `docs/github/issues/` and can be created idempotently with `scripts/github/create-issues.ps1`.

## Public-readiness status

The project is public-readable for documentation and scaffold review. It is not ready for unsolved-page cryptanalysis campaigns, canonical corpus release, or GPU acceleration claims.

## Quick start on Windows

```powershell
.\scripts\verify-toolchain.ps1
.\scripts\configure-windows.ps1
cmake --build build\msvc-debug
ctest --test-dir build\msvc-debug --output-on-failure
```

For Python:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\libreprimus.exe smoke
```

## Toolchain requirements

- Windows 11 or compatible Windows 10 development host.
- Git for Windows.
- CMake 3.26 or newer.
- Ninja.
- Python >=3.12,<3.14, with Python 3.12 preferred.
- Visual Studio 2022 Build Tools with the Desktop C++ workload.
- Optional CUDA Toolkit for CUDA smoke builds.

## Configure and build CPU-only

```powershell
cmake -S . -B build\msvc-debug -G Ninja -DCMAKE_BUILD_TYPE=Debug -DLPGPU_ENABLE_CUDA=OFF -DLPGPU_BUILD_TESTS=ON
cmake --build build\msvc-debug
ctest --test-dir build\msvc-debug --output-on-failure
```

If `cl.exe` is not visible in the current shell, run through `scripts\configure-windows.ps1`, which locates `VsDevCmd.bat`.

## Configure and build with CUDA

CUDA builds remain optional and are scaffold/smoke only at the current stage.

```powershell
cmake -S . -B build\cuda-debug -G Ninja -DCMAKE_BUILD_TYPE=Debug -DLPGPU_ENABLE_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DLPGPU_BUILD_TESTS=ON
cmake --build build\cuda-debug
ctest --test-dir build\cuda-debug --output-on-failure
```

## Python environment setup

The Python package exposes smoke/toolchain commands plus legacy ingestion, transcript alignment, profile validation, corpus-candidate generation, and solved-fixture reproduction.

Direct fixture smoke:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture stage1a-smoke --fixture-dir data/fixtures/solved-pages/direct-translation-v0 --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate --out-dir data/normalized/solved-baselines/direct-translation-v0 --allow-pending --allow-warnings
```

All-known solved-baseline registry smoke:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-baseline stage2a-smoke --manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml --out-dir experiments/results/solved-baselines/stage2a --allow-warnings
```

Stage 2B result-store smoke:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store stage2b-smoke --solved-baseline-manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml --result-store-manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml --solved-baseline-out-dir experiments/results/solved-baselines/stage2a --result-store-out-dir experiments/results/result-store/stage2b --replace --allow-warnings
```

Local Stage 2C CI reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
```

## Repository map

- `src/`: C++20 native scaffold.
- `cuda/`: optional CUDA smoke scaffold.
- `python/`: Python orchestration package.
- `tests/`: C++ and Python smoke tests.
- `data/`: immutable raw-data placeholders and future corpus areas.
- `experiments/`: manifest-driven experiment policy and smoke manifest.
- `docs/`: methodology, CUDA, corpus, scoring, and Codex notes.
- `scripts/`: Windows verification, bootstrap, configure, cleanup, and GitHub helper scripts.
- `tutorials/`: public user-facing tutorials.
- `.github/`: issue templates and pull request template.

## Data policy

`data/raw/` is immutable. Do not overwrite raw evidence, normalize in place, or commit real raw corpus files. Corpus work must use explicit SHA-256 locks and transcript version metadata.

## Experiment policy

Experiments are manifest-driven. Candidate outputs must never be treated as solves without pinned corpus data, full transform chains, score metadata, null controls, reproducible tests, and manual review.

## Testing policy

Current tests cover the C++ skeleton, Python package, manifests, schemas, result stores, lock hashes, public documentation status, and consistency gates. Future CUDA kernels must have CPU reference implementations, CPU/GPU parity tests, and benchmarks before optimization.

## Next milestones

Stage 2J replaced per-experiment approval as the default path with the standing policy in `experiments/policies/operator-policy-v0.yaml` and the queue in `experiments/queues/stage2j-bounded-cpu-queue.yaml`. Normal local CPU items can run automatically when they stay within the hard limits: candidate upper bound `100000`, runtime estimate `600` seconds, generated output budget `250` MB, CPU only, no CUDA/cloud/paid services, no generated-output commit, no canonical corpus activation, no page-boundary finalization, and no solve claim.

The first Caesar plus affine reviewable-slice queue item has candidate upper bound `841` and is policy-eligible. Stage 3A adds the minimal CPU executor and deterministic triage scoring for that item. Full candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3a/`; committed research logs summarize counts and top score metadata only.

Stage 3B inspected Stage 3A top candidates, refined the scorer, reranked the 841 candidates, and ran the reverse-direction comparison. Both refined and reverse-direction top leads remain `noisy`.

Stage 3C calibrated scoring against positive solved-fixture controls, deterministic null controls, negative controls, and tiny crib checks. Stage 3D ran the conservative small Vigenere known-motif key-list preview for exactly four declared keys. The top key was `LIBER`, calibrated as `noisy`.

Stage 3E ingests the Deep Research method backlog, commits `experiments/queues/stage3e-method-backlog.yaml` and `experiments/queues/stage3e-bounded-cpu-queue.yaml`, and dry-runs bounded methods with deterministic counts: LP evidence Vigenere `48`, p56 local prime-minus-one offsets `256`, historical Vigenere `56`, family-specific negative controls `100`, reset/advance ablation `64`, prime mod/gap `256`, and Mersenne/perfect-number probe `192`.

Stage 3F implements the reset/advance-aware evidence-key Vigenere pack executor and runs only `stage3e_vig_lp_evidence_pack_v1`. It executes `48` candidates, records key/reset/advance metadata, leaves generated outputs ignored, and makes no solve claim.

Stage 3G implements the p56-local prime-minus-one offset sweep executor and runs only `stage3e_prime_minus_one_offsets_v1`. It executes `256` candidates, records offset/direction/reset metadata, leaves generated outputs ignored, adds a future `192` candidate Mersenne/perfect-number probe to the queue without executing it, and makes no solve claim.

Stage 3H implements the shared reset/advance state machine and runs only `stage3h_reset_advance_ablation_v1`. It executes `64` bounded candidates across Vigenere and prime-stream adapters, records reset/advance and metadata-support status, writes `100` ignored family-specific negative controls, and makes no solve claim.

Stage 3I reuses the bounded Vigenere key-pack executor and runs only `stage3e_vig_history_key_pack_v1`. It executes `56` candidates for the 14 declared historical motif keys across reset modes `none` and `line` and advance modes `runes_only` and `token_break_preserving`. The top key `SELFRELIANCE` remains calibrated `noisy`; generated outputs stay ignored and no solve claim is made.

Stage 3J implements the bounded Mersenne/perfect-number stream probe and runs only `stage3j_mersenne_prime_stream_tiny_v1`. It executes `192` candidates from the finite declared exponent sequence, reports `96` duplicate stream signatures, leaves generated outputs ignored, and makes no solve claim.

## Stage 1B Atbash-Family Fixtures

The workbench now includes known-solved reverse Gematria and rotated reverse Gematria reproduction fixtures. These run through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture stage1b-smoke `
  --direct-fixture-dir data/fixtures/solved-pages/direct-translation-v0 `
  --atbash-fixture-dir data/fixtures/solved-pages/atbash-family-v0 `
  --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate `
  --direct-out-dir data/normalized/solved-baselines/direct-translation-v0 `
  --atbash-out-dir data/normalized/solved-baselines/atbash-family-v0 `
  --allow-pending `
  --allow-warnings
```

These fixtures are regression baselines, not new solve claims. Generated outputs remain ignored, and `canonical_corpus_active=false`.
## Stage 1C Vigenere Baselines

Stage 1C adds explicit-key Vigenere known-solved fixture reproduction for `DIVINITY` and `FIRFUMFERENFE`, plus reference-source locks for selected `scream314/cicada3301` and `lipeeeee/gematria` files. These are provenance and test fixtures only: no new page is solved, no key search is implemented, and `canonical_corpus_active=false` remains required.

## Stage 1D Prime-Stream Baseline

Stage 1D adds p56 `An End` known-solved reproduction using a CPU-only `prime_minus_one_stream` transform with `phi_prime_stream` recorded as an equivalent alias for prime inputs. The p56 hex block is preserved as a payload check, not merged into plaintext. No prime-stream search, scoring, CUDA, or corpus activation is implemented.

## Stage 2B Result Store

Stage 2B adds generated JSONL and SQLite result stores for solved-baseline regression imports. Run records preserve manifest SHA-256, registry SHA-256, git commit, profile/source provenance, and explicit false flags for canonical corpus activation, page-boundary finalization, search, scoring, CUDA, and canonical trust. Generated result-store outputs under `experiments/results/result-store/` remain ignored and are not publication artifacts.

## Stage 2C CI

Stage 2C adds `.github/workflows/ci.yml` plus local scripts under `scripts/ci/`. CI is raw-data-free, CUDA-free, secret-free, and does not upload generated corpus or result artifacts by default. The Python job runs Ruff, pytest, package smoke, transform-registry validation, solved-baseline manifest validation, and result-store manifest validation.
