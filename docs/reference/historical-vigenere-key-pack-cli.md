# Historical Vigenere Key-Pack CLI

Run the Stage 3I historical motif key pack:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-vigenere-key-pack `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_vig_history_key_pack_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3i `
  --top-k 25 `
  --allow-warnings
```

Summarize the generated ignored output:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3i
```

The command executes only the manifest-declared keys and modes. It does not expand the key list, perform dictionary search, use CUDA, commit generated outputs, or make solve claims.

