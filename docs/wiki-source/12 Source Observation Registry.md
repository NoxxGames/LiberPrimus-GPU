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

Stage 4A aggregate records under `data/observations/discord/stage4a-full-review-aggregate.yaml`
and `data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml` record generated bundle
counts and privacy flags only. They do not promote raw Discord messages, usernames, private URLs, or
page-image bytes into source truth.

Stage 4B records website-derived public source locks, source-health metadata, review-only visual
observations, cookie source candidates, and negative controls:

- `data/observations/archive/stage4b-promoted-source-records.yaml`
- `data/locks/third-party/stage4b-source-health-records.yaml`
- `data/observations/visual/stage4b-visual-observation-records.yaml`
- `data/observations/research/stage4b-negative-control-records.yaml`
- `data/observations/web/stage4b-cookie-candidate-source-records.yaml`

These records preserve ambiguity and stop conditions. Visual records remain
`usable_as_experiment_seed=false`.

Stage 4C adds annotation task records for the Stage 4B visual subset:

- `data/observations/visual/stage4c-visual-annotation-tasks.yaml`
- `data/observations/visual/stage4c-cuneiform-reading-candidates.yaml`
- `data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml`
- `data/observations/visual/stage4c-delimiter-annotation-tasks.yaml`
- `data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml`
- `data/observations/visual/stage4c-annotation-pack-summary.yaml`

These records make visual claims reviewable and measurable, but they still keep
`trusted_as_canonical=false`, `usable_as_experiment_seed=false`, and `solve_claim=false`.

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
Do not commit generated Stage 4A redacted streams, channel shards, topic shards, indexes, static
site files, copied LP page images, thumbnails, contact sheets, or upload archives.
Do not commit generated Stage 4B source-lock triage reports, rejected-link lists, duplicate-link
lists, or warnings under `experiments/results/source-lock-triage/stage4b/`.
Do not commit generated Stage 4C annotation sites, copied review images, grid overlays, or blank
templates under `experiments/results/visual-annotation/stage4c/`.

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

If a Stage 4C annotation task looks promising, keep coordinates, accepted readings, rejected
readings, confidence, and review status separate. A later explicit promotion stage is required
before any manifest treats it as a seed.
