# Local CI Reproduction

## Purpose

These commands reproduce the Stage 2C CI checks without requiring raw data, CUDA, secrets, or generated result artifacts.

## Windows PowerShell Commands

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
```

## Linux Shell Commands

```bash
bash scripts/ci/run-python-ci.sh
bash scripts/ci/run-schema-manifest-checks.sh
```

## Python Test Commands

```powershell
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli smoke
```

## Schema And Manifest Validation Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli profile summary
.\.venv\Scripts\python.exe -m libreprimus.cli transform-registry validate --registry data/transform-registry/cpu-reference-transforms-v0.json
.\.venv\Scripts\python.exe -m libreprimus.cli solved-baseline validate-manifest --manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-manifest --manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml
```

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
