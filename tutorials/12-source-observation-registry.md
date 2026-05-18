# Source Observation Registry

## Purpose

Store reviewable source links, archive records, visual observations, cookie/hash artefacts, and
Discord-promoted candidates without turning them into facts. Stage 3P visual transform candidates
are also review leads only; selected items must be promoted through observation review before any
future experiment can use them.

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
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review validate-bundles `
  --results-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing
```

## Expected Outputs

Validation should confirm records are redacted, reviewable, and noncanonical.

Stage 3P transform outputs can support later review, but the generated flags themselves are not
registry records and have `usable_as_experiment_seed=false`.

Stage 3Q redacted Discord topic shards can support later lead review, but the shards are generated
outputs and are not committed evidence. The committed aggregate records counts and privacy flags
only.

## What Not To Commit

Raw source material, raw chat logs, generated extraction dumps, or unreviewed claims as facts.
Do not commit generated image-transform outputs, contact sheets, review pages, or derived images.
Do not commit generated Discord review shards, redacted stream JSONL, or local review indexes.

## Troubleshooting

If a promoted item looks useful, promote the public source through source-classification policy
before turning it into any experiment seed.
