param(
    [string]$Stage = "stage5ea",
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
$ParallelResultsRoot = Join-Path (Join-Path (Join-Path "experiments" "results") "ci") "parallel-validation"

function ConvertTo-StageCommandId {
    param([string]$Value)
    $token = ($Value.ToLowerInvariant() -replace "[^a-z0-9]", "")
    if ([string]::IsNullOrWhiteSpace($token)) {
        throw "Stage identifier is empty"
    }
    if (-not $token.StartsWith("stage")) {
        $token = "stage$token"
    }
    return $token
}

function Stop-StageProcessTree {
    param([int]$ProcessId)
    try {
        $children = Get-CimInstance Win32_Process -Filter "ParentProcessId = $ProcessId" -ErrorAction SilentlyContinue
        foreach ($child in $children) {
            Stop-StageProcessTree -ProcessId ([int]$child.ProcessId)
        }
    } catch {
        # Best-effort cleanup; the direct process kill below is authoritative.
    }
    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
}

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
        Stop-StageProcessTree -ProcessId $process.Id
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

$StageId = ConvertTo-StageCommandId $Stage
if ($Workers -gt 8 -or $PytestWorkers -gt 8) {
    throw "Stage validation policy caps local workers at 8"
}
if ($StageId -notin @("stage5dy", "stage5dz", "stage5ea")) {
    throw "run-stage-validation currently supports Stage 5DY, Stage 5DZ, and Stage 5EA"
}
$StageDisplay = $StageId.ToUpperInvariant().Replace("STAGE", "Stage ")
$stageTestFiles = Get-ChildItem tests/python -Filter "test_${StageId}_*.py" | ForEach-Object { $_.FullName }
$stageModulePath = "python/libreprimus/token_block/$StageId.py"
$validateCommand = "validate-$StageId"
$summaryCommand = "$StageId-summary"
$stageResultsDir = Join-Path $ParallelResultsRoot $StageId

switch ($Profile) {
    "focused" {
        Invoke-StageStep "validate $StageDisplay" $Python @("-m", "libreprimus.cli", "token-block", $validateCommand)
        if ($stageTestFiles.Count -gt 0) {
            $pytestArgs = @("-m", "pytest", "-q") + $stageTestFiles
            Invoke-StageStep "pytest $StageDisplay focused files" $Python $pytestArgs
        }
    }
    "stage-fast" {
        Invoke-StageStep "validate $StageDisplay" $Python @("-m", "libreprimus.cli", "token-block", $validateCommand)
        Invoke-StageStep "$StageDisplay summary" $Python @("-m", "libreprimus.cli", "token-block", $summaryCommand)
        Invoke-StageStep "Source Browser index smoke" $Python @("-m", "libreprimus.cli", "source-browser", "validate-index")
        if ($stageTestFiles.Count -gt 0) {
            $pytestArgs = @("-m", "pytest", "-q") + $stageTestFiles
            Invoke-StageStep "pytest $StageDisplay focused files" $Python $pytestArgs
        }
        $ruffArgs = @("-m", "ruff", "check", $stageModulePath) + $stageTestFiles
        Invoke-StageStep "ruff $StageDisplay files" $Python $ruffArgs
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
            "-ResultsDir", $stageResultsDir
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
