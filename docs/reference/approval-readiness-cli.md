# Approval-Readiness CLI

## validate

Validate a Stage 2I proposal and optional pending approval record:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness validate `
  --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml `
  --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml
```

## packet

Generate ignored JSON and Markdown readiness packets:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness packet `
  --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml `
  --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml `
  --out-dir experiments/results/approval-readiness/stage2i `
  --allow-warnings
```

## stage2i-review

Validate all Stage 2I proposals and generate packets:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness stage2i-review `
  --proposal-dir experiments/proposals/stage2i `
  --out-dir experiments/results/approval-readiness/stage2i `
  --allow-warnings
```

## summary

Summarize generated readiness packets:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness summary `
  --results-dir experiments/results/approval-readiness/stage2i
```

## Troubleshooting

If validation fails, check that approval is pending, proposal and approval hashes match, all execution/search/candidate-generation/scoring/CUDA flags are false, the candidate upper bound is `841`, and generated output paths remain ignored.
