# Bounded Experiment Queues

## Purpose

Run policy-approved local CPU experiments without broadening into campaigns.

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

## Expected Outputs

Policy checks should pass for bounded CPU-only items and fail for over-budget examples.

The Stage 3S Onion 7 run should execute `72` candidates under a cap of `144`. Generated candidates stay in `experiments/results/post-discord/stage3s/` and are not solve evidence.

The Stage 3T GP/rune verifier should process exact claims under a cap of `64`. Generated verification JSONL and summary files stay in `experiments/results/post-discord/stage3t/` and are not solve evidence.

## What Not To Commit

Do not commit generated candidate dumps, top-candidate JSONL, verification JSONL, summary JSON, SQLite files, or broad-search outputs.

## Troubleshooting

If a queue item lacks an executor, record it as deferred instead of faking output.

If an Onion 7 run appears interesting, inspect the generated top candidates locally and queue a separate bounded follow-up instead of broadening routes or adding speculative value spaces.

If a GP/rune claim is `missing_source_span`, improve source/span linking in a separate follow-up instead of searching neighbouring spans to make the claim true.
