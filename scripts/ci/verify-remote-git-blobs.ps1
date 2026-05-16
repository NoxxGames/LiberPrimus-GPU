param(
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [int]$MinimumWorkflowLines = 25,
    [int]$MinimumGitattributesLines = 10,
    [switch]$CheckRawUrl,
    [switch]$CheckGitHubApi,
    [string]$RepoOwner = "NoxxGames",
    [string]$RepoName = "LiberPrimus-GPU"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-LineReport {
    param([string]$Content)
    $normalized = $Content -replace "`r`n", "`n"
    $lines = $normalized -split "`n"
    if ($lines.Count -gt 0 -and $lines[-1] -eq "") {
        $lineCount = $lines.Count - 1
    } else {
        $lineCount = $lines.Count
    }
    $firstLine = if ($lineCount -gt 0) { $lines[0] } else { "" }
    return @{
        LineCount = $lineCount
        FirstLine = $firstLine
    }
}

function Get-RemoteBlob {
    param([string]$Path)
    # Authoritative remote verification uses git show against the fetched remote blob.
    $spec = "${Remote}/${Branch}:$Path"
    $lines = & git show $spec
    if ($LASTEXITCODE -ne 0) {
        throw "git show failed for $spec"
    }
    return ($lines -join "`n") + "`n"
}

function Assert-Contains {
    param([string]$Content, [string]$Snippet, [string]$Label)
    if (-not $Content.Contains($Snippet)) {
        throw "$Label is missing required snippet: $Snippet"
    }
}

function Warn-RawOrApiMismatch {
    param([string]$Label, [int]$BlobLines, [int]$ObservedLines)
    if ($BlobLines -ne $ObservedLines) {
        Write-Warning "$Label line count differs from git blob ($ObservedLines vs $BlobLines). Raw/API mismatch warning only; git blob remains authoritative."
    }
}

Write-Host "Fetching $Remote"
& git fetch $Remote | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "git fetch $Remote failed"
}

$workflow = Get-RemoteBlob ".github/workflows/ci.yml"
$attributes = Get-RemoteBlob ".gitattributes"
$workflowReport = Get-LineReport $workflow
$attributesReport = Get-LineReport $attributes

if ($workflowReport.LineCount -le $MinimumWorkflowLines) {
    throw "Remote git blob workflow line count $($workflowReport.LineCount) is not greater than $MinimumWorkflowLines."
}
if ($attributesReport.LineCount -le $MinimumGitattributesLines) {
    throw "Remote git blob .gitattributes line count $($attributesReport.LineCount) is not greater than $MinimumGitattributesLines."
}
if ($workflowReport.FirstLine -match "name:\s*CI\s+on:") {
    throw "Remote git blob workflow appears flattened."
}
if ($attributesReport.FirstLine -match "\*\s+text=auto\s+\.gitattributes") {
    throw "Remote git blob .gitattributes appears flattened."
}

foreach ($snippet in @(
    "python-ci:",
    "cmake-cpu-smoke:",
    'python-version: "3.12"',
    "ruff check",
    "pytest -q",
    "transform-registry validate",
    "solved-baseline validate-manifest",
    "result-store validate-manifest"
)) {
    Assert-Contains $workflow $snippet "workflow"
}

foreach ($snippet in @(
    "*.json text eol=lf",
    "*.yml text eol=lf",
    "*.sh text eol=lf",
    "*.sha256 text eol=lf"
)) {
    Assert-Contains $attributes $snippet ".gitattributes"
}

if ($CheckRawUrl) {
    foreach ($path in @(".github/workflows/ci.yml", ".gitattributes")) {
        $rawPath = $path.TrimStart("/", "\") -replace "\\", "/"
        $uri = "https://raw.githubusercontent.com/$RepoOwner/$RepoName/$Branch/$rawPath"
        $content = [string](Invoke-WebRequest -Uri $uri -UseBasicParsing -Headers @{"Cache-Control" = "no-cache"; "Pragma" = "no-cache"}).Content
        $report = Get-LineReport $content
        $blobLines = if ($path -eq ".github/workflows/ci.yml") { $workflowReport.LineCount } else { $attributesReport.LineCount }
        Warn-RawOrApiMismatch "raw URL $path" $blobLines $report.LineCount
        Write-Host "raw_url_${path}_line_count=$($report.LineCount)"
    }
}

if ($CheckGitHubApi) {
    foreach ($path in @(".github/workflows/ci.yml", ".gitattributes")) {
        $apiPath = $path.TrimStart("/", "\") -replace "\\", "/"
        $uri = "https://api.github.com/repos/$RepoOwner/$RepoName/contents/$apiPath`?ref=$Branch"
        try {
            $json = Invoke-WebRequest -Uri $uri -UseBasicParsing -Headers @{"User-Agent" = "liberprimus-remote-blob-verifier"} | ConvertFrom-Json
            $bytes = [Convert]::FromBase64String(($json.content -replace "\s", ""))
            $content = [System.Text.Encoding]::UTF8.GetString($bytes)
            $report = Get-LineReport $content
            $blobLines = if ($path -eq ".github/workflows/ci.yml") { $workflowReport.LineCount } else { $attributesReport.LineCount }
            Warn-RawOrApiMismatch "GitHub API $path" $blobLines $report.LineCount
            Write-Host "github_api_${path}_line_count=$($report.LineCount)"
        } catch {
            Write-Warning "GitHub API check skipped for ${path}: $($_.Exception.Message)"
        }
    }
}

Write-Host "Remote git blob validation OK"
Write-Host "git_blob_workflow_line_count=$($workflowReport.LineCount)"
Write-Host "git_blob_gitattributes_line_count=$($attributesReport.LineCount)"
