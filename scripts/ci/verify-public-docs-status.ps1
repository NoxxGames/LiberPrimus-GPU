Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

Write-Host "Validating public documentation status"
& $Python -m pytest -q tests/python/test_stage2c_public_docs_status.py tests/python/test_stage2d_readme_boundaries.py
