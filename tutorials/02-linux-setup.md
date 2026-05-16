# Linux Setup

## Python Virtual Environment

From `<repo-root>`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip setuptools wheel
.venv/bin/python -m pip install -e ".[dev]"
```

## CMake And Native Tools

Install CMake, Ninja, and a C++20 compiler through your platform package manager. Current transcript parsing and alignment tools do not require CUDA or a native build.

## Run Tests

```bash
.venv/bin/python -m pytest -q tests/python
```

## Run CLI Commands

```bash
.venv/bin/python -m libreprimus.cli legacy-pastebin summary
```

## CUDA Status

CUDA is optional and not used in Stage 0D-P. Linux users without NVIDIA hardware can still run the current Python tools.
