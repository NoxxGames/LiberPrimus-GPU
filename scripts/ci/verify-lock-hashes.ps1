Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

$Attributes = Get-Content ".gitattributes"
if ($Attributes.Count -le 10) {
    throw ".gitattributes must have more than 10 physical lines."
}
if ($Attributes | Where-Object { $_ -like "* text=auto .gitattributes*" }) {
    throw ".gitattributes appears to be flattened onto one line."
}
foreach ($Required in @("*.json text eol=lf", "*.sha256 text eol=lf", "*.yml text eol=lf", "*.sh text eol=lf")) {
    if ($Required -notin $Attributes) {
        throw ".gitattributes is missing required rule: $Required"
    }
}

Write-Host "Validating canonical JSON locks"
& $Python scripts\ci\repair-canonical-json-locks.py --check
Write-Host "Lock hash validation OK"
