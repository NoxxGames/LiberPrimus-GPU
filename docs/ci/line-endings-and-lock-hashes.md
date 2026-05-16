# Line Endings And Lock Hashes

## Purpose

Stage 2C-followup-3 fixes Linux CI SHA-256 lock failures caused by platform-dependent line endings in committed profile and registry JSON files.

## Gitattributes Policy

`.gitattributes` must remain a readable multi-line attributes file. A flattened file such as `* text=auto .gitattributes text eol=lf ...` prevents Git from applying the intended per-pattern line-ending rules.

The repository pins JSON, YAML, shell scripts, Markdown, source files, and `.sha256` files to LF. PowerShell and batch scripts remain CRLF because those are Windows-oriented entry points.

## Canonical JSON Bytes

Committed profile and registry JSON locks use deterministic UTF-8 JSON with:

- LF line endings.
- A final newline.
- Stable object-key ordering.
- Preserved list ordering.

The `.sha256` file hashes the exact checked-out JSON bytes under Git attributes. Metadata JSON records the same SHA-256.

## Failure Mode

On Windows, CRLF working-tree bytes can produce a different SHA-256 than Linux LF checkouts. If a lock was generated from CRLF bytes, local Windows tests may pass while GitHub Actions fails on Linux.

## Validation

Run:

```powershell
.\.venv\Scripts\python.exe scripts\ci\repair-canonical-json-locks.py --check
.\scripts\ci\verify-lock-hashes.ps1
```

On Linux:

```bash
python scripts/ci/repair-canonical-json-locks.py --check
bash scripts/ci/verify-lock-hashes.sh
```

The verification checks `.gitattributes`, canonical JSON line endings, raw SHA-256 locks, and metadata SHA fields.

For remote verification after a push, run the remote Git blob verifier:

```powershell
.\scripts\ci\verify-remote-git-blobs.ps1 -Remote origin -Branch main -CheckRawUrl -CheckGitHubApi
```

This checks the fetched `origin/main` `.gitattributes` blob before considering raw URL diagnostics.

## Repair

To repair canonical profile/registry locks:

```powershell
.\.venv\Scripts\python.exe scripts\ci\repair-canonical-json-locks.py
```

After repair, rerun the full local CI scripts and stage only the explicit changed files. Do not update `.sha256` files by hand without validation.
