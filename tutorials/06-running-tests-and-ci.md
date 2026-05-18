# Running Tests And CI

## Purpose

Reproduce the local validation stack before pushing.

## Commands

```powershell
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli smoke
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
.\scripts\ci\run-consistency-checks.ps1
.\scripts\ci\verify-public-docs-status.ps1
.\scripts\ci\verify-lock-hashes.ps1
.\scripts\ci\validate-workflow-static.ps1
```

## Expected Outputs

Ruff and pytest should pass. Consistency and anti-drift checks should report zero failures.

## What Not To Commit

Do not commit temporary test output, generated summaries, or local result-store files.

## Troubleshooting

If a CI helper writes generated outputs under `experiments/results/`, verify those paths are ignored.
If anti-drift fails, update the operational docs together instead of weakening the check.
