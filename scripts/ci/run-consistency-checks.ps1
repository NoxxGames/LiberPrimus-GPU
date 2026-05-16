Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("libreprimus-consistency-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $TempDir | Out-Null

try {
    Write-Host "Running full consistency suite"
    & $Python -m libreprimus.cli consistency check-all --allow-warnings

    Write-Host "Running result-store consistency suite"
    & $Python -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings

    Write-Host "Exporting consistency summary to temp"
    & $Python -m libreprimus.cli consistency check-all --out (Join-Path $TempDir "consistency_summary.json") --allow-warnings
} finally {
    if (Test-Path $TempDir) {
        Remove-Item -LiteralPath $TempDir -Recurse -Force
    }
}
