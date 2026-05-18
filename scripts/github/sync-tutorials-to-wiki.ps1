Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$DryRun = $false
$Publish = $false
$Repo = "NoxxGames/LiberPrimus-GPU"
$WikiRemote = "https://github.com/NoxxGames/LiberPrimus-GPU.wiki.git"
$TutorialDir = "tutorials"
$WikiSourceDir = "docs/wiki-source"
$WikiWorktreeDir = ".wiki-worktree"
$ReportPath = "experiments/results/wiki-sync/stage3o/wiki-sync-report.json"

for ($i = 0; $i -lt $args.Count; $i++) {
    switch -Regex ($args[$i]) {
        "^--?DryRun$" { $DryRun = $true; continue }
        "^--?Publish$" { $Publish = $true; continue }
        "^--?Repo$" { $i++; $Repo = $args[$i]; continue }
        "^--?WikiRemote$" { $i++; $WikiRemote = $args[$i]; continue }
        "^--?TutorialDir$" { $i++; $TutorialDir = $args[$i]; continue }
        "^--?WikiSourceDir$" { $i++; $WikiSourceDir = $args[$i]; continue }
        "^--?WikiWorktreeDir$" { $i++; $WikiWorktreeDir = $args[$i]; continue }
        "^--?ReportPath$" { $i++; $ReportPath = $args[$i]; continue }
        default { throw "Unknown argument: $($args[$i])" }
    }
}

if (-not $DryRun -and -not $Publish) {
    $DryRun = $true
}

function Convert-ToWikiPageName {
    param([Parameter(Mandatory = $true)][string]$FileName)
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
    $parts = $stem -split "-"
    $titleParts = foreach ($part in $parts) {
        if ($part -match "^\d+$") {
            $part
        } elseif ($part.Length -gt 0) {
            $part.Substring(0, 1).ToUpperInvariant() + $part.Substring(1).ToLowerInvariant()
        }
    }
    return (($titleParts -join " ") + ".md")
}

function Write-Report {
    param([hashtable]$Report)
    $dir = Split-Path -Parent $ReportPath
    if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $Report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding utf8
}

function New-WikiSource {
    if (-not (Test-Path -LiteralPath $TutorialDir)) {
        throw "Tutorial directory not found: $TutorialDir"
    }
    New-Item -ItemType Directory -Force -Path $WikiSourceDir | Out-Null

    Get-ChildItem -LiteralPath $WikiSourceDir -Filter "*.md" -File -ErrorAction SilentlyContinue |
        Remove-Item -Force

    $tutorials = Get-ChildItem -LiteralPath $TutorialDir -Filter "*.md" -File | Sort-Object Name
    $pages = New-Object System.Collections.Generic.List[hashtable]

    foreach ($tutorial in $tutorials) {
        $pageName = Convert-ToWikiPageName -FileName $tutorial.Name
        $target = Join-Path $WikiSourceDir $pageName
        $sourceRel = "tutorials/$($tutorial.Name)"
        $body = (Get-Content -LiteralPath $tutorial.FullName -Raw).TrimEnd()
        $notice = @(
            "> This Wiki page mirrors `$sourceRel`. The repository tutorial file is the source of truth.",
            "",
            ""
        ) -join [Environment]::NewLine
        [System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath($target), $notice + $body + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
        $pages.Add(@{ source = $sourceRel; page = $pageName }) | Out-Null
    }

    $homeLines = New-Object System.Collections.Generic.List[string]
    $homeLines.Add("# Liber Primus GPU Wiki Mirror") | Out-Null
    $homeLines.Add("") | Out-Null
    $homeLines.Add("This Wiki mirrors the repository tutorials. The repository files under `tutorials/` are the source of truth.") | Out-Null
    $homeLines.Add("") | Out-Null
    foreach ($page in $pages) {
        $title = [System.IO.Path]::GetFileNameWithoutExtension([string]$page.page)
        $homeLines.Add("- [[$title]]") | Out-Null
    }
    [System.IO.File]::WriteAllText((Join-Path (Resolve-Path -LiteralPath $WikiSourceDir).Path "Home.md"), ($homeLines -join [Environment]::NewLine) + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))

    $sidebarLines = New-Object System.Collections.Generic.List[string]
    $sidebarLines.Add("# Tutorials") | Out-Null
    foreach ($page in $pages) {
        $title = [System.IO.Path]::GetFileNameWithoutExtension([string]$page.page)
        $sidebarLines.Add("- [[$title]]") | Out-Null
    }
    [System.IO.File]::WriteAllText((Join-Path (Resolve-Path -LiteralPath $WikiSourceDir).Path "_Sidebar.md"), ($sidebarLines -join [Environment]::NewLine) + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))

    return $pages
}

$pages = New-WikiSource
& "$PSScriptRoot\validate-wiki-source.ps1" -TutorialDir $TutorialDir -WikiSourceDir $WikiSourceDir | Out-Host

$report = @{
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    repo = $Repo
    wiki_remote = $WikiRemote
    dry_run = [bool]$DryRun
    publish = [bool]$Publish
    wiki_source_dir = $WikiSourceDir
    tutorial_count = $pages.Count
    wiki_page_count = (Get-ChildItem -LiteralPath $WikiSourceDir -Filter "*.md" -File).Count
    publish_attempted = $false
    publish_succeeded = $false
    wiki_commit = $null
    failure_reason = $null
}

if ($DryRun -and -not $Publish) {
    Write-Report -Report $report
    Write-Host "dry_run=true"
    Write-Host "wiki_source_dir=$WikiSourceDir"
    Write-Host "tutorial_pages=$($pages.Count)"
    Write-Host "publish_attempted=false"
    return
}

if ($Publish) {
    $report.publish_attempted = $true
    try {
        git ls-remote $WikiRemote | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Wiki remote is not accessible: $WikiRemote" }

        if (Test-Path -LiteralPath $WikiWorktreeDir) {
            Push-Location $WikiWorktreeDir
            try {
                git fetch origin
                git checkout master
                git pull --ff-only origin master
            } finally {
                Pop-Location
            }
        } else {
            git clone $WikiRemote $WikiWorktreeDir
            if ($LASTEXITCODE -ne 0) { throw "Wiki clone failed." }
        }

        Get-ChildItem -LiteralPath $WikiSourceDir -Filter "*.md" -File | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $WikiWorktreeDir -Force
        }

        Push-Location $WikiWorktreeDir
        try {
            git add -- *.md
            $status = git status --short
            if ($status) {
                git commit -m "Sync tutorials from main repository"
                if ($LASTEXITCODE -ne 0) { throw "Wiki commit failed." }
                $commit = (git rev-parse HEAD).Trim()
                git push origin HEAD
                if ($LASTEXITCODE -ne 0) { throw "Wiki push failed." }
                $report.publish_succeeded = $true
                $report.wiki_commit = $commit
                Write-Host "wiki_pushed=true"
                Write-Host "wiki_commit=$commit"
            } else {
                $commit = $null
                try { $commit = (git rev-parse HEAD).Trim() } catch { $commit = $null }
                $report.publish_succeeded = $true
                $report.wiki_commit = $commit
                Write-Host "wiki_no_changes=true"
                if ($commit) { Write-Host "wiki_commit=$commit" }
            }
        } finally {
            Pop-Location
        }
    } catch {
        $report.failure_reason = $_.Exception.Message
        Write-Report -Report $report
        Write-Error $report.failure_reason
        exit 1
    }
}

Write-Report -Report $report
Write-Host "wiki_page_count=$($report.wiki_page_count)"
