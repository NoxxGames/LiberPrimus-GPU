param(
    [int]$Workers = $(if ($env:LIBERPRIMUS_VALIDATION_WORKERS) { [int]$env:LIBERPRIMUS_VALIDATION_WORKERS } else { 16 }),
    [int]$PytestWorkers = $(if ($env:LIBERPRIMUS_PYTEST_WORKERS) { [int]$env:LIBERPRIMUS_PYTEST_WORKERS } else { 16 }),
    [string]$PytestMode = $(if ($env:LIBERPRIMUS_PYTEST_MODE) { $env:LIBERPRIMUS_PYTEST_MODE } else { "auto" }),
    [string]$ResultsDir = $(if ($env:LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR) { $env:LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR } else { Join-Path "experiments" "results/ci/parallel-validation/stage5ax" }),
    [switch]$FailFast
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

Write-Host "Building Stage 5AX parallel validation plan"
& $Python -m libreprimus.cli parallel-validation build-stage5ax-plan `
    --out-plan data/ci/stage5ax-parallel-validation-plan.yaml `
    --out-command-registry data/ci/stage5ax-parallel-command-registry.yaml `
    --out-run-policy data/ci/stage5ax-parallel-run-policy.yaml `
    --out-safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml `
    --out-pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml

Write-Host "Running Stage 5AX parallel validation"
& $Python -m libreprimus.cli parallel-validation run-stage5ax-parallel-validation `
    --plan data/ci/stage5ax-parallel-validation-plan.yaml `
    --workers $Workers `
    --pytest-workers $PytestWorkers `
    --pytest-mode $PytestMode `
    --results-dir $ResultsDir `
    --out-run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml

Write-Host "Building Stage 5AX summary"
& $Python -m libreprimus.cli parallel-validation build-stage5ax-summary `
    --plan data/ci/stage5ax-parallel-validation-plan.yaml `
    --command-registry data/ci/stage5ax-parallel-command-registry.yaml `
    --run-policy data/ci/stage5ax-parallel-run-policy.yaml `
    --run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml `
    --safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml `
    --pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml `
    --out-guardrail data/ci/stage5ax-guardrail.yaml `
    --out-next-stage data/project-state/stage5ax-next-stage-decision.yaml `
    --out-summary data/project-state/stage5ax-summary.yaml

Write-Host "Validating Stage 5AX records"
& $Python -m libreprimus.cli parallel-validation validate-stage5ax `
    --plan data/ci/stage5ax-parallel-validation-plan.yaml `
    --command-registry data/ci/stage5ax-parallel-command-registry.yaml `
    --run-policy data/ci/stage5ax-parallel-run-policy.yaml `
    --run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml `
    --safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml `
    --pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml `
    --guardrail data/ci/stage5ax-guardrail.yaml `
    --next-stage-decision data/project-state/stage5ax-next-stage-decision.yaml `
    --summary data/project-state/stage5ax-summary.yaml `
    --results-dir $ResultsDir
