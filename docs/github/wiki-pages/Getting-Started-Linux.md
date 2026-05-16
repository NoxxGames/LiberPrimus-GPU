# Getting Started On Linux

Use a Python virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q tests/python
```

Current parser/alignment tools run on CPU hardware.
