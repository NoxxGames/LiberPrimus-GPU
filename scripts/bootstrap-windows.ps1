param(
    [switch]$InstallTools,
    [switch]$InstallCuda,
    [switch]$SkipCuda,
    [switch]$Configure,
    [switch]$Build,
    [switch]$Test,
    [string]$PythonVersion = "3.12"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-CommandExists {
    param([Parameter(Mandatory)][string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-WingetPackageIfMissing {
    param(
        [Parameter(Mandatory)][string]$Id,
        [Parameter(Mandatory)][string]$DisplayName
    )

    Write-Host "Checking package: $DisplayName [$Id]"
    winget search --id $Id --exact --source winget
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Package ID not found in winget source: $Id"
        return $false
    }

    winget list --id $Id --exact --source winget
    if ($LASTEXITCODE -eq 0) {
        Write-Host "$DisplayName already appears installed."
        return $true
    }

    winget install --id $Id --exact --source winget --accept-package-agreements --accept-source-agreements
    return ($LASTEXITCODE -eq 0)
}

function Find-VsWhere {
    $candidate = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path -LiteralPath $candidate) { return $candidate }
    return $null
}

function Test-VsCppWorkload {
    $vswhere = Find-VsWhere
    if ($null -eq $vswhere) { return $false }
    $path = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    return -not [string]::IsNullOrWhiteSpace($path)
}

function Find-VsDevCmd {
    $vswhere = Find-VsWhere
    if ($null -eq $vswhere) { return $null }
    $install = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ([string]::IsNullOrWhiteSpace($install)) { return $null }
    $candidate = Join-Path $install.Trim() "Common7\Tools\VsDevCmd.bat"
    if (Test-Path -LiteralPath $candidate) { return $candidate }
    return $null
}

function Invoke-DeveloperCommand {
    param([Parameter(Mandatory)][string]$Command)

    if (Test-CommandExists cl) {
        cmd /c $Command
        return $LASTEXITCODE
    }

    $vsDevCmd = Find-VsDevCmd
    if ($null -eq $vsDevCmd) {
        throw "cl.exe is unavailable and VsDevCmd.bat could not be located."
    }

    cmd /c "`"$vsDevCmd`" -arch=x64 && $Command"
    return $LASTEXITCODE
}

Write-Host "LiberPrimus Stage 0A Windows bootstrap"

if (-not $InstallTools -and -not $InstallCuda -and -not $Configure -and -not $Build -and -not $Test) {
    & (Join-Path $PSScriptRoot "verify-toolchain.ps1")
    exit $LASTEXITCODE
}

if ($InstallTools) {
    if (-not (Test-CommandExists winget)) {
        throw "WinGet is unavailable. Install tools manually; this script will not bootstrap a package manager."
    }

    if (-not (Test-CommandExists git)) { [void](Install-WingetPackageIfMissing "Git.Git" "Git for Windows") }
    if (-not (Test-CommandExists cmake)) { [void](Install-WingetPackageIfMissing "Kitware.CMake" "CMake") }
    if (-not (Test-CommandExists ninja)) { [void](Install-WingetPackageIfMissing "Ninja-build.Ninja" "Ninja") }
    if (-not (Test-CommandExists py)) { [void](Install-WingetPackageIfMissing "Python.Python.$PythonVersion" "Python $PythonVersion") }

    if (-not (Test-VsCppWorkload)) {
        winget search --id Microsoft.VisualStudio.2022.BuildTools --exact --source winget
        if ($LASTEXITCODE -ne 0) { throw "Visual Studio Build Tools package ID was not found." }
        winget install --id Microsoft.VisualStudio.2022.BuildTools --exact --source winget --accept-package-agreements --accept-source-agreements --override "--wait --quiet --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
        if ($LASTEXITCODE -ne 0) { throw "Visual Studio Build Tools install failed." }
    }
}

if ($InstallCuda -and $SkipCuda) {
    throw "Use either -InstallCuda or -SkipCuda, not both."
}

if ($InstallCuda -and -not $SkipCuda) {
    if (Test-CommandExists nvcc) {
        Write-Host "CUDA Toolkit already available; skipping install."
    } else {
        if (-not (Test-CommandExists nvidia-smi)) {
            throw "CUDA install skipped because no NVIDIA runtime was detected."
        }
        winget search --id Nvidia.CUDA --exact --source winget
        if ($LASTEXITCODE -ne 0) {
            throw "Nvidia.CUDA package ID not found. Install CUDA Toolkit manually from NVIDIA."
        }
        winget install --id Nvidia.CUDA --exact --source winget --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) { throw "CUDA Toolkit install failed or requires manual intervention." }
    }
}

if ($Configure) {
    & (Join-Path $PSScriptRoot "configure-windows.ps1")
}

if ($Build) {
    $code = Invoke-DeveloperCommand "cmake --build build/msvc-debug"
    if ($code -ne 0) { exit $code }
}

if ($Test) {
    $code = Invoke-DeveloperCommand "ctest --test-dir build/msvc-debug --output-on-failure"
    if ($code -ne 0) { exit $code }
}
