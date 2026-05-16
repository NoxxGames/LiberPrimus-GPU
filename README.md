# liberprimus-gpu

## Mission

`liberprimus-gpu` is a research workbench for future CUDA-accelerated Liber Primus cryptanalysis experiments. Stage 0A creates the repository structure, documentation, build system, smoke tests, and toolchain checks needed before any serious corpus work or cipher implementation begins.

## Non-goals for Stage 0A

- No Liber Primus page is claimed solved.
- No real corpus data is imported, transformed, or normalized.
- No cipher-solving logic, search campaign, or benchmark campaign is implemented.
- No generated experiment output is committed.
- No final Gematria rune table is frozen.

## Architecture summary

The CPU side owns corpus management, manifests, hypothesis generation, branching search, result provenance, and manual review. The GPU side will only accelerate large regular batches of transform-and-score work after a CPU reference implementation, parity tests, and benchmarks exist.

## Current status

Stage 1A solved-page golden fixtures. The repository has tutorials, non-canonical source ingestion tools, transcript-alignment scaffolding, frozen Stage 0E profiles, an inactive corpus candidate generator, and direct-translation fixture reproduction for selected known solved material. No canonical corpus is active and no unsolved page is claimed solved.

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

CUDA builds are optional in Stage 0A.

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

`data/raw/` is immutable. Do not overwrite raw evidence, normalize in place, or commit real raw corpus files in Stage 0A. Later corpus work must use explicit SHA-256 locks and transcript version metadata.

## Experiment policy

Experiments are manifest-driven. Candidate outputs must never be treated as solves without pinned corpus data, full transform chains, score metadata, null controls, reproducible tests, and manual review.

## Testing policy

Stage 0A requires smoke tests for the C++ skeleton and Python package. Future CUDA kernels must have CPU reference implementations, CPU/GPU parity tests, and benchmarks before optimization.

## Next milestones

Stage 1C should reproduce explicit-key Vigenere solved pages using the Stage 1A fixture framework, without key search.

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
