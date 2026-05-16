Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

Write-Host "Running Ruff"
& $Python -m ruff check python/libreprimus tests/python

Write-Host "Running pytest"
& $Python -m pytest -q tests/python

Write-Host "Running Python smoke"
& $Python -m libreprimus.cli smoke
