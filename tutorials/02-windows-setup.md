# Windows Setup

## Purpose

Set up the Python and local validation environment on Windows.

## Prerequisites

- Python 3.12
- Git
- PowerShell
- Optional Visual Studio Build Tools, CMake, and Ninja

## Commands

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe -m libreprimus.cli smoke
```

## Expected Outputs

The smoke command should print `LiberPrimus Python Stage 0A smoke OK`.

## What Not To Commit

Do not commit `.venv/`, build directories, generated results, raw Discord logs, or raw page images.

## Troubleshooting

If PowerShell cannot find Python, run `py -0p` to list installed interpreters. If editable install
fails, upgrade pip inside the virtual environment first.
