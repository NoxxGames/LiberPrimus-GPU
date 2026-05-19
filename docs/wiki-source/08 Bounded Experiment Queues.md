> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Bounded Experiment Queues

## Purpose

Run policy-approved local CPU experiments without broadening into campaigns.

Before adding or reopening an experiment family, check `docs/roadmap/staged-plan.md` and
`data/research/method-retirement-records-v0.yaml`. Stage 3Y records which noisy, negative, or
inconclusive families are blocked from widening without new source evidence.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment validate-policy `
  --policy experiments/policies/operator-policy-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment dry-run-stage3e `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --out experiments/results/bounded-auto-runs/stage3e/stage3e_queue_dry_run_summary.json `
  --allow-warnings
```

Post-Discord manifest execution uses the same bounded policy expectations. Stage 3S runs only the Onion 7 explicit seed pack:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-onion7-seed-pack `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml `
  --out-dir experiments/results/post-discord/stage3s `
  --top-k 25 `
  --allow-warnings
```

Stage 3T runs only the GP/rune claim verifier:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-gp-rune-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-gp-rune-verifier `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --visual-observations data/observations/visual/visual-numeric-observations-v0.yaml `
  --out-dir experiments/results/post-discord/stage3t `
  --allow-warnings
```

Stage 3U runs only the cookie SHA-256 signed-variant pack:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-cookie-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-cookie-signed-variants `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/post-discord/stage3u `
  --allow-warnings
```

## Expected Outputs

Policy checks should pass for bounded CPU-only items and fail for over-budget examples.

The Stage 3S Onion 7 run should execute `72` candidates under a cap of `144`. Generated candidates stay in `experiments/results/post-discord/stage3s/` and are not solve evidence.

The Stage 3T GP/rune verifier should process exact claims under a cap of `64`. Generated verification JSONL and summary files stay in `experiments/results/post-discord/stage3t/` and are not solve evidence.

The Stage 3U cookie signed-variant pack should process only manifest-declared SHA-256 candidates under a cap of `576`. Generated hash JSONL and summary files stay in `experiments/results/post-discord/stage3u/` and are not solve evidence.

Stage 4D runs only bounded no-fudge numeric and metadata audits from the Stage 4B disabled backlog:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric run `
  --manifest-dir experiments/manifests/stage4b-disabled `
  --stage4b-visual data/observations/visual/stage4b-visual-observation-records.yaml `
  --stage4c-tasks data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --stage4c-cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --stage4c-dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --stage4c-delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --stage4c-negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --out-dir experiments/results/bounded-numeric/stage4d `
  --allow-warnings
```

Generated Stage 4D result records stay in `experiments/results/bounded-numeric/stage4d/` and are not solve evidence.

## What Not To Commit

Do not commit generated candidate dumps, top-candidate JSONL, verification JSONL, hash candidate JSONL, exact-match JSONL, summary JSON, SQLite files, or broad-search outputs.

## Troubleshooting

If a queue item lacks an executor, record it as deferred instead of faking output.

If an Onion 7 run appears interesting, inspect the generated top candidates locally and queue a separate bounded follow-up instead of broadening routes or adding speculative value spaces.

If a GP/rune claim is `missing_source_span`, improve source/span linking in a separate follow-up instead of searching neighbouring spans to make the claim true.

If a cookie pack finds no exact match, record the negative result and move to a separately scoped manifest. Do not add strings or variants to a completed run after the fact.

If a method family is retired or deprioritised, update the staged plan and method-retirement ledger
before adding a new manifest.

If a bounded numeric verifier stage lacks exact claims, locked raw values, or accepted annotations, record a skipped/deferred result instead of adding nearest-prime, +/-n, route, or fuzzy matching adjustments.
