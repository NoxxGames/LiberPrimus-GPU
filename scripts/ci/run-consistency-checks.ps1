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

    Write-Host "Running state-drift consistency checks"
    & $Python -m libreprimus.cli consistency check-state-drift

    Write-Host "Validating Stage 3Y research synthesis records"
    & $Python -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md

    Write-Host "Validating Stage 4B source-lock triage records"
    & $Python -m libreprimus.cli source-lock-triage validate `
        --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml `
        --source-health data/locks/third-party/stage4b-source-health-records.yaml `
        --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
        --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
        --cookie-source-records data/observations/web/stage4b-cookie-candidate-source-records.yaml `
        --manifest-dir experiments/manifests/stage4b-disabled

    Write-Host "Validating Stage 4C visual annotation records"
    & $Python -m libreprimus.cli visual-annotation validate `
        --task data/observations/visual/stage4c-visual-annotation-tasks.yaml `
        --cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
        --dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
        --delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
        --negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
        --summary data/observations/visual/stage4c-annotation-pack-summary.yaml

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

    Write-Host "Validating Stage 4A Discord full-review synthetic build"
    $Stage4ADiscord = Join-Path $TempDir "stage4a-discord"
    $Stage4APages = Join-Path $TempDir "stage4a-pages"
    $Stage4AOut = Join-Path $TempDir "stage4a-full-review"
    New-Item -ItemType Directory -Path $Stage4ADiscord, $Stage4APages | Out-Null
    @"
from pathlib import Path
from PIL import Image
discord = Path(r"$Stage4ADiscord")
pages = Path(r"$Stage4APages")
(discord / "CicadaSolvers - Cicada - ci-test [123456789012345678].html").write_text(
    '<div class="chatlog__message"><span class="chatlog__author-name">User</span>'
    '<div class="chatlog__content">cuneiform base60 onion 7 https://example.org/source '
    'https://cdn.discordapp.com/attachments/1/2/test.png?secret=1</div></div>',
    encoding="utf-8",
)
Image.new("RGB", (32, 32), "white").save(pages / "page001.jpg")
"@ | & $Python -
    & $Python -m libreprimus.cli discord-full-review build --discord-dir $Stage4ADiscord --lp-pages-dir $Stage4APages --out-dir $Stage4AOut --privacy-mode redacted_public --include-lp-page-gallery --allow-warnings
    & $Python -m libreprimus.cli discord-full-review validate --results-dir $Stage4AOut

    Write-Host "Validating Stage 3R Discord lead promotion records and disabled manifests"
    & $Python -m libreprimus.cli discord-leads validate --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml --negative-controls data/observations/discord/stage3r-negative-control-records.yaml --manifest-dir experiments/manifests/post-discord --allow-empty

    Write-Host "Validating Stage 3S post-Discord Onion 7 manifest"
    & $Python -m libreprimus.cli post-discord validate-manifest --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml

    Write-Host "Validating Stage 3T GP/rune claim verifier manifest"
    & $Python -m libreprimus.cli post-discord validate-gp-rune-manifest --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml

    Write-Host "Validating Stage 3U cookie signed-variant manifest"
    & $Python -m libreprimus.cli post-discord validate-cookie-manifest --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml

    Write-Host "Validating Stage 3V OutGuess regression manifest and missing-tool-safe detection"
    & $Python -m libreprimus.cli stego outguess-validate-manifest --manifest experiments/manifests/stego/outguess-regression-v1.yaml --artifacts data/observations/stego/outguess-artifacts-v0.yaml
    & $Python -m libreprimus.cli stego outguess-detect --out-dir (Join-Path $TempDir "stage3v-outguess") --allow-missing-tool

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
