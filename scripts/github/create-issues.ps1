[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,
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

function Get-IssueTitle {
    param([string]$Text)
    foreach ($line in ($Text -split "`r?`n")) {
        if ($line -match "^#\s+(.+)$") { return $Matches[1].Trim() }
    }
    throw "Issue seed has no H1 title."
}

function Get-IssueLabels {
    param([string]$Text)
    foreach ($line in ($Text -split "`r?`n")) {
        if ($line -match "^Suggested labels:\s*(.+)$") {
            return @($Matches[1].Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        }
    }
    return @()
}

$gh = Find-Gh
& $gh repo view $Repo --json nameWithOwner | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Repository verification failed: $Repo"
}

$issueDir = Join-Path (Get-Location) "docs/github/issues"
$reportPath = Join-Path (Get-Location) "docs/github/issue-bootstrap-report.md"
$files = Get-ChildItem -LiteralPath $issueDir -Filter "*.md" | Where-Object { $_.Name -ne "README.md" } | Sort-Object Name
$created = @()
$skipped = @()

foreach ($file in $files) {
    $body = Get-Content -LiteralPath $file.FullName -Raw
    $title = Get-IssueTitle -Text $body
    $labels = Get-IssueLabels -Text $body
    $search = "$title in:title"
    $existingJson = & $gh issue list --repo $Repo --state all --search $search --json number,title,state,url
    if ($LASTEXITCODE -ne 0) { throw "Issue search failed for title: $title" }
    $parsedExisting = @()
    if ($existingJson.Trim()) {
        $parsedExisting = @($existingJson | ConvertFrom-Json)
    }
    $existing = @(
        $parsedExisting | Where-Object {
            $null -ne $_.PSObject.Properties["title"] -and $_.title -eq $title
        }
    )
    if ($existing.Count -gt 0) {
        $skipped += [pscustomobject]@{ title = $title; url = $existing[0].url; state = $existing[0].state }
        Write-Host "skip_existing=$title"
        continue
    }

    if ($DryRun) {
        $created += [pscustomobject]@{ title = $title; url = "(dry-run)"; state = "dry-run" }
        Write-Host "dry_run_create=$title"
        continue
    }

    $args = @("issue", "create", "--repo", $Repo, "--title", $title, "--body-file", $file.FullName)
    if ($labels.Count -gt 0) {
        $args += @("--label", ($labels -join ","))
    }
    $url = (& $gh @args).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Issue creation failed for title: $title" }
    $created += [pscustomobject]@{ title = $title; url = $url; state = "created" }
    Write-Host "created=$url"
}

$lines = @(
    "# GitHub Issue Bootstrap Report",
    "",
    "- Repo: ``$Repo``",
    "- Dry run: ``$($DryRun.IsPresent.ToString().ToLowerInvariant())``",
    "- Created count: ``$($created.Count)``",
    "- Skipped existing count: ``$($skipped.Count)``",
    "",
    "## Created",
    ""
)
foreach ($item in $created) {
    $lines += "- $($item.title) - $($item.url)"
}
$lines += @("", "## Skipped Existing", "")
foreach ($item in $skipped) {
    $lines += "- $($item.title) - $($item.url) [$($item.state)]"
}
$lines += ""
Set-Content -LiteralPath $reportPath -Value $lines -Encoding utf8

Write-Host "issues_created_count=$($created.Count)"
Write-Host "issues_skipped_existing_count=$($skipped.Count)"
Write-Host "report_path=$reportPath"
