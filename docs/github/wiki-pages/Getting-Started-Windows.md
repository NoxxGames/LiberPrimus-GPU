# Getting Started On Windows

Use PowerShell in the repository root.

Install the Python package in a virtual environment and run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli legacy-pastebin summary
```

CUDA is optional and not used in Stage 0D-P.
