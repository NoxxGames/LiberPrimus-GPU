param(
    [int]$Workers = 16,
    [int]$PytestWorkers = 16,
    [string]$PytestMode = "auto"
)

& "$PSScriptRoot\run-parallel-validation.ps1" -Workers $Workers -PytestWorkers $PytestWorkers -PytestMode $PytestMode
