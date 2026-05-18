> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

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
- `data/observations/stego/`
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
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads validate `
  --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls data/observations/discord/stage3r-negative-control-records.yaml `
  --manifest-dir experiments/manifests/post-discord `
  --allow-empty
```

## Expected Outputs

Validation should confirm records are redacted, reviewable, and noncanonical.

Stage 3P transform outputs can support later review, but the generated flags themselves are not
registry records and have `usable_as_experiment_seed=false`.

Stage 3Q redacted Discord topic shards can support later lead review, but the shards are generated
outputs and are not committed evidence. The committed aggregate records counts and privacy flags
only.

Stage 3R promoted records can support future bounded manifest review, but they are still
reviewable leads. Discord-only claims are not source truth. Negative controls should be preserved
when known false-positive classes appear in future review.

Stage 3S executes one post-Discord manifest based on reviewed Onion 7 observations. The raw 4x4
table values and derived tables remain separate, and the generated candidate records are ignored
experiment outputs rather than registry records.

Stage 3T verifies exact GP/rune and derived numeric claims from promoted observations. Claims
without exact spans stay classified instead of being forced into neighbouring-span searches.
Generated verification records are ignored experiment outputs rather than registry records.

Stage 3U tests manifest-declared signed/public strings against the archived cookie/hash records.
The generated hash candidate records are ignored experiment outputs rather than registry records.

Stage 3V records OutGuess artefact metadata and source-lock placeholders under `data/observations/stego/`
and `data/locks/third-party/outguess-regression/`. These records are regression fixtures, not proof of
hidden content. Missing tools or assets are valid skipped states.

## What Not To Commit

Raw source material, raw chat logs, generated extraction dumps, or unreviewed claims as facts.
Do not commit generated image-transform outputs, contact sheets, review pages, or derived images.
Do not commit generated Discord review shards, redacted stream JSONL, or local review indexes.
Do not commit generated Stage 3R promotion-audit JSONL files.
Do not commit generated Stage 3S post-Discord candidate JSONL, top-candidate JSONL, summary JSON,
or score-detail files.
Do not commit generated Stage 3T verification JSONL, per-status JSONL, summary JSON, or warning
files.
Do not commit generated Stage 3U hash candidate JSONL, exact-match JSONL, summary JSON, or warning
files.
Do not commit generated Stage 3V extraction JSONL, tool JSON, summary JSON, synthetic inputs, or
extracted payloads.

## Troubleshooting

If a promoted item looks useful, promote the public source through source-classification policy
before turning it into any experiment seed.

If a disabled Stage 3R manifest looks ready to run, execute it only in a new bounded stage with
explicit candidate-count validation.

If a Stage 3S candidate looks useful, promote only a summary and queue a new manifest-backed
follow-up. Do not promote generated candidate text as source evidence.

If a Stage 3T verification result looks useful, promote only the verified claim summary and claim
ID. Do not promote generated verification dumps as source evidence.

If a Stage 3U exact preimage candidate appears, promote only a reviewed summary and independently
verify source provenance before any interpretation.

If a Stage 3V extraction produces bytes, interpret it only when an expected payload hash exists and
matches. Otherwise keep it as an ignored reference extraction record.
