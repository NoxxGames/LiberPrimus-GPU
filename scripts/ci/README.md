# CI Scripts

These scripts reproduce the Stage 2C GitHub Actions checks locally.

- `run-python-ci.ps1` / `run-python-ci.sh`: Ruff, pytest, and the Python smoke command.
- `run-schema-manifest-checks.ps1` / `run-schema-manifest-checks.sh`: raw-data-free profile, registry, solved-baseline manifest, and result-store manifest validation.

They do not require raw transcript files, CUDA, GitHub credentials, secrets, or generated result-store outputs.
