# Source Harvester CLI

The Stage 5AF CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester --help
```

Core commands:

- `validate-manifest --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml`
- `plan --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml --out experiments/results/source-harvester/stage5af/harvest_plan.json`
- `build-bundles --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml --out-root experiments/results/source-harvester/stage5af/research_bundles_preview`
- `summarize --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml --out experiments/results/source-harvester/stage5af/summary.json`
- `validate-stage5af ...`
- `summary --summary data/source-harvester/stage5af-source-harvester-summary.yaml`

Real network use is opt-in and not part of CI:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester fetch `
  --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
  --source-id fandom_liber_primus_ideas `
  --out-root source-harvester-output `
  --allow-network `
  --rate-limit-seconds 3
```

Do not use Google Drive as storage. Export Google/Dropbox/Colab material manually into an ignored local root, then inventory it locally.
