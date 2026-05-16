[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,
    [string]$WikiSourceDir = "docs/github/wiki-pages",
    [string]$WikiWorktreeDir = ".wiki-worktree",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Find-Gh {
    $cmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }
    foreach ($candidate in @("C:\Program Files\GitHub CLI\gh.exe", "C:\Program Files (x86)\GitHub CLI\gh.exe", "$env:LOCALAPPDATA\GitHub CLI\gh.exe")) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    throw "GitHub CLI 'gh' was not found."
}

$gh = Find-Gh
& $gh auth status | Out-Host
$repoInfo = (& $gh repo view $Repo --json nameWithOwner,url,hasWikiEnabled | ConvertFrom-Json)
if ($LASTEXITCODE -ne 0) { throw "Repository verification failed: $Repo" }

$source = Resolve-Path -LiteralPath $WikiSourceDir
$pageCount = (Get-ChildItem -LiteralPath $source -Filter "*.md").Count

if ($DryRun) {
    Write-Host "dry_run=true"
    Write-Host "repo=$($repoInfo.nameWithOwner)"
    Write-Host "wiki_source=$source"
    Write-Host "wiki_pages=$pageCount"
    Write-Host "would_enable_wiki=true"
    Write-Host "would_worktree=$WikiWorktreeDir"
    return
}

& $gh repo edit $Repo --enable-wiki
if ($LASTEXITCODE -ne 0) { throw "Could not enable or verify wiki for $Repo" }

$wikiUrl = "https://github.com/$Repo.wiki.git"
if (-not (Test-Path -LiteralPath $WikiWorktreeDir)) {
    git clone $wikiUrl $WikiWorktreeDir
    if ($LASTEXITCODE -ne 0) {
        New-Item -ItemType Directory -Force -Path $WikiWorktreeDir | Out-Null
        Push-Location $WikiWorktreeDir
        try {
            git init
            git remote add origin $wikiUrl
            git checkout -B master
        } finally {
            Pop-Location
        }
    }
}

Get-ChildItem -LiteralPath $source -File -Filter "*.md" | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $WikiWorktreeDir -Force
}

Push-Location $WikiWorktreeDir
try {
    git add -- *.md
    $status = git status --short
    if ($status) {
        git commit -m "Publish Liber Primus GPU wiki pages"
        if ($LASTEXITCODE -ne 0) { throw "Wiki commit failed." }
        $commit = (git rev-parse HEAD).Trim()
        git push -u origin HEAD
        if ($LASTEXITCODE -ne 0) { throw "Wiki push failed." }
        Write-Host "wiki_commit=$commit"
        Write-Host "wiki_pushed=true"
    } else {
        $commit = $null
        try {
            $commit = (git rev-parse HEAD 2>$null)
        } catch {
            $commit = $null
        }
        Write-Host "wiki_no_changes=true"
        if ($commit) { Write-Host "wiki_commit=$($commit.Trim())" }
        Write-Host "wiki_pushed=false"
    }
} finally {
    Pop-Location
}

Write-Host "wiki_pages=$pageCount"
Write-Host "wiki_url=https://github.com/$Repo/wiki"
