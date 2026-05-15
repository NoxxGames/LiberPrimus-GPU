param(
    [switch]$EnableCuda,
    [ValidateSet("Debug", "Release", "RelWithDebInfo", "MinSizeRel")]
    [string]$BuildType = "Debug",
    [string]$Generator = "Ninja",
    [string]$BuildDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-CommandExists {
    param([Parameter(Mandatory)][string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Find-Ninja {
    $cmd = Get-Command ninja -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }

    $wingetRoot = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages"
    if (Test-Path -LiteralPath $wingetRoot) {
        $candidate = Get-ChildItem -Path $wingetRoot -Recurse -Filter ninja.exe -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -ne $candidate) { return $candidate.FullName }
    }

    return $null
}

function Find-VsDevCmd {
    $vswhere = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path -LiteralPath $vswhere) {
        $install = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
        if (-not [string]::IsNullOrWhiteSpace($install)) {
            $candidate = Join-Path $install.Trim() "Common7\Tools\VsDevCmd.bat"
            if (Test-Path -LiteralPath $candidate) { return $candidate }
        }
    }
    return $null
}

function ConvertTo-CmdArgument {
    param([Parameter(Mandatory)][string]$Value)
    if ($Value -match '[\s"]') {
        return '"' + ($Value -replace '"', '\"') + '"'
    }
    return $Value
}

if ([string]::IsNullOrWhiteSpace($BuildDir)) {
    if ($EnableCuda) { $BuildDir = "build/cuda-$($BuildType.ToLowerInvariant())" }
    else { $BuildDir = "build/msvc-$($BuildType.ToLowerInvariant())" }
}

$cmakeArgs = @(
    "-S", ".",
    "-B", $BuildDir,
    "-G", $Generator,
    "-DCMAKE_BUILD_TYPE=$BuildType",
    "-DLPGPU_BUILD_TESTS=ON"
)

if ($EnableCuda) {
    $cmakeArgs += "-DLPGPU_ENABLE_CUDA=ON"
    $cmakeArgs += "-DCMAKE_CUDA_ARCHITECTURES=89"
} else {
    $cmakeArgs += "-DLPGPU_ENABLE_CUDA=OFF"
}

if ($Generator -eq "Ninja") {
    $ninja = Find-Ninja
    if ($null -eq $ninja) { throw "Ninja was not found. Install Ninja or choose another generator." }
    $cmakeArgs += "-DCMAKE_MAKE_PROGRAM=$ninja"
}

Write-Host "Configuring $BuildDir"

if (Test-CommandExists cl) {
    cmake @cmakeArgs
    exit $LASTEXITCODE
}

$vsDevCmd = Find-VsDevCmd
if ($null -eq $vsDevCmd) {
    throw "cl.exe is unavailable and VsDevCmd.bat could not be located."
}

$cmakeCommand = "cmake " + (($cmakeArgs | ForEach-Object { ConvertTo-CmdArgument $_ }) -join " ")
cmd /c "`"$vsDevCmd`" -arch=x64 && $cmakeCommand"
exit $LASTEXITCODE
