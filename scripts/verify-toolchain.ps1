Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-CommandExists {
    param([Parameter(Mandatory)][string]$Name)
    return $null -ne (Get-CommandPath $Name)
}

function Get-CommandPath {
    param([Parameter(Mandatory)][string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }

    if ($Name -eq "ninja") {
        $wingetRoot = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages"
        if (Test-Path -LiteralPath $wingetRoot) {
            $candidate = Get-ChildItem -Path $wingetRoot -Recurse -Filter ninja.exe -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($null -ne $candidate) { return $candidate.FullName }
        }
    }

    return $null
}

function Find-VsWhere {
    $candidate = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path -LiteralPath $candidate) { return $candidate }
    return $null
}

function Find-VsInstall {
    $vswhere = Find-VsWhere
    if ($null -eq $vswhere) { return $null }
    $path = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ([string]::IsNullOrWhiteSpace($path)) { return $null }
    return $path.Trim()
}

function Get-VersionLine {
    param([Parameter(Mandatory)][string]$Command, [string[]]$Arguments = @("--version"))
    $path = Get-CommandPath $Command
    if ($null -eq $path) { return "missing" }
    try {
        $output = & $path @Arguments 2>&1 | Select-Object -First 1
        if ($null -eq $output) { return "present" }
        return [string]$output
    } catch {
        return "present but version failed: $($_.Exception.Message)"
    }
}

Write-Host "LiberPrimus Stage 0A toolchain verification"
Write-Host "WorkingDirectory: $((Get-Location).Path)"
Write-Host "OS: $([System.Runtime.InteropServices.RuntimeInformation]::OSDescription)"
Write-Host "PowerShell: $($PSVersionTable.PSVersion)"

$commands = @("git", "cmake", "ninja", "py", "python", "cl", "nvcc", "nvidia-smi")
foreach ($command in $commands) {
    Write-Host "$command.present: $(Test-CommandExists $command)"
    Write-Host "$command.path: $(Get-CommandPath $command)"
}

Write-Host "git.version: $(Get-VersionLine git)"
Write-Host "cmake.version: $(Get-VersionLine cmake)"
Write-Host "ninja.version: $(Get-VersionLine ninja)"
Write-Host "py.versions:"
if (Test-CommandExists py) {
    py -0p
}
Write-Host "python.version: $(Get-VersionLine python)"
Write-Host "nvcc.version: $(Get-VersionLine nvcc)"
Write-Host "nvidia-smi.present: $(Test-CommandExists nvidia-smi)"
Write-Host "CUDA_PATH: $env:CUDA_PATH"

$vsInstall = Find-VsInstall
Write-Host "VSBuildTools.present: $($null -ne $vsInstall)"
Write-Host "VSBuildTools.path: $vsInstall"
Write-Host "MSVCEnvironmentActive: $(Test-CommandExists cl)"
