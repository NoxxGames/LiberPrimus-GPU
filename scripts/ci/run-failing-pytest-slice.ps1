param(
    [Parameter(Mandatory = $true)]
    [string]$ResultsDir
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Summary = Get-ChildItem -LiteralPath $ResultsDir -Recurse -File |
    Where-Object { $_.Name -like "*run-summary*.yaml" -or $_.Name -like "*run-summary*.yml" -or $_.Name -like "*run-summary*.json" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
if ($null -eq $Summary) {
    throw "No parallel-validation run summary found under $ResultsDir"
}
Write-Host "Inspect run summary for failure_rerun_commands: $($Summary.FullName)"
if ($Summary.Extension -eq ".json") {
    $Record = Get-Content -Raw -LiteralPath $Summary.FullName | ConvertFrom-Json
    if ($Record.pytest_result.failure_rerun_commands) {
        foreach ($Command in $Record.pytest_result.failure_rerun_commands) {
            Write-Host $Command
        }
    }
    if ($Record.pytest_result.shard_results) {
        foreach ($Shard in $Record.pytest_result.shard_results) {
            if (-not $Shard.passed -and $Shard.rerun_command) {
                Write-Host $Shard.rerun_command
            }
        }
    }
} else {
    Select-String -LiteralPath $Summary.FullName -Pattern "rerun_command|failure_rerun_commands|rerun_guidance" -Context 0,3
}
