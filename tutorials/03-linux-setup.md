# Linux Setup

## Purpose

Set up the Python and local validation environment on Linux.

## Prerequisites

- Python 3.12
- Git
- Bash
- Optional CMake and Ninja

## Commands

```bash
python3.12 -m venv .venv
./.venv/bin/python -m pip install -e '.[dev]'
./.venv/bin/python -m libreprimus.cli smoke
```

## Expected Outputs

The smoke command should print `LiberPrimus Python Stage 0A smoke OK`.

## What Not To Commit

Do not commit `.venv/`, build directories, generated results, raw Discord logs, or raw page images.

## Troubleshooting

If Python 3.12 is unavailable, install it through your distribution package manager or use a local
toolchain manager. Keep CI reproduction raw-data-free.
