# Bounded Vigenere Key-List CLI

Stage 3D adds a bounded explicit-key Vigenere command:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-vigenere-key-list `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3c-bounded-cpu-queue.yaml `
  --item-id stage3c-small-vigenere-known-motif-key-list `
  --out-dir experiments/results/bounded-auto-runs/stage3d `
  --top-k 4 `
  --allow-warnings
```

Print the generated summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3d
```

The command enforces the committed key list and candidate bound. It does not generate new keys, mutate keys, search key lengths, use CUDA, or claim a solve.

Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3d/`.
