param(
    [string[]]$BuildDirs = @("build"),
    [switch]$PythonCaches
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$buildRoot = Join-Path $repoRoot "build"

foreach ($dir in $BuildDirs) {
    $target = if ([System.IO.Path]::IsPathRooted($dir)) { $dir } else { Join-Path $repoRoot $dir }
    if (-not (Test-Path -LiteralPath $target)) {
        Write-Host "Skipping missing path: $target"
        continue
    }

    $resolved = (Resolve-Path -LiteralPath $target).Path
    if ($resolved -ne $buildRoot -and -not $resolved.StartsWith($buildRoot + [System.IO.Path]::DirectorySeparatorChar)) {
        throw "Refusing to delete outside build directory: $resolved"
    }

    Write-Host "Removing build path: $resolved"
    Remove-Item -LiteralPath $resolved -Recurse -Force
}

if ($PythonCaches) {
    foreach ($cache in @(".pytest_cache", ".mypy_cache", ".ruff_cache")) {
        $path = Join-Path $repoRoot $cache
        if (Test-Path -LiteralPath $path) {
            Write-Host "Removing Python cache: $path"
            Remove-Item -LiteralPath $path -Recurse -Force
        }
    }
}
