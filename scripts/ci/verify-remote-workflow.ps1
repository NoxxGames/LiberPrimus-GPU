param(
    [string]$RepoOwner = "NoxxGames",
    [string]$RepoName = "LiberPrimus-GPU",
    [string]$Branch = "main",
    [string]$WorkflowPath = ".github/workflows/ci.yml",
    [int]$MinimumLineCount = 25
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$relativeWorkflowPath = $WorkflowPath.TrimStart("/", "\") -replace "\\", "/"
$uri = "https://raw.githubusercontent.com/$RepoOwner/$RepoName/$Branch/$relativeWorkflowPath"

Write-Host "Fetching remote workflow: $uri"
$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
$content = [string]$response.Content
$normalized = $content -replace "`r`n", "`n"
$lines = $normalized -split "`n"
if ($lines.Count -gt 0 -and $lines[-1] -eq "") {
    $lineCount = $lines.Count - 1
} else {
    $lineCount = $lines.Count
}

$firstLine = if ($lineCount -gt 0) { $lines[0] } else { "" }
if ($lineCount -le $MinimumLineCount) {
    throw "Remote workflow line count $lineCount is not greater than $MinimumLineCount."
}
if ($firstLine -match "name:\s*CI\s+on:") {
    throw "Remote workflow appears flattened: first line contains multiple top-level keys."
}

$requiredSnippets = @(
    "python-ci:",
    "cmake-cpu-smoke:",
    'python-version: "3.12"',
    "ruff check",
    "pytest -q",
    "transform-registry validate",
    "solved-baseline validate-manifest",
    "result-store validate-manifest"
)
foreach ($snippet in $requiredSnippets) {
    if (-not $content.Contains($snippet)) {
        throw "Remote workflow is missing required snippet: $snippet"
    }
}

$rawDataSnippet = "data/" + "raw"
$generatedResultSnippet = "experiments/" + "results"
$forbiddenSnippets = @(
    "secrets.",
    "upload-artifact",
    $rawDataSnippet,
    $generatedResultSnippet,
    "LPGPU_ENABLE_CUDA=ON"
)
foreach ($snippet in $forbiddenSnippets) {
    if ($content.Contains($snippet)) {
        throw "Remote workflow contains forbidden snippet: $snippet"
    }
}

Write-Host "Remote workflow validation OK"
Write-Host "line_count=$lineCount"
Write-Host "first_line=$firstLine"
