[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Repo
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Find-Gh {
    $cmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }
    foreach ($candidate in @("C:\Program Files\GitHub CLI\gh.exe", "C:\Program Files (x86)\GitHub CLI\gh.exe", "$env:LOCALAPPDATA\GitHub CLI\gh.exe")) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    throw "GitHub CLI 'gh' was not found."
}

$gh = Find-Gh
$labelsPath = Join-Path (Get-Location) "docs/github/labels.json"
$labels = Get-Content -LiteralPath $labelsPath -Raw | ConvertFrom-Json
$count = 0

foreach ($label in $labels) {
    $color = ([string]$label.color).TrimStart("#")
    & $gh label create $label.name --repo $Repo --description $label.description --color $color --force | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create or update label: $($label.name)"
    }
    $count += 1
}

Write-Host "labels_created_or_updated=$count"
