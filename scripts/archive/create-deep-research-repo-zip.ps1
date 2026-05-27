param(
    [string]$Stage = "stage5bd",
    [string]$OutDir = "deep-research-repo-zips/stage5bd",
    [switch]$IncludeGit
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path ".").Path
$outPath = Join-Path $repoRoot $OutDir
New-Item -ItemType Directory -Force -Path $outPath | Out-Null

$commit = "unavailable"
$branch = "unavailable"
try { $commit = (& git rev-parse HEAD).Trim() } catch {}
try { $branch = (& git branch --show-current).Trim() } catch {}

$archiveCommit = Join-Path $outPath "ARCHIVE_COMMIT.txt"
$archiveManifest = Join-Path $outPath "ARCHIVE_MANIFEST.json"
$archiveHash = Join-Path $outPath "ARCHIVE_MANIFEST.sha256"
$archiveReadme = Join-Path $outPath "ARCHIVE_README.md"
$zipPath = Join-Path $outPath "LiberPrimus-GPU-$Stage-review.zip"

@"
commit=$commit
branch=$branch
stage=$Stage
expected_next_stage=Stage 5BE - Deep Research review of token-block preflight dry-run implementation, archive/evidence hygiene, and execution-gate enforcement
"@ | Set-Content -LiteralPath $archiveCommit -Encoding UTF8

$files = git ls-files | Where-Object {
    ($_ -notlike "codex-output/*") -and
    ($_ -notlike "human-review-packs/*") -and
    ($_ -notlike "third_party/*") -and
    ($_ -notlike "experiments/results/*")
}
$manifestObject = [ordered]@{
    repo_name = "NoxxGames/LiberPrimus-GPU"
    stage = $Stage
    commit = $commit
    branch = $branch
    generated_utc = (Get-Date).ToUniversalTime().ToString("o")
    git_directory_included = [bool]$IncludeGit
    file_count = $files.Count
    excluded_roots = @(".git", "codex-output", "human-review-packs", "third_party", "experiments/results")
    instruction = "Use attached repository ZIP as primary evidence."
}
$manifestJson = $manifestObject | ConvertTo-Json -Depth 5
$manifestJson | Set-Content -LiteralPath $archiveManifest -Encoding UTF8

$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $archiveManifest).Hash.ToLowerInvariant()
$sha | Set-Content -LiteralPath $archiveHash -Encoding ASCII
"# Deep Research Repository ZIP`n`nUse attached repository ZIP as primary evidence.`n" |
    Set-Content -LiteralPath $archiveReadme -Encoding UTF8

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}
$items = @($files | ForEach-Object { Join-Path $repoRoot $_ }) + @($archiveCommit, $archiveManifest, $archiveHash, $archiveReadme)
Compress-Archive -Path $items -DestinationPath $zipPath -Force

Write-Host "archive_zip=$zipPath"
Write-Host "archive_commit=$archiveCommit"
Write-Host "Use attached repository ZIP as primary evidence."
