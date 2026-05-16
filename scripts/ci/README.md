# CI Scripts

These scripts reproduce the Stage 2C GitHub Actions checks locally.

- `run-python-ci.ps1` / `run-python-ci.sh`: Ruff, pytest, and the Python smoke command.
- `run-schema-manifest-checks.ps1` / `run-schema-manifest-checks.sh`: raw-data-free profile, registry, solved-baseline manifest, and result-store manifest validation.
- `validate-workflow-static.ps1` / `validate-workflow-static.sh`: static GitHub Actions workflow validation.
- `verify-remote-workflow.ps1` / `verify-remote-workflow.sh`: post-push raw GitHub workflow validation without requiring `gh`.
- `verify-lock-hashes.ps1` / `verify-lock-hashes.sh`: `.gitattributes`, LF canonical JSON, SHA lock, and metadata validation.
- `verify-public-docs-status.ps1` / `verify-public-docs-status.sh`: public README, STATUS, and ROADMAP status validation.

They do not require raw transcript files, CUDA, GitHub credentials, secrets, or generated result-store outputs.

The workflow validation scripts reject flattened one-line workflow formatting and check parsed YAML structure.

After a CI workflow push, run the remote verifier to confirm GitHub serves the same readable multi-line workflow from the raw `main` URL.
