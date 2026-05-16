Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

Write-Host "Validating profile summaries"
& $Python -m libreprimus.cli profile summary

Write-Host "Validating transform registry"
& $Python -m libreprimus.cli transform-registry validate --registry data/transform-registry/cpu-reference-transforms-v0.json

$SolvedManifests = @(
    "experiments/manifests/solved-baselines/direct-translation-v0.yaml",
    "experiments/manifests/solved-baselines/atbash-family-v0.yaml",
    "experiments/manifests/solved-baselines/vigenere-v0.yaml",
    "experiments/manifests/solved-baselines/prime-stream-v0.yaml",
    "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml"
)

foreach ($Manifest in $SolvedManifests) {
    Write-Host "Validating solved-baseline manifest $Manifest"
    & $Python -m libreprimus.cli solved-baseline validate-manifest --manifest $Manifest
}

Write-Host "Validating result-store manifest"
& $Python -m libreprimus.cli result-store validate-manifest --manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml
