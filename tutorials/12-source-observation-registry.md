# Source Observation Registry

## Purpose

Store reviewable source links, archive records, visual observations, cookie/hash artefacts, and
Discord-promoted candidates without turning them into facts.

## Key Paths

- `data/observations/archive/`
- `data/observations/visual/`
- `data/observations/web/`
- `data/observations/discord/`
- `data/locks/third-party/`

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli archive validate-sources `
  --records data/observations/archive/source-archive-records-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli discord-promote validate-promoted `
  --links data/observations/discord/promoted-public-source-links-stage3o.yaml `
  --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml `
  --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml `
  --allow-empty
```

## Expected Outputs

Validation should confirm records are redacted, reviewable, and noncanonical.

## What Not To Commit

Raw source material, raw chat logs, generated extraction dumps, or unreviewed claims as facts.

## Troubleshooting

If a promoted item looks useful, promote the public source through source-classification policy
before turning it into any experiment seed.
