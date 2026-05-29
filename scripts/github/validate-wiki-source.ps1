[CmdletBinding()]
param(
    [string]$TutorialDir = "tutorials",
    [string]$WikiSourceDir = "docs/wiki-source"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

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

$errors = New-Object System.Collections.Generic.List[string]

if (-not (Test-Path -LiteralPath $TutorialDir)) {
    $errors.Add("tutorial_dir_missing=$TutorialDir")
}
if (-not (Test-Path -LiteralPath $WikiSourceDir)) {
    $errors.Add("wiki_source_dir_missing=$WikiSourceDir")
}

$homePath = Join-Path $WikiSourceDir "Home.md"
$sidebar = Join-Path $WikiSourceDir "_Sidebar.md"
if (-not (Test-Path -LiteralPath $homePath)) { $errors.Add("missing_home=$homePath") }
if (-not (Test-Path -LiteralPath $sidebar)) { $errors.Add("missing_sidebar=$sidebar") }

$tutorials = @()
if (Test-Path -LiteralPath $TutorialDir) {
    $tutorials = @(Get-ChildItem -LiteralPath $TutorialDir -Filter "*.md" -File | Sort-Object Name)
}

foreach ($tutorial in $tutorials) {
    $pageName = Convert-ToWikiPageName -FileName $tutorial.Name
    $pagePath = Join-Path $WikiSourceDir $pageName
    if (-not (Test-Path -LiteralPath $pagePath)) {
        $errors.Add("missing_wiki_page=$pageName")
        continue
    }
    $content = Get-Content -LiteralPath $pagePath -Raw
    if ($content -notmatch "repository tutorial file is the source of truth") {
        $errors.Add("missing_source_of_truth_notice=$pageName")
    }
    if ($content -match "third_party[/\\]LiberPrimusDiscordChats[/\\].+\.html") {
        $errors.Add("raw_discord_html_path_in_wiki_page=$pageName")
    }
}

if (Test-Path -LiteralPath $WikiSourceDir) {
    Get-ChildItem -LiteralPath $WikiSourceDir -Filter "*.md" -File | ForEach-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw
        if ($content -match "`"record_type`"\s*:\s*`"discord_extracted_link`"") {
            $errors.Add("possible_generated_output_dump=$($_.Name)")
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "wiki_source_valid=true"
Write-Host "tutorial_count=$($tutorials.Count)"
$wikiPages = @(Get-ChildItem -LiteralPath $WikiSourceDir -Filter "*.md" -File)
Write-Host "wiki_page_count=$($wikiPages.Count)"
