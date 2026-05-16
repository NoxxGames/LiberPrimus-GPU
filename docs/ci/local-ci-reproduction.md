# Local CI Reproduction

## Purpose

These commands reproduce the Stage 2C CI checks without requiring raw data, CUDA, secrets, or generated result artifacts.

## Windows PowerShell Commands

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
.\scripts\ci\run-consistency-checks.ps1
.\scripts\ci\validate-workflow-static.ps1
.\scripts\ci\verify-lock-hashes.ps1
```

After a workflow push:

```powershell
.\scripts\ci\verify-remote-workflow.ps1 -RepoOwner NoxxGames -RepoName LiberPrimus-GPU -Branch main -WorkflowPath ".github/workflows/ci.yml"
```

## Linux Shell Commands

```bash
bash scripts/ci/run-python-ci.sh
bash scripts/ci/run-schema-manifest-checks.sh
bash scripts/ci/run-consistency-checks.sh
bash scripts/ci/validate-workflow-static.sh
bash scripts/ci/verify-lock-hashes.sh
```

After a workflow push:

```bash
bash scripts/ci/verify-remote-workflow.sh --repo-owner NoxxGames --repo-name LiberPrimus-GPU --branch main --workflow-path .github/workflows/ci.yml
```

## Python Test Commands

```powershell
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli smoke
```

## Schema And Manifest Validation Commands

```powershell
.\.venv\Scripts\python.exe scripts\ci\repair-canonical-json-locks.py --check
.\.venv\Scripts\python.exe -m libreprimus.cli profile summary
.\.venv\Scripts\python.exe -m libreprimus.cli transform-registry validate --registry data/transform-registry/cpu-reference-transforms-v0.json
.\.venv\Scripts\python.exe -m libreprimus.cli solved-baseline validate-manifest --manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-manifest --manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings
```

## Workflow Static Validation

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python/test_stage2c_workflow_static.py
```

The static test parses `.github/workflows/ci.yml`, verifies trigger and job structure, and rejects flattened one-line workflow formatting.

Remote workflow verification fetches the public raw workflow URL and rejects minified files, missing required commands, raw-data references, secrets, artifact uploads, and CUDA enablement.

## Optional CMake CPU Commands

On single-config generators:

```bash
cmake -S . -B build/ci-cpu -DCMAKE_BUILD_TYPE=Release -DLPGPU_ENABLE_CUDA=OFF -DLPGPU_BUILD_TESTS=ON
cmake --build build/ci-cpu --parallel
ctest --test-dir build/ci-cpu --output-on-failure
```

On Visual Studio multi-config generators, pass the build/test configuration:

```powershell
cmake -S . -B build\ci-cpu -DLPGPU_ENABLE_CUDA=OFF -DLPGPU_BUILD_TESTS=ON
cmake --build build\ci-cpu --config Debug --parallel
ctest --test-dir build\ci-cpu -C Debug --output-on-failure
```

## Common Failures

- Missing development dependencies: rerun `python -m pip install -e ".[dev]"`.
- Real-source tests fail instead of skip: verify the test guards only require raw files when they exist locally.
- CTest says configuration is missing: add `-C Debug` or `-C Release` for Visual Studio builds.

## Raw-Data Expectations

CI commands do not require files under ignored raw-data locations. They should pass on a clean checkout.
