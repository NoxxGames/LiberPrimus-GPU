# Vigenere Key-Pack CLI

Stage 3F adds a bounded Vigenere key-pack command:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-vigenere-key-pack `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_vig_lp_evidence_pack_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3f `
  --top-k 25 `
  --allow-warnings
```

Summarize the generated ignored output:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3f
```

The command validates the queue item, operator policy, key count, reset modes, advance modes, and `12 * 2 * 2 = 48` candidate count before writing candidate records.

Generated outputs are ignored. Do not commit `candidate_records.jsonl`, `top_candidates.jsonl`, `summary.json`, or score-detail JSONL files.
