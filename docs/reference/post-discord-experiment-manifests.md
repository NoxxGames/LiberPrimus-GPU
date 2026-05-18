# Post-Discord Experiment Manifests

Stage 3R adds `libreprimus discord-leads` commands for redacted lead promotion and disabled post-Discord manifest creation.

## Promote Leads

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads promote `
  --review-dir experiments/results/discord-review-bundles/stage3q `
  --stage3o-links data/observations/discord/promoted-public-source-links-stage3o.yaml `
  --stage3o-methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml `
  --stage3o-numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml `
  --source-registry data/observations/archive/source-archive-records-v0.yaml `
  --visual-registry data/observations/visual/visual-numeric-observations-v0.yaml `
  --cookie-records data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/discord-lead-promotion/stage3r `
  --promoted-sources-out data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations-out data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls-out data/observations/discord/stage3r-negative-control-records.yaml `
  --audit-summary-out data/observations/discord/stage3r-promotion-audit-summary.yaml `
  --allow-missing `
  --allow-warnings
```

## Build Manifests

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads build-manifests `
  --audit-summary data/observations/discord/stage3r-promotion-audit-summary.yaml `
  --out-dir experiments/manifests/post-discord `
  --allow-warnings
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads validate `
  --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls data/observations/discord/stage3r-negative-control-records.yaml `
  --manifest-dir experiments/manifests/post-discord `
  --allow-empty
```

These commands do not execute experiments. Generated audit output remains ignored.

Stage 3S executes one manifest through the dedicated Onion 7 CLI documented at `docs/reference/onion7-seed-pack-cli.md`. Do not execute other post-Discord manifests in the same stage.
