> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Windows Setup

## PowerShell

Open PowerShell in `<repo-root>`. Use repository scripts from that directory.

```powershell
.\scripts\verify-toolchain.ps1
```

## Python Virtual Environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## CMake And Native Tools

Stage 0A includes CMake/Ninja/Visual Studio Build Tools guidance in `README.md` and `scripts/`. Native builds are smoke checks; current Stage 0D-P work is Python/docs only.

## GitHub CLI

GitHub CLI is optional for users and useful for maintainers:

```powershell
gh auth status
```

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python
```

## Run CLI Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli legacy-pastebin summary
```

## CUDA Status

CUDA is optional and unused by Stage 0D-P. Future GPU acceleration is for batch transform/scoring after CPU references and parity tests exist.
