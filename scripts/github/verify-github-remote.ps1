[CmdletBinding()]
param(
    [string]$Repo
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Find-Gh {
    $cmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }

    $candidates = @(
        "C:\Program Files\GitHub CLI\gh.exe",
        "C:\Program Files (x86)\GitHub CLI\gh.exe",
        "$env:LOCALAPPDATA\GitHub CLI\gh.exe"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    throw "GitHub CLI 'gh' was not found."
}

function Convert-GitHubRemoteToRepo {
    param([string]$RemoteUrl)

    if ($RemoteUrl -match "github\.com[:/](?<owner>[^/]+)/(?<repo>[^/.]+)(\.git)?$") {
        return "$($Matches.owner)/$($Matches.repo)"
    }
    return $null
}

$gh = Find-Gh
& $gh auth status | Out-Host
$login = (& $gh api user --jq ".login").Trim()

if (-not $Repo) {
    $Repo = [Environment]::GetEnvironmentVariable("LIBERPRIMUS_GITHUB_REPO")
}

$originUrl = $null
try {
    $originUrl = (git remote get-url origin 2>$null).Trim()
} catch {
    $originUrl = $null
}

if (-not $Repo -and $originUrl) {
    $Repo = Convert-GitHubRemoteToRepo -RemoteUrl $originUrl
}

if (-not $Repo) {
    $Repo = "$login/LiberPrimus-GPU"
}

$repoJson = & $gh repo view $Repo --json nameWithOwner,url,sshUrl,isPrivate,defaultBranchRef,hasIssuesEnabled,hasWikiEnabled
if ($LASTEXITCODE -ne 0) {
    throw "Could not view GitHub repository: $Repo"
}
$repoInfo = $repoJson | ConvertFrom-Json
$targetName = [string]$repoInfo.nameWithOwner

$originVerified = $true
if ($originUrl) {
    $originRepo = Convert-GitHubRemoteToRepo -RemoteUrl $originUrl
    if (-not $originRepo) {
        throw "origin is not a GitHub remote: $originUrl"
    }
    $originJson = & $gh repo view $originRepo --json nameWithOwner 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "origin repository could not be resolved through GitHub: $originRepo"
    }
    $originResolved = ($originJson | ConvertFrom-Json).nameWithOwner
    if ($originResolved -ne $targetName) {
        throw "origin resolves to $originResolved, expected $targetName"
    }
} else {
    $originVerified = $false
}

[ordered]@{
    gh = $gh
    authenticated_user = $login
    target_repo = $targetName
    repo_url = $repoInfo.url
    ssh_url = $repoInfo.sshUrl
    is_private = $repoInfo.isPrivate
    default_branch = $repoInfo.defaultBranchRef.name
    has_issues_enabled = $repoInfo.hasIssuesEnabled
    has_wiki_enabled = $repoInfo.hasWikiEnabled
    origin_url = $originUrl
    origin_verified = $originVerified
} | ConvertTo-Json -Depth 4
