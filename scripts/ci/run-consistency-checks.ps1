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

    Write-Host "Validating Stage 3K archive and observation registries"
    & $Python -m libreprimus.cli archive validate-sources --records data/observations/archive/source-archive-records-v0.yaml
    & $Python -m libreprimus.cli archive validate-image-locks --locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl --artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl --allow-empty
    & $Python -m libreprimus.cli observation validate-visual --records data/observations/visual/visual-numeric-observations-v0.yaml
    & $Python -m libreprimus.cli observation validate-cookies --records data/observations/web/cookie-hash-records-v0.yaml

    Write-Host "Validating Stage 3L hash preimage candidate packs"
    & $Python -m libreprimus.cli hash-preimage validate-packs --pack-dir data/observations/web/hash-preimage-candidate-packs

    Write-Host "Validating Stage 3M deterministic image-analysis raw-data-free mode"
    & $Python -m libreprimus.cli image-analysis validate-results --results-dir (Join-Path $TempDir "stage3m-image-analysis") --allow-missing

    Write-Host "Validating Stage 3P deterministic image-transform raw-data-free mode"
    & $Python -m libreprimus.cli image-transform validate-results --results-dir (Join-Path $TempDir "stage3p-image-transforms") --allow-missing

    Write-Host "Validating Stage 3N Discord ingestion raw-log-free mode"
    & $Python -m libreprimus.cli discord-ingest scan --source-dir (Join-Path $TempDir "missing-discord") --out-dir (Join-Path $TempDir "stage3n-discord") --allow-missing --allow-warnings
    & $Python -m libreprimus.cli discord-ingest validate-results --results-dir (Join-Path $TempDir "stage3n-discord") --allow-missing

    Write-Host "Validating Stage 3O Discord promotion and Wiki mirror"
    & $Python -m libreprimus.cli discord-promote validate-promoted --links data/observations/discord/promoted-public-source-links-stage3o.yaml --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml --allow-empty
    & .\scripts\github\validate-wiki-source.ps1

    Write-Host "Validating Stage 3Q Discord review-bundle raw-log-free mode"
    $Stage3QOut = Join-Path $TempDir "stage3q-discord-review"
    $Stage3QAggregate = Join-Path $TempDir "stage3q-discord-review-aggregate.yaml"
    & $Python -m libreprimus.cli discord-review build-bundles --ingestion-dir (Join-Path $TempDir "missing-stage3n") --promotion-dir (Join-Path $TempDir "missing-stage3o") --raw-dir (Join-Path $TempDir "missing-discord") --out-dir $Stage3QOut --aggregate-out $Stage3QAggregate --allow-missing --allow-warnings
    & $Python -m libreprimus.cli discord-review validate-bundles --results-dir $Stage3QOut --aggregate $Stage3QAggregate --allow-missing

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

    Write-Host "Validating Stage 2G proposals and approval gates"
    & $Python -m libreprimus.cli proposal validate --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml
    & $Python -m libreprimus.cli proposal check-approval --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --approval experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml

    Write-Host "Generating Stage 2G review packet to temp"
    & $Python -m libreprimus.cli proposal review-packet --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --out-dir (Join-Path $TempDir "stage2g-review") --allow-warnings

    Write-Host "Validating Stage 2H approval-gated requests"
    & $Python -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml
    & $Python -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-noop-real-request.yaml

    Write-Host "Running Stage 2H approved synthetic request to temp"
    & $Python -m libreprimus.cli approval-execution run --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml --out-dir (Join-Path $TempDir "stage2h-approval-execution") --allow-warnings

    Write-Host "Validating Stage 2I approval-readiness proposal"
    & $Python -m libreprimus.cli approval-readiness validate --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml

    Write-Host "Generating Stage 2I readiness packet to temp"
    & $Python -m libreprimus.cli approval-readiness packet --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml --out-dir (Join-Path $TempDir "stage2i-readiness") --allow-warnings

    Write-Host "Validating Stage 2J bounded operator policy and queue"
    & $Python -m libreprimus.cli bounded-experiment validate-policy --policy experiments/policies/operator-policy-v0.yaml
    & $Python -m libreprimus.cli bounded-experiment validate-queue --queue experiments/queues/stage2j-bounded-cpu-queue.yaml
    & $Python -m libreprimus.cli bounded-experiment check-queue --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml

    Write-Host "Running Stage 2J bounded queue to temp"
    & $Python -m libreprimus.cli bounded-experiment run-all --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml --out-dir (Join-Path $TempDir "stage2j-bounded") --allow-warnings
} finally {
    if (Test-Path $TempDir) {
        Remove-Item -LiteralPath $TempDir -Recurse -Force
    }
}
