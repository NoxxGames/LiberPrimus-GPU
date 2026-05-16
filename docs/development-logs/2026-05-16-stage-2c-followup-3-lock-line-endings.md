# Stage 2C-followup-3 Lock Line Endings

## Initial State

- Branch: `main`
- Local commit: `4fb19788ee5db5fe5d7d7835ec6ff77de7c30aa4`
- Remote main commit: `4fb19788ee5db5fe5d7d7835ec6ff77de7c30aa4`
- Local equals remote: `true`
- Git status before changes: clean
- `.gitattributes` local physical line count: `30`
- `.gitattributes` malformed one-line suspected locally: `false`
- Remote `.gitattributes` physical line count: `30`
- Local workflow line count: `68`
- Profile JSON CRLF detected: `true`
- Registry JSON CRLF detected: `true`
- Local Windows SHA matched locks before repair: `true` for all four locked JSON files
- GitHub Actions Python CI failure: Linux LF checkout SHA mismatched CRLF-generated locks
- `gh` available and authenticated: `true`
- Raw files staged: `0`
- Generated outputs staged: `0`
- `LiberPrimus-Research-Report.md` staged: `0`

## Gitattributes Repair

`.gitattributes` was rewritten as a documented multi-line attributes file with explicit LF rules for JSON, YAML, shell scripts, source files, and SHA locks.

## Lock Regeneration

Canonical profile and registry JSON files were normalized to deterministic UTF-8 JSON with LF line endings and final newlines. SHA-256 lock files and metadata JSON were regenerated from those exact bytes.

Hash changes:

- Gematria profile: `93577209028c964523068b5975180e05bda5b1a07b2675d4e35d03d6d164c5c2` -> `80cb10863b1fd3de57b44000c6bd90c307f11b90cc9d864a3d493e3f069c3280`
- Separator grammar: `303f3062ad8b41bf84ab068f2fd6601b1efb3291872d53956669ea3dd7d88e3c` -> `e0a5f682ced4afcf25956d06b1b49d1356203fe8ed47c7dec41365e3bec7b8e7`
- Glyph variants: `5acae61c4ea2aa9f2f2fb76bdcafb7ed9c6504bd98caf29590a95d7d43271d6d` -> `df81597b15c991ddf2894a44f1a6980554a5e463881d00a31524e5366dd704bf`
- Transform registry: `32e449b0a0f02cd1180767625474f0cfe2d988a26b13fd37741b7aa31023595e` -> `640f280094d8c6d87548fd768236c084cd03f096880a14c3790a3bc546eda6b9`

Dependent solved fixtures and solved-baseline manifests were updated to reference the new canonical profile/registry hashes.

## Validation

Pending final local validation, commit, push, and remote CI observation.

## Local Validation

- `repair-canonical-json-locks.py --check`: passed.
- `verify-lock-hashes.ps1`: passed.
- Ruff: passed.
- Pytest: `247 passed`.
- Python smoke: passed.
- Transform registry validation: passed.
- Solved-baseline manifest validation: passed.
- Result-store manifest validation: passed.
- `run-python-ci.ps1`: passed.
- `run-schema-manifest-checks.ps1`: passed.
- `validate-workflow-static.ps1`: passed.
- Bash syntax checks: skipped because local `bash` delegates to WSL and no WSL distributions are installed.
- CMake CPU smoke: configure/build/CTest passed with Visual Studio Debug config and `LPGPU_ENABLE_CUDA=OFF`.
- Raw files staged: `0`.
- Generated outputs staged: `0`.
- SQLite outputs staged: `0`.
- `LiberPrimus-Research-Report.md` staged: `0`.
