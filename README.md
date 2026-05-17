# liberprimus-gpu

[![CI](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml/badge.svg)](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml)

## Mission

`liberprimus-gpu` is a reproducible research workbench for conservative Liber Primus cryptanalysis experiments. The project keeps corpus provenance, solved baselines, transform metadata, run records, and CI gates ahead of any exploratory search or GPU acceleration work.

## Current boundaries and deferred work

These are not permanent project exclusions unless marked as safety rules. They describe the current implementation boundary after Stage 3A and the work that must stay bounded, reviewable, and reproducible before larger experiments begin. CUDA and broad campaigns are deferred, not permanently excluded.

### Permanent safety rules

- No generated output is a solve by itself.
- No Liber Primus page is claimed solved; material that is still unsolved must not receive a solve claim without a pinned corpus, manifest, transform chain, reproducible output, tests, and review.
- Raw data must not be overwritten or committed.
- Generated outputs and SQLite databases must not be committed.

### Current boundaries

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page search campaigns: not started.
- Scoring campaigns: not started; Stage 3A minimal triage scoring exists only for sorting one bounded 841-candidate CPU run.
- CUDA experiment campaigns: not started.
- Normal bounded local CPU experiments: allowed automatically when they pass `experiments/policies/operator-policy-v0.yaml`.
- Broad unsolved-page campaigns: not started.
- Approval packets: optional/high-risk audit tooling, not the default path for policy-passing bounded CPU items.
- Existing CUDA code is scaffold and smoke-test infrastructure only.

### Deferred future work

- Stronger scoring and null controls for bounded candidate review.
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

## Architecture summary

The CPU side owns corpus management, manifests, hypothesis generation, branching search, result provenance, and manual review. The GPU side will only accelerate large regular batches of transform-and-score work after a CPU reference implementation, parity tests, and benchmarks exist.

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
- Known solved baselines: `10` passing through the registry/manifest path.
- Fixture breakdown: direct translation `4`, Atbash-family `3`, explicit-key Vigenere `2`, p56 prime-minus-one / phi-prime `1`.
- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad search/scoring/CUDA campaigns: not started.
- Latest bounded run: Stage 3A executed `841` CPU candidates for one reviewable Caesar plus affine queue item; no solve claim.
- Next: Stage 3B inspect Stage 3A top candidates and queue the next bounded method or scoring refinement.

## CI status

GitHub Actions runs at [NoxxGames/LiberPrimus-GPU Actions](https://github.com/NoxxGames/LiberPrimus-GPU/actions). CI is raw-data-free, CUDA-free, secret-free, and does not upload generated corpus or result artifacts by default. Real-source smoke checks remain local-only because ignored raw sources are not present on GitHub-hosted runners.

## Tutorials

Start with `tutorials/README.md`. The tutorials cover Windows and Linux setup, local data handling, current CLI tools, transcript alignment, hardware expectations, and Codex-assisted development.

## GitHub wiki

Wiki source pages live under `docs/github/wiki-pages/`. The repository tutorials and docs are the source of truth; the GitHub wiki is a public mirror and must not contain raw data, generated dumps, or solve claims.

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

Stage 2J replaces per-experiment approval as the default path with the standing policy in `experiments/policies/operator-policy-v0.yaml` and the queue in `experiments/queues/stage2j-bounded-cpu-queue.yaml`. Normal local CPU items can run automatically when they stay within the hard limits: candidate upper bound `100000`, runtime estimate `600` seconds, generated output budget `250` MB, CPU only, no CUDA/cloud/paid services, no generated-output commit, no canonical corpus activation, no page-boundary finalization, and no solve claim.

The first Caesar plus affine reviewable-slice queue item has candidate upper bound `841` and is policy-eligible. Stage 3A adds the minimal CPU executor and deterministic triage scoring for that item. Full candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3a/`; committed research logs summarize counts and top score metadata only.

Stage 3B should inspect Stage 3A top candidates as leads and queue the next bounded method or scoring refinement. No Stage 3A output is a solve claim.

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
