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

    Write-Host "Validating Stage 2E exploratory manifests"
    & $Python -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml
    & $Python -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-affine-preview-dry-run.yaml

    Write-Host "Dry-running Stage 2E Caesar preview to temp"
    & $Python -m libreprimus.cli experiment dry-run --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml --out-dir (Join-Path $TempDir "stage2e-dry-run") --allow-warnings

    Write-Host "Validating Stage 2F CPU execution manifests"
    & $Python -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml
    & $Python -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-solved-baseline-replay.yaml

    Write-Host "Running Stage 2F synthetic direct execution"
    & $Python -m libreprimus.cli execution run --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml --out-dir experiments/results/cpu-execution/stage2f --allow-warnings
} finally {
    if (Test-Path $TempDir) {
        Remove-Item -LiteralPath $TempDir -Recurse -Force
    }
}
