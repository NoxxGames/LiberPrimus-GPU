# CI Scripts

These scripts reproduce the raw-data-free GitHub Actions checks locally.

- `run-python-ci.ps1` / `run-python-ci.sh`: Ruff, pytest, and the Python smoke command.
- `run-schema-manifest-checks.ps1` / `run-schema-manifest-checks.sh`: raw-data-free profile, registry, solved-baseline manifest, and result-store manifest validation.
- `run-consistency-checks.ps1` / `run-consistency-checks.sh`: schema, manifest, docs, registry, ignored-output, result-store, and Stage 2E exploratory dry-run consistency checks.
- `validate-workflow-static.ps1` / `validate-workflow-static.sh`: static GitHub Actions workflow validation.
- `verify-remote-workflow.ps1` / `verify-remote-workflow.sh`: post-push raw GitHub workflow validation without requiring `gh`.
- `verify-remote-git-blobs.ps1` / `verify-remote-git-blobs.sh`: post-push Git blob validation for the workflow and `.gitattributes`; raw URL/API checks are diagnostic.
- `verify-lock-hashes.ps1` / `verify-lock-hashes.sh`: `.gitattributes`, LF canonical JSON, SHA lock, and metadata validation.
- `verify-public-docs-status.ps1` / `verify-public-docs-status.sh`: public README, STATUS, and ROADMAP status validation.
- `verify-remote-readme-status.ps1` / `verify-remote-readme-status.sh`: remote README boundary wording validation using the fetched Git blob as the authority.

They do not require raw transcript files, CUDA, GitHub credentials, secrets, or generated result-store outputs.

The workflow validation scripts reject flattened one-line workflow formatting and check parsed YAML structure.

After a CI workflow or `.gitattributes` push, run the remote Git blob verifier first. Use the raw workflow verifier as a public URL diagnostic, not as the only source of remote truth.
