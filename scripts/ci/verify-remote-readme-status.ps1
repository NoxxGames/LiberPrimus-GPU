param(
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [string]$RepoOwner = "NoxxGames",
    [string]$RepoName = "LiberPrimus-GPU",
    [switch]$CheckRawUrl,
    [switch]$CheckGitHubApi
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

function Join-Lines([string[]]$Lines) {
    return ($Lines -join "`n")
}

function Get-LineCount([string]$Text) {
    return (($Text -split "`n").Count)
}

function Test-TopLevelHeading([string]$Text, [string]$Heading) {
    return (($Text -split "`r?`n") -contains $Heading)
}

function Assert-ReadmeStatus([string]$Text, [string]$SourceName) {
    if (Test-TopLevelHeading $Text "## Non-goals") {
        throw "$SourceName README contains forbidden top-level heading: ## Non-goals"
    }
    if (Test-TopLevelHeading $Text "## Non-goals for Stage 0A") {
        throw "$SourceName README contains forbidden top-level heading: ## Non-goals for Stage 0A"
    }
    foreach ($Required in @(
        "## Current boundaries and deferred work",
        "### Permanent safety rules",
        "### Current boundaries",
        "### Deferred future work",
        "### Already implemented since Stage 0A",
        "These are not permanent project exclusions",
        "Canonical corpus: inactive.",
        "No Liber Primus page is claimed solved",
        "Search/scoring/CUDA campaigns: not started",
        "Stage 2E: CPU exploratory experiment manifest scaffold and dry-run planner complete.",
        "Stage 2F: bounded CPU execution harness for synthetic and solved-fixture-only runs complete.",
        "Stage 2H: approval-gated execution path for approved synthetic/solved controls complete.",
        "Stage 2I: first real bounded CPU exploratory experiment approval packet complete.",
        "Stage 2J human decision on the first bounded CPU exploratory experiment proposal"
    )) {
        if (-not $Text.Contains($Required)) {
            throw "$SourceName README is missing required text: $Required"
        }
    }
}

Write-Host "Fetching $Remote"
& git fetch $Remote | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "git fetch $Remote failed"
}

$BlobRef = "$Remote/$Branch`:README.md"
$BlobLines = & git show $BlobRef
if ($LASTEXITCODE -ne 0) {
    throw "git show $BlobRef failed"
}
$BlobText = Join-Lines $BlobLines
Assert-ReadmeStatus $BlobText "git_blob"
Write-Host "git_blob_readme_line_count=$(Get-LineCount $BlobText)"

if ($CheckGitHubApi) {
    $ApiUri = "https://api.github.com/repos/$RepoOwner/$RepoName/contents/README.md?ref=$Branch"
    try {
        $Api = Invoke-RestMethod -Uri $ApiUri
        $ApiText = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String(($Api.content -replace "\s", "")))
        Assert-ReadmeStatus $ApiText "github_api"
        Write-Host "github_api_readme_line_count=$(Get-LineCount $ApiText)"
    }
    catch {
        Write-Warning "GitHub API README check failed: $($_.Exception.Message)"
    }
}

if ($CheckRawUrl) {
    $RawUri = "https://raw.githubusercontent.com/$RepoOwner/$RepoName/$Branch/README.md"
    try {
        $RawText = (Invoke-WebRequest -Uri $RawUri -UseBasicParsing).Content
        try {
            Assert-ReadmeStatus $RawText "raw_url"
        }
        catch {
            Write-Warning "Raw README status differs from git blob/API: $($_.Exception.Message)"
        }
        Write-Host "raw_url_readme_line_count=$(Get-LineCount $RawText)"
    }
    catch {
        Write-Warning "Raw README fetch failed: $($_.Exception.Message)"
    }
}

Write-Host "Remote README status validation OK"
