param(
    [Parameter(Mandatory = $true)]
    [int]$Shard,
    [Parameter(Mandatory = $true)]
    [string]$Plan
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$Files = @(& $Python -c "import json, sys, yaml; from pathlib import Path; payload=yaml.safe_load(Path(sys.argv[1]).read_text(encoding='utf-8')) or {}; shard_id=f'pytest-shard-{int(sys.argv[2]):02d}'; matches=[item for item in payload.get('shards', []) if item.get('shard_id') == shard_id]; sys.exit(f'Pytest shard not found in plan: {shard_id}') if not matches else None; print('\n'.join(matches[0].get('test_files', [])))" $Plan $Shard)
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ($Files.Count -eq 0) {
    throw "Pytest shard has no files: $Shard"
}
Write-Host ("Rerunning pytest-shard-{0:D2}" -f $Shard)
& $Python -m pytest -q @Files
exit $LASTEXITCODE
