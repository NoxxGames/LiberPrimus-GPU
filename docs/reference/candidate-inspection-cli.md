# Candidate Inspection CLI

The `libreprimus candidate-inspect` command group reads ignored generated candidate outputs and prints or writes summary-only reports.

## inspect-stage3a

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli candidate-inspect inspect-stage3a --results-dir experiments/results/bounded-auto-runs/stage3a --top-n 25 --out-markdown research-log/2026-05-16-stage-3b-stage3a-lead-inspection.md
```

This command reads `candidate_records.jsonl`, `top_candidates.jsonl`, and `summary.json`, then writes a Markdown report without full candidate dumps.

## summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli candidate-inspect summary --results-dir experiments/results/bounded-auto-runs/stage3a
```

Prints run ID, candidate count, top transform metadata, qualitative label, and warning count.

## Reranking

Reranking is exposed through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run rerank --results-dir experiments/results/bounded-auto-runs/stage3a --out-dir experiments/results/bounded-auto-runs/stage3b --top-k 25 --allow-warnings
```

Generated rerank outputs remain ignored and must not be committed.
