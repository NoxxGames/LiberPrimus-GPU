param(
    [int]$Workers = $(if ($env:LIBERPRIMUS_VALIDATION_WORKERS) { [int]$env:LIBERPRIMUS_VALIDATION_WORKERS } else { 8 }),
    [int]$PytestWorkers = $(if ($env:LIBERPRIMUS_PYTEST_WORKERS) { [int]$env:LIBERPRIMUS_PYTEST_WORKERS } else { 8 }),
    [string]$PytestMode = $(if ($env:LIBERPRIMUS_PYTEST_MODE) { $env:LIBERPRIMUS_PYTEST_MODE } else { "auto" }),
    [string]$ResultsDir = $(if ($env:LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR) { $env:LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR } else { Join-Path "experiments" "results/ci/parallel-validation/stage5ax" }),
    [switch]$FailFast
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$RunStateDir = Join-Path $ResultsDir "_stage5ax_state"
New-Item -ItemType Directory -Path $RunStateDir -Force | Out-Null

if ($Workers -gt 8 -or $PytestWorkers -gt 8) {
    throw "Stage 5DY validation policy caps local parallel validation at 8 workers"
}

$RunExitCode = 0

Write-Host "Building Stage 5AX parallel validation plan"
& $Python -m libreprimus.cli parallel-validation build-stage5ax-plan `
    --out-plan (Join-Path $RunStateDir "stage5ax-parallel-validation-plan.yaml") `
    --out-command-registry (Join-Path $RunStateDir "stage5ax-parallel-command-registry.yaml") `
    --out-run-policy (Join-Path $RunStateDir "stage5ax-parallel-run-policy.yaml") `
    --out-safety-audit (Join-Path $RunStateDir "stage5ax-parallel-validation-safety-audit.yaml") `
    --out-pytest-shard-plan (Join-Path $RunStateDir "stage5ax-pytest-shard-plan.yaml")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Running Stage 5AX parallel validation"
& $Python -m libreprimus.cli parallel-validation run-stage5ax-parallel-validation `
    --plan (Join-Path $RunStateDir "stage5ax-parallel-validation-plan.yaml") `
    --workers $Workers `
    --pytest-workers $PytestWorkers `
    --pytest-mode $PytestMode `
    --results-dir $ResultsDir `
    --out-run-summary (Join-Path $RunStateDir "stage5ax-parallel-validation-run-summary.yaml") `
    --out-safety-audit (Join-Path $RunStateDir "stage5ax-parallel-validation-safety-audit.yaml")
$RunExitCode = $LASTEXITCODE

Write-Host "Building Stage 5AX summary"
& $Python -m libreprimus.cli parallel-validation build-stage5ax-summary `
    --plan (Join-Path $RunStateDir "stage5ax-parallel-validation-plan.yaml") `
    --command-registry (Join-Path $RunStateDir "stage5ax-parallel-command-registry.yaml") `
    --run-policy (Join-Path $RunStateDir "stage5ax-parallel-run-policy.yaml") `
    --run-summary (Join-Path $RunStateDir "stage5ax-parallel-validation-run-summary.yaml") `
    --safety-audit (Join-Path $RunStateDir "stage5ax-parallel-validation-safety-audit.yaml") `
    --pytest-shard-plan (Join-Path $RunStateDir "stage5ax-pytest-shard-plan.yaml") `
    --out-guardrail (Join-Path $RunStateDir "stage5ax-guardrail.yaml") `
    --out-next-stage (Join-Path $RunStateDir "stage5ax-next-stage-decision.yaml") `
    --out-summary (Join-Path $RunStateDir "stage5ax-summary.yaml")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Validating Stage 5AX records"
& $Python -m libreprimus.cli parallel-validation validate-stage5ax `
    --plan (Join-Path $RunStateDir "stage5ax-parallel-validation-plan.yaml") `
    --command-registry (Join-Path $RunStateDir "stage5ax-parallel-command-registry.yaml") `
    --run-policy (Join-Path $RunStateDir "stage5ax-parallel-run-policy.yaml") `
    --run-summary (Join-Path $RunStateDir "stage5ax-parallel-validation-run-summary.yaml") `
    --safety-audit (Join-Path $RunStateDir "stage5ax-parallel-validation-safety-audit.yaml") `
    --pytest-shard-plan (Join-Path $RunStateDir "stage5ax-pytest-shard-plan.yaml") `
    --guardrail (Join-Path $RunStateDir "stage5ax-guardrail.yaml") `
    --next-stage-decision (Join-Path $RunStateDir "stage5ax-next-stage-decision.yaml") `
    --summary (Join-Path $RunStateDir "stage5ax-summary.yaml") `
    --results-dir $ResultsDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ($RunExitCode -ne 0) { exit $RunExitCode }
