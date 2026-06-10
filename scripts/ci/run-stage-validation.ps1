param(
    [string]$Stage = "stage5dy",
    [ValidateSet("focused", "stage-fast", "local-fast", "full-parallel", "full-serial-rare", "ci")]
    [string]$Profile = "stage-fast",
    [int]$Workers = 8,
    [int]$PytestWorkers = 8,
    [int]$CommandTimeoutSeconds = 900
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$PowerShellExe = if ($PSVersionTable.PSEdition -eq "Core") { "pwsh" } else { "powershell.exe" }
$Stage5DYResultsDir = Join-Path (Join-Path (Join-Path (Join-Path "experiments" "results") "ci") "parallel-validation") "stage5dy"

function Invoke-StageStep {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$Arguments,
        [int]$TimeoutSeconds = $CommandTimeoutSeconds
    )
    Write-Host "[$Profile] $Name"
    $processInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $processInfo.FileName = $FilePath
    $processInfo.UseShellExecute = $false
    $processInfo.Arguments = ($Arguments | ForEach-Object {
        if ($_ -match '\s') {
            '"' + ($_ -replace '"', '\"') + '"'
        } else {
            $_
        }
    }) -join " "
    $process = [System.Diagnostics.Process]::Start($processInfo)
    if ($null -eq $process) {
        throw "$Name failed to start"
    }
    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        throw "$Name timed out after $TimeoutSeconds seconds"
    }
    $process.Refresh()
    $exitCode = $process.ExitCode
    if ($null -eq $exitCode) {
        throw "$Name exited but no exit code was reported"
    }
    if ($exitCode -ne 0) {
        throw "$Name failed with exit code $exitCode"
    }
}

if ($Workers -gt 8 -or $PytestWorkers -gt 8) {
    throw "Stage 5DY validation policy caps local workers at 8"
}

if ($Stage -ne "stage5dy" -and $Stage -ne "stage-5dy") {
    throw "run-stage-validation currently supports Stage 5DY only"
}

$stageTestFiles = Get-ChildItem tests/python -Filter "test_stage5dy_*.py" | ForEach-Object { $_.FullName }

switch ($Profile) {
    "focused" {
        Invoke-StageStep "validate Stage 5DY" $Python @("-m", "libreprimus.cli", "token-block", "validate-stage5dy")
        if ($stageTestFiles.Count -gt 0) {
            $pytestArgs = @("-m", "pytest", "-q") + $stageTestFiles
            Invoke-StageStep "pytest Stage 5DY focused files" $Python $pytestArgs
        }
    }
    "stage-fast" {
        Invoke-StageStep "validate Stage 5DY" $Python @("-m", "libreprimus.cli", "token-block", "validate-stage5dy")
        Invoke-StageStep "Stage 5DY summary" $Python @("-m", "libreprimus.cli", "token-block", "stage5dy-summary")
        Invoke-StageStep "Source Browser index smoke" $Python @("-m", "libreprimus.cli", "source-browser", "validate-index")
        if ($stageTestFiles.Count -gt 0) {
            $pytestArgs = @("-m", "pytest", "-q") + $stageTestFiles
            Invoke-StageStep "pytest Stage 5DY focused files" $Python $pytestArgs
        }
        $ruffArgs = @("-m", "ruff", "check", "python/libreprimus/token_block/stage5dy.py") + $stageTestFiles
        Invoke-StageStep "ruff Stage 5DY files" $Python $ruffArgs
    }
    "local-fast" {
        & $PSCommandPath -Stage $Stage -Profile stage-fast -Workers $Workers -PytestWorkers $PytestWorkers
        Invoke-StageStep "state drift" $Python @("-m", "libreprimus.cli", "consistency", "check-state-drift")
        Invoke-StageStep "fast consistency profile" $PowerShellExe @(
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            ".\scripts\ci\run-consistency-checks.ps1",
            "-Profile",
            "stage-fast"
        )
    }
    "full-parallel" {
        Invoke-StageStep "full parallel validation" $PowerShellExe @(
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            ".\scripts\ci\run-parallel-validation.ps1",
            "-Workers", "$Workers",
            "-PytestWorkers", "$PytestWorkers",
            "-PytestMode", "auto",
            "-ResultsDir", $Stage5DYResultsDir
        ) 7200
    }
    "full-serial-rare" {
        Write-Host "Full serial pytest is a rare fallback. Running only because the profile was explicitly requested."
        Invoke-StageStep "full serial pytest rare fallback" $Python @("-m", "pytest", "-q", "tests/python") 7200
    }
    "ci" {
        & $PSCommandPath -Stage $Stage -Profile local-fast -Workers $Workers -PytestWorkers $PytestWorkers
        & $PSCommandPath -Stage $Stage -Profile full-parallel -Workers $Workers -PytestWorkers $PytestWorkers
    }
}
