# Deep Research Repository ZIP Workflow

Stage 5BD provides helper scripts for future ZIP-based Deep Research handoffs:

```powershell
.\scripts\archive\create-deep-research-repo-zip.ps1
```

```bash
scripts/archive/create-deep-research-repo-zip.sh
```

The scripts write marker files and a ZIP under `deep-research-repo-zips/stage5bd/`. That output root is ignored. The marker files are intended to let a reviewer verify the commit, branch, stage ID, expected next stage, and manifest hash from inside the archive without requiring `.git/`.

Do not commit generated ZIPs or generated marker files.
