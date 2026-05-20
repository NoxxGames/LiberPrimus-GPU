# Bounded Experiment Queues

## Purpose

Run policy-approved local CPU experiments without broadening into campaigns.

Before adding or reopening an experiment family, check `docs/roadmap/staged-plan.md` and
`data/research/method-retirement-records-v0.yaml`. Stage 3Y records which noisy, negative, or
inconclusive families are blocked from widening without new source evidence.

After Stage 4L, future manifests that depend on reviewed observations should cite
observation-promotion readiness records. Readiness is not execution; every
manifest still needs a separately scoped bounded execution stage.

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

Stage 4G runs the later source-backed cookie refresh:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cookie-refresh run `
  --manifest experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml `
  --candidate-sources data/observations/web/stage4b-cookie-candidate-source-records.yaml `
  --cookie-targets data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/cookie-refresh/stage4g `
  --summary-out data/observations/web/stage4g-cookie-refresh-summary.yaml `
  --allow-warnings
```

The Stage 4G refresh should process only source-backed strings and manifest-declared variants. Generated hash JSONL and summary JSON stay in `experiments/results/cookie-refresh/stage4g/` and are not solve evidence.

Stage 4H adds CPU batch API smoke manifests. These are parity infrastructure, not unsolved-page queues:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-manifest `
  --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch run `
  --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml `
  --out-dir experiments/results/cpu-batch/stage4h `
  --allow-warnings
```

Generated Stage 4H CPU batch records stay in `experiments/results/cpu-batch/stage4h/` and are future parity anchors, not solve evidence.

Stage 4I consolidates scoring labels and calibration records for CPU batch compatibility:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli scoring consolidate `
  --out-dir experiments/results/scoring-consolidation/stage4i `
  --data-dir data/scoring `
  --allow-warnings
```

Generated Stage 4I scorer inventories and rendered reports stay in `experiments/results/scoring-consolidation/stage4i/`. Committed scoring records live under `data/scoring/`. Score labels are triage metadata only and cannot imply solved plaintext.

Stage 4P unifies result-store and score-summary reporting without running experiments:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-stage4p `
  --results-dir experiments/results/result-store-unification/stage4p `
  --summary data/research/stage4p-result-store-score-summary-unification-summary.yaml
```

Generated Stage 4P source inventory, unified result, score-summary, method-status, and cross-stage
report files stay in `experiments/results/result-store-unification/stage4p/`. They are comparison
aids only and not solve evidence.

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

If a cookie pack finds no exact match, record the negative result and move to a separately scoped manifest. After Stage 4G, do not rerun cookie work without newly source-locked exact candidate strings.

If a CPU batch adapter is missing, add a synthetic or solved-fixture-safe manifest/test, explicit deferred reason, and output hash expectation before using it in broader workflows. Stage 4O parity expectations are the CPU reference for future CUDA; do not add CUDA code to satisfy a missing CPU adapter.

If a scoring label looks strong, treat it as a review lead only. Do not convert a score into a solve claim or broaden a method family without source-backed evidence and a bounded manifest.

If a unified Stage 4P report shows missing optional generated outputs, treat that as an inventory
warning. Do not rerun broad experiments or stage generated result bodies just to fill the report.

If an observation looks ready for a future bounded run, pass it through `libreprimus observation-review`
first. Review-only visual, Discord-derived, cuneiform, dot, or negative-control records cannot become
experiment seeds by implication.

If a method family is retired or deprioritised, update the staged plan and method-retirement ledger
before adding a new manifest.

If a bounded numeric verifier stage lacks exact claims, locked raw values, or accepted annotations, record a skipped/deferred result instead of adding nearest-prime, +/-n, route, or fuzzy matching adjustments.
