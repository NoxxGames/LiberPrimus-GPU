# GitHub CLI Troubleshooting

## Purpose

Stage 2C-followup-2 keeps GitHub Actions remote workflow verification independent of `gh`, but `gh` is still useful for issue comments and run observation.

## Check Availability

On Windows:

```powershell
where gh
gh --version
gh auth status
```

PowerShell can also inspect command resolution:

```powershell
Get-Command gh -ErrorAction SilentlyContinue
```

## Common Windows Install Paths

Check these locations when Codex or another shell cannot find `gh` even though a user terminal can:

```powershell
C:\Program Files\GitHub CLI\gh.exe
C:\Program Files (x86)\GitHub CLI\gh.exe
$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe
```

If one exists, use the absolute path for optional run checks:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" run list --repo NoxxGames/LiberPrimus-GPU --workflow ci.yml --limit 5
```

## PATH Mismatch

Different shells can inherit different PATH values. A desktop app shell can miss a freshly installed CLI until the app is restarted, while a regular terminal can already see it.

## Remote Workflow Verification Without gh

The remote workflow verifier fetches the public raw GitHub URL and does not require GitHub authentication:

```powershell
.\scripts\ci\verify-remote-workflow.ps1 -RepoOwner NoxxGames -RepoName LiberPrimus-GPU -Branch main -WorkflowPath ".github/workflows/ci.yml"
```

Use this after pushing workflow changes to confirm the remote raw file is readable multi-line YAML and still contains the required CI commands.
